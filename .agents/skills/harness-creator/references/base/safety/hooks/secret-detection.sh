#!/bin/bash
#
# secret-detection.sh - Comprehensive secret detection utility
# Scans files and directories for secrets, API keys, passwords, tokens
#
# Usage: ./secret-detection.sh [options] [path...]
#   Options:
#     -a, --all          Scan all files (including hidden)
#     -d, --deep         Deep scan with context
#     -r, --recursive    Scan directories recursively
#     -f, --file FILE    Scan specific file
#     -o, --output FILE  Write results to file
#     -q, --quiet        Quiet mode (exit code only)
#     -v, --verbose      Verbose output
#     --strict           Exit 1 on any finding
#     --entropy          Enable entropy detection
#     --baseline FILE    Use baseline file to ignore known secrets
#
# Exit codes: 0 = no secrets found, 1 = secrets found, 2 = error
#

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
FINDINGS=0
VERBOSE=false
QUIET=false
STRICT=false
DEEP_SCAN=false
ENTROPY_CHECK=false
RECURSIVE=false
SCAN_ALL=false
OUTPUT_FILE=""
BASELINE_FILE=""
BASELINE_HASHES=()

# Directories to skip
SKIP_DIRS=(
    ".git"
    ".svn"
    ".hg"
    "node_modules"
    "venv"
    ".venv"
    "__pycache__"
    "dist"
    "build"
    "target"
    ".idea"
    ".vscode"
    "vendor"
    "bower_components"
)

# File extensions to skip
SKIP_EXTENSIONS=(
    ".png"
    ".jpg"
    ".jpeg"
    ".gif"
    ".ico"
    ".svg"
    ".woff"
    ".woff2"
    ".ttf"
    ".eot"
    ".otf"
    ".mp3"
    ".mp4"
    ".avi"
    ".mov"
    ".pdf"
    ".zip"
    ".tar"
    ".gz"
    ".rar"
    ".7z"
    ".exe"
    ".dll"
    ".so"
    ".dylib"
    ".pyc"
    ".pyo"
    ".class"
    ".jar"
    ".war"
    ".min.js"
    ".min.css"
)

# =============================================================================
# Secret Pattern Definitions
# =============================================================================

declare -A SECRET_PATTERNS

# API Keys
SECRET_PATTERNS["api_key"]="api[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"
SECRET_PATTERNS["apikey"]="apikey\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"
SECRET_PATTERNS["api_key_upper"]="API[_-]?KEY\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# AWS
SECRET_PATTERNS["aws_access_key"]="AKIA[0-9A-Z]{16}"
SECRET_PATTERNS["aws_secret"]="aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9/+=]{40}['\"]?"
SECRET_PATTERNS["aws_session"]="aws[_-]?session[_-]?token\s*[=:]\s*['\"]?[a-zA-Z0-9/+=]{16,}['\"]?"

# Azure
SECRET_PATTERNS["azure_key"]="azure[_-]?(key|storage)[_-]?(key|connection)\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# GCP
SECRET_PATTERNS["gcp_key"]="google[_-]?(cloud|api)[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# Passwords
SECRET_PATTERNS["password"]="password\s*[=:]\s*['\"]?[^\s'\"]{8,}['\"]?"
SECRET_PATTERNS["passwd"]="passwd\s*[=:]\s*['\"]?[^\s'\"]{8,}['\"]?"
SECRET_PATTERNS["pwd"]="pwd\s*[=:]\s*['\"]?[^\s'\"]{8,}['\"]?"

# Tokens
SECRET_PATTERNS["auth_token"]="auth[_-]?token\s*[=:]\s*['\"]?[a-zA-Z0-9_\-\.]{20,}['\"]?"
SECRET_PATTERNS["access_token"]="access[_-]?token\s*[=:]\s*['\"]?[a-zA-Z0-9_\-\.]{20,}['\"]?"
SECRET_PATTERNS["refresh_token"]="refresh[_-]?token\s*[=:]\s*['\"]?[a-zA-Z0-9_\-\.]{20,}['\"]?"
SECRET_PATTERNS["bearer_token"]="bearer\s+[a-zA-Z0-9_\-\.]{20,}"
SECRET_PATTERNS["bearer_header"]="Authorization:\s*Bearer\s+[a-zA-Z0-9_\-\.]{20,}"

# OAuth
SECRET_PATTERNS["oauth_token"]="oauth[_-]?(access)?token\s*[=:]\s*['\"]?[a-zA-Z0-9_\-\.]{20,}['\"]?"
SECRET_PATTERNS["client_secret"]="client[_-]?secret\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# Secrets and Keys
SECRET_PATTERNS["secret_key"]="secret[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"
SECRET_PATTERNS["private_key"]="private[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"
SECRET_PATTERNS["encryption_key"]="encryption[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# JWT
SECRET_PATTERNS["jwt"]="eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*"
SECRET_PATTERNS["jwt_secret"]="jwt[_-]?secret\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"

# SSH Keys
SECRET_PATTERNS["rsa_private"]="-----BEGIN RSA PRIVATE KEY-----"
SECRET_PATTERNS["dsa_private"]="-----BEGIN DSA PRIVATE KEY-----"
SECRET_PATTERNS["ec_private"]="-----BEGIN EC PRIVATE KEY-----"
SECRET_PATTERNS["openssh_private"]="-----BEGIN OPENSSH PRIVATE KEY-----"
SECRET_PATTERNS["pgp_private"]="-----BEGIN PGP PRIVATE KEY BLOCK-----"

# Database URLs
SECRET_PATTERNS["mongo_url"]="mongodb(\+srv)?://[^:]+:[^@]+@[a-zA-Z0-9.-]+"
SECRET_PATTERNS["postgres_url"]="postgres(ql)?://[^:]+:[^@]+@[a-zA-Z0-9.-]+"
SECRET_PATTERNS["mysql_url"]="mysql://[^:]+:[^@]+@[a-zA-Z0-9.-]+"
SECRET_PATTERNS["redis_url"]="redis://[^:]*:[^@]+@[a-zA-Z0-9.-]+"
SECRET_PATTERNS["db_url_generic"]="(jdbc|database)[_-]?url\s*[=:]\s*['\"]?[^'\"]+:[^'\"]+@[^'\"]+['\"]?"

# Generic Secrets
SECRET_PATTERNS["generic_secret"]="secret\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{32,}['\"]?"

# Slack/Discord/Webhooks
SECRET_PATTERNS["slack_webhook"]="https://hooks\.slack\.com/services/T[a-zA-Z0-9]+/B[a-zA-Z0-9]+/[a-zA-Z0-9]+"
SECRET_PATTERNS["discord_webhook"]="https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+"
SECRET_PATTERNS["generic_webhook"]="webhook[_-]?url\s*[=:]\s*['\"]?https://[^'\"]+['\"]?"

# Stripe
SECRET_PATTERNS["stripe_key"]="sk_(live|test)_[a-zA-Z0-9]{24,}"
SECRET_PATTERNS["stripe_publishable"]="pk_(live|test)_[a-zA-Z0-9]{24,}"

# GitHub
SECRET_PATTERNS["github_token"]="ghp_[a-zA-Z0-9]{36}"
SECRET_PATTERNS["github_oauth"]="gho_[a-zA-Z0-9]{36}"
SECRET_PATTERNS["github_app"]="ghu_[a-zA-Z0-9]{36}"
SECRET_PATTERNS["github_refresh"]="ghr_[a-zA-Z0-9]{36}"

# NPM
SECRET_PATTERNS["npm_token"]="//registry\.npmjs\.org/:_authToken=[a-zA-Z0-9-]{36}"

# SendGrid
SECRET_PATTERNS["sendgrid_key"]="SG\.[a-zA-Z0-9_-]{22,}\.[a-zA-Z0-9_-]{43,}"

# Twilio
SECRET_PATTERNS["twilio_sid"]="AC[a-f0-9]{32}"
SECRET_PATTERNS["twilio_token"]="twilio[_-]?auth[_-]?token\s*[=:]\s*['\"]?[a-f0-9]{32}['\"]?"

# RSA Key Fingerprints
SECRET_PATTERNS["rsa_fingerprint"]="SHA256:[a-zA-Z0-9+/]{43}"

# Base64 encoded secrets (entropy-based detection)
SECRET_PATTERNS["base64_secret"]="['\"]?[a-zA-Z0-9+/]{40,}={0,2}['\"]?"

# =============================================================================
# Helper Functions
# =============================================================================

print_usage() {
    cat << EOF
Usage: $0 [options] [path...]

Secret Detection Utility - Scans files for secrets, API keys, passwords, and tokens.

Options:
    -a, --all          Scan all files (including hidden)
    -d, --deep         Deep scan with context lines
    -r, --recursive    Scan directories recursively
    -f, --file FILE    Scan specific file
    -o, --output FILE  Write results to file
    -q, --quiet        Quiet mode (exit code only)
    -v, --verbose      Verbose output
    --strict           Exit 1 on any finding
    --entropy          Enable entropy detection
    --baseline FILE    Use baseline file to ignore known secrets
    -h, --help          Show this help message

Examples:
    $0 --recursive --deep ./src
    $0 --file .env --strict
    $0 --baseline .secrets-baseline ./src

Exit Codes:
    0 - No secrets found
    1 - Secrets found
    2 - Error
EOF
}

should_skip_file() {
    local file="$1"

    # Check extension
    for ext in "${SKIP_EXTENSIONS[@]}"; do
        if [[ "$file" == *"$ext" ]]; then
            return 0
        fi
    done

    # Check if binary
    if file "$file" 2>/dev/null | grep -q "binary"; then
        return 0
    fi

    return 1
}

should_skip_dir() {
    local dir="$1"
    local basename
    basename=$(basename "$dir")

    for skip in "${SKIP_DIRS[@]}"; do
        if [[ "$basename" == "$skip" ]]; then
            return 0
        fi
    done

    return 1
}

load_baseline() {
    if [ -n "$BASELINE_FILE" ] && [ -f "$BASELINE_FILE" ]; then
        while IFS= read -r line; do
            BASELINE_HASHES+=("$line")
        done < "$BASELINE_FILE"
        [ "$VERBOSE" = true ] && echo "Loaded ${#BASELINE_HASHES[@]} baseline entries"
    fi
}

is_baseline() {
    local hash="$1"
    for baseline in "${BASELINE_HASHES[@]}"; do
        if [[ "$hash" == "$baseline" ]]; then
            return 0
        fi
    done
    return 1
}

calculate_entropy() {
    local string="$1"
    local length=${#string}
    local -A char_count
    local entropy=0

    for ((i=0; i<length; i++)); do
        char="${string:$i:1}"
        ((char_count["$char"]++))
    done

    for count in "${char_count[@]}"; do
        local prob=$((count * 100 / length))
        if [ $prob -gt 0 ]; then
            # Using bc for floating point
            local p=$(echo "scale=10; $count / $length" | bc)
            local e=$(echo "scale=10; -$p * l($p) / l(2)" | bc -l)
            entropy=$(echo "$entropy + $e" | bc)
        fi
    done

    echo "$entropy"
}

check_entropy() {
    local string="$1"
    # Skip strings that are too short
    if [ ${#string} -lt 20 ]; then
        return 1
    fi

    local entropy
    entropy=$(calculate_entropy "$string")

    # High entropy threshold (typically > 4.5 indicates random/secret)
    if (( $(echo "$entropy > 4.5" | bc -l) )); then
        return 0
    fi

    return 1
}

report_finding() {
    local file="$1"
    local line_num="$2"
    local pattern_name="$3"
    local match="$4"
    local context="$5"

    ((FINDINGS++))

    if [ "$QUIET" = true ]; then
        return
    fi

    # Create hash for baseline check
    local hash
    hash=$(echo "${file}:${line_num}:${match}" | sha256sum | cut -d' ' -f1)

    if is_baseline "$hash"; then
        [ "$VERBOSE" = true ] && echo -e "${BLUE}[BASELINE]${NC} $file:$line_num"
        ((FINDINGS--))
        return
    fi

    if [ "$DEEP_SCAN" = true ]; then
        echo -e "${RED}[SECRET]${NC} ${MAGENTA}$pattern_name${NC}"
        echo -e "  ${BLUE}File:${NC}     $file"
        echo -e "  ${BLUE}Line:${NC}     $line_num"
        echo -e "  ${BLUE}Match:${NC}    $match"
        if [ -n "$context" ]; then
            echo -e "  ${BLUE}Context:${NC}"
            echo "$context" | sed 's/^/    /'
        fi
        echo ""
    else
        echo -e "${RED}[SECRET]${NC} $file:$line_num - ${MAGENTA}$pattern_name${NC}: $match"
    fi
}

scan_file() {
    local file="$1"

    if [ ! -f "$file" ]; then
        [ "$VERBOSE" = true ] && echo -e "${YELLOW}Skipping non-file: $file${NC}"
        return
    fi

    if should_skip_file "$file"; then
        [ "$VERBOSE" = true ] && echo -e "${BLUE}Skipping: $file${NC}"
        return
    fi

    [ "$VERBOSE" = true ] && echo -e "${GREEN}Scanning: $file${NC}"

    local line_num=0
    local prev_line=""
    local curr_line=""
    local next_line=""

    while IFS= read -r line || [ -n "$line" ]; do
        ((line_num++))
        prev_line="$curr_line"
        curr_line="$next_line"
        next_line="$line"

        if [ $line_num -lt 2 ]; then
            continue
        fi

        # Check each pattern
        for pattern_name in "${!SECRET_PATTERNS[@]}"; do
            local pattern="${SECRET_PATTERNS[$pattern_name]}"

            if echo "$curr_line" | grep -qiE "$pattern" 2>/dev/null; then
                local match
                match=$(echo "$curr_line" | grep -oiE "$pattern" | head -1)

                # Skip common false positives
                if [[ "$match" =~ "example" ]] || [[ "$match" =~ "test" ]] || \
                   [[ "$match" =~ "placeholder" ]] || [[ "$match" =~ "your_" ]] || \
                   [[ "$match" =~ "xxx" ]] || [[ "$match" =~ "dummy" ]]; then
                    [ "$VERBOSE" = true ] && echo -e "  ${BLUE}Skipping false positive: $match${NC}"
                    continue
                fi

                # Check entropy if enabled
                if [ "$ENTROPY_CHECK" = true ]; then
                    if ! check_entropy "$match"; then
                        continue
                    fi
                fi

                # Build context for deep scan
                local context=""
                if [ "$DEEP_SCAN" = true ]; then
                    context="$((line_num - 1)): $prev_line\n$line_num: $curr_line\n$((line_num + 1)): $next_line"
                fi

                report_finding "$file" "$line_num" "$pattern_name" "$match" "$context"
            fi
        done
    done < "$file"

    # Process last line
    curr_line="$next_line"
    line_num=$((line_num + 1))

    for pattern_name in "${!SECRET_PATTERNS[@]}"; do
        local pattern="${SECRET_PATTERNS[$pattern_name]}"
        if echo "$curr_line" | grep -qiE "$pattern" 2>/dev/null; then
            local match
            match=$(echo "$curr_line" | grep -oiE "$pattern" | head -1)
            report_finding "$file" "$line_num" "$pattern_name" "$match" ""
        fi
    done
}

scan_directory() {
    local dir="$1"

    if [ ! -d "$dir" ]; then
        echo -e "${RED}Error: $dir is not a directory${NC}"
        return
    fi

    [ "$VERBOSE" = true ] && echo -e "${GREEN}Scanning directory: $dir${NC}"

    if [ "$RECURSIVE" = true ]; then
        while IFS= read -r -d '' file; do
            if should_skip_dir "$(dirname "$file")"; then
                continue
            fi
            scan_file "$file"
        done < <(find "$dir" -type f -print0 2>/dev/null)
    else
        for file in "$dir"/*; do
            if [ -f "$file" ]; then
                if ! should_skip_file "$file"; then
                    scan_file "$file"
                fi
            fi
        done
    fi
}

# =============================================================================
# Parse Arguments
# =============================================================================

PATHS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            SCAN_ALL=true
            shift
            ;;
        -d|--deep)
            DEEP_SCAN=true
            shift
            ;;
        -r|--recursive)
            RECURSIVE=true
            shift
            ;;
        -f|--file)
            shift
            SCAN_FILE="$1"
            shift
            ;;
        -o|--output)
            shift
            OUTPUT_FILE="$1"
            shift
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --strict)
            STRICT=true
            shift
            ;;
        --entropy)
            ENTROPY_CHECK=true
            shift
            ;;
        --baseline)
            shift
            BASELINE_FILE="$1"
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            PATHS+=("$1")
            shift
            ;;
    esac
done

# =============================================================================
# Main Execution
# =============================================================================

[ "$VERBOSE" = true ] && echo "Starting secret detection scan..."

# Load baseline if specified
load_baseline

# Scan specified file or paths
if [ -n "$SCAN_FILE" ]; then
    scan_file "$SCAN_FILE"
elif [ ${#PATHS[@]} -gt 0 ]; then
    for path in "${PATHS[@]}"; do
        if [ -f "$path" ]; then
            scan_file "$path"
        elif [ -d "$path" ]; then
            scan_directory "$path"
        else
            echo -e "${RED}Error: $path does not exist${NC}"
        fi
    done
else
    # Default to current directory
    scan_directory "."
fi

# =============================================================================
# Summary
# =============================================================================

if [ "$QUIET" = true ]; then
    [ $FINDINGS -gt 0 ] && exit 1
    exit 0
fi

echo ""
echo "=========================================="
echo "Secret Detection Summary"
echo "=========================================="

if [ $FINDINGS -gt 0 ]; then
    echo -e "${RED}Found $FINDINGS potential secret(s)${NC}"
    echo ""
    echo "Recommendations:"
    echo "  1. Review each finding above"
    echo "  2. Remove secrets from code"
    echo "  3. Use environment variables or secret managers"
    echo "  4. Rotate any exposed credentials immediately"
    echo "  5. Add secrets to .gitignore"
    echo ""

    if [ -n "$BASELINE_FILE" ]; then
        echo "To create a baseline of known secrets:"
        echo "  $0 --recursive . > $BASELINE_FILE"
    fi

    [ "$STRICT" = true ] && exit 1
    exit 1
else
    echo -e "${GREEN}No secrets detected${NC}"
    exit 0
fi