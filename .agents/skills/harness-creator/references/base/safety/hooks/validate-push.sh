#!/bin/bash
#
# validate-push.sh - Pre-push validation hook
# Warns on force push, direct pushes to main, and other unsafe push patterns
#
# Usage: ./validate-push.sh [remote] [ref]
# Exit codes: 0 = allow, 1 = block, 2 = warning only
#

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REMOTE="${1:-origin}"
REF="${2:-$(git symbolic-ref HEAD 2>/dev/null || git rev-parse HEAD)}"
BRANCH="${REF#refs/heads/}"

ERRORS=0
WARNINGS=0

echo "=== Push Validation ==="
echo "Remote: $REMOTE"
echo "Branch: $BRANCH"
echo ""

# =============================================================================
# Check 1: Force Push Detection
# =============================================================================

check_force_push() {
    # Check if this is a force push
    local remote_branch
    remote_branch=$(git ls-remote --heads "$REMOTE" "$BRANCH" 2>/dev/null | cut -f1)

    if [ -n "$remote_branch" ]; then
        local local_commit
        local_commit=$(git rev-parse HEAD 2>/dev/null)

        # Check if local commit is an ancestor of remote
        if ! git merge-base --is-ancestor "$remote_branch" "$local_commit" 2>/dev/null; then
            # Check if --force flag was used (check git config or environment)
            if git config --get advice.pushForce 2>/dev/null | grep -q "false" || \
               echo "$GIT_PUSH_OPTION_FORCE" | grep -q "true" 2>/dev/null; then
                echo -e "${RED}BLOCKED: Force push detected${NC}"
                echo "  Force pushing to '$BRANCH' is not allowed."
                echo "  Use 'git push --force-with-lease' if you must force push."
                echo "  Better yet, create a new commit that merges/rebases properly."
                ((ERRORS++))
                return 1
            fi

            echo -e "${YELLOW}WARNING: Your branch has diverged from remote${NC}"
            echo "  Local commits may not include remote changes."
            echo "  Consider using 'git pull --rebase' before pushing."
            echo "  If you must force push, use 'git push --force-with-lease'."
            ((WARNINGS++))
        fi
    fi

    return 0
}

# =============================================================================
# Check 2: Direct Push to Main/Master
# =============================================================================

check_main_push() {
    if [[ "$BRANCH" == "main" ]] || [[ "$BRANCH" == "master" ]]; then
        echo -e "${RED}BLOCKED: Direct push to $BRANCH branch${NC}"
        echo "  Direct pushes to '$BRANCH' are not allowed."
        echo "  Please:"
        echo "  1. Create a feature branch: git checkout -b feature/your-feature"
        echo "  2. Push to your branch: git push origin feature/your-feature"
        echo "  3. Create a Pull Request for review"
        ((ERRORS++))
        return 1
    fi

    return 0
}

# =============================================================================
# Check 3: Protected Branches
# =============================================================================

check_protected_branches() {
    local protected_branches=("main" "master" "develop" "staging" "production" "release/*")

    for pattern in "${protected_branches[@]}"; do
        if [[ "$BRANCH" == $pattern ]]; then
            # Already checked main/master above
            if [[ "$BRANCH" != "main" ]] && [[ "$BRANCH" != "master" ]]; then
                echo -e "${YELLOW}WARNING: Pushing to protected branch '$BRANCH'${NC}"
                echo "  This branch may have additional protection rules."
                echo "  Consider using a feature branch instead."
                ((WARNINGS++))
            fi
        fi
    done

    return 0
}

# =============================================================================
# Check 4: Commit Count Warning
# =============================================================================

check_commit_count() {
    local remote_branch
    remote_branch=$(git ls-remote --heads "$REMOTE" "$BRANCH" 2>/dev/null | cut -f1)

    if [ -n "$remote_branch" ]; then
        local commit_count
        commit_count=$(git rev-list --count "$remote_branch"..HEAD 2>/dev/null || echo "0")

        if [ "$commit_count" -gt 10 ]; then
            echo -e "${YELLOW}WARNING: Pushing $commit_count commits${NC}"
            echo "  Consider squashing or organizing your commits."
            echo "  Large pushes are harder to review and may cause issues."
            ((WARNINGS++))
        elif [ "$commit_count" -gt 5 ]; then
            echo -e "${BLUE}INFO: Pushing $commit_count commits${NC}"
        fi
    fi

    return 0
}

# =============================================================================
# Check 5: Require PR for Large Changes
# =============================================================================

check_pr_requirement() {
    local remote_branch
    remote_branch=$(git ls-remote --heads "$REMOTE" "$BRANCH" 2>/dev/null | cut -f1)

    if [ -n "$remote_branch" ]; then
        # Count changed files
        local changed_files
        changed_files=$(git diff --name-only "$remote_branch" HEAD 2>/dev/null | wc -l)

        if [ "$changed_files" -gt 20 ]; then
            echo -e "${YELLOW}WARNING: Large changeset ($changed_files files)${NC}"
            echo "  Consider creating a Pull Request for review."
            echo "  Large changes should be reviewed before merging."
            ((WARNINGS++))
        fi
    fi

    return 0
}

# =============================================================================
# Check 6: Test Status
# =============================================================================

check_test_status() {
    # Check if there are test files modified
    local test_files
    test_files=$(git diff --name-only HEAD~1 2>/dev/null | grep -E "test|spec" || true)

    if [ -n "$test_files" ]; then
        echo -e "${BLUE}INFO: Test files modified${NC}"
        echo "  Ensure tests pass before pushing: $(echo "$test_files" | head -3)"
    fi

    return 0
}

# =============================================================================
# Run All Checks
# =============================================================================

check_main_push
if [ $ERRORS -eq 0 ]; then
    check_force_push
    check_protected_branches
    check_commit_count
    check_pr_requirement
    check_test_status
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo "=== Push Validation Summary ==="

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}BLOCKED: $ERRORS error(s) found${NC}"
    echo "Push rejected. Please fix the above issues."
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}WARNING: $WARNINGS warning(s) found${NC}"
    echo "Push allowed, but please review the warnings above."
    echo ""
    echo "To proceed with the push, run: git push $REMOTE $BRANCH"
    exit 2
fi

echo -e "${GREEN}All checks passed!${NC}"
echo "Push allowed to $BRANCH"
exit 0