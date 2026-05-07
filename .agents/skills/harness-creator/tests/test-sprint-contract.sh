#!/bin/bash
set -e

# Test: Sprint Contract Negotiation Flow
# Description: Tests sprint contract negotiation between Generator and Evaluator
# Validates contract lifecycle: PROPOSE -> REVIEW -> NEGOTIATE -> APPROVE -> IMPLEMENT -> EVALUATE

echo "Running test: Sprint Contract"

# Setup
TEST_DIR="D:/01coding/00projects/github/harness-creator"
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Test 1: Sprint contract skill definition exists
echo ""
echo "=== Phase 1: Contract Skill Definition ==="

CONTRACT_SKILL="$TEST_DIR/references/base/core/skills/sprint-contract/SKILL.md"
if [ ! -f "$CONTRACT_SKILL" ]; then
    echo "FAIL: Sprint contract skill not found at $CONTRACT_SKILL"
    exit 1
fi
echo "PASS: Sprint contract skill definition exists"

# Test 2: Contract template exists
echo ""
echo "=== Phase 2: Contract Template ==="

CONTRACT_TEMPLATE="$TEST_DIR/references/base/core/templates/sprint-contract.md"
if [ ! -f "$CONTRACT_TEMPLATE" ]; then
    echo "FAIL: Sprint contract template not found at $CONTRACT_TEMPLATE"
    exit 1
fi
echo "PASS: Sprint contract template exists"

# Test 3: Verify contract lifecycle phases
echo ""
echo "=== Phase 3: Contract Lifecycle Phases ==="

# Verify PROPOSE phase
if grep -q "PROPOSE" "$CONTRACT_SKILL" || grep -q "Generator proposes" "$CONTRACT_SKILL"; then
    echo "PASS: PROPOSE phase documented"
else
    echo "FAIL: PROPOSE phase should be documented"
    exit 1
fi

# Verify REVIEW phase
if grep -q "REVIEW" "$CONTRACT_SKILL" || grep -q "Evaluator reviews" "$CONTRACT_SKILL"; then
    echo "PASS: REVIEW phase documented"
else
    echo "FAIL: REVIEW phase should be documented"
    exit 1
fi

# Verify NEGOTIATE phase
if grep -q "NEGOTIATE" "$CONTRACT_SKILL" || grep -q "Negotiation" "$CONTRACT_SKILL"; then
    echo "PASS: NEGOTIATE phase documented"
else
    echo "FAIL: NEGOTIATE phase should be documented"
    exit 1
fi

# Verify APPROVE phase
if grep -q "APPROVE" "$CONTRACT_SKILL" || grep -q "Agreement" "$CONTRACT_SKILL"; then
    echo "PASS: APPROVE phase documented"
else
    echo "FAIL: APPROVE phase should be documented"
    exit 1
fi

# Test 4: Contract template has required sections
echo ""
echo "=== Phase 4: Contract Template Sections ==="

# Check Scope section
if grep -q "## Scope" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has Scope section"
else
    echo "FAIL: Contract must have Scope section"
    exit 1
fi

# Check Testable Behaviors section
if grep -q "## Testable Behaviors" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has Testable Behaviors section"
else
    echo "FAIL: Contract must have Testable Behaviors section"
    exit 1
fi

# Check Acceptance Criteria section
if grep -q "## Acceptance Criteria" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has Acceptance Criteria section"
else
    echo "FAIL: Contract must have Acceptance Criteria section"
    exit 1
fi

# Check Negotiation Log section
if grep -q "## Negotiation Log" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has Negotiation Log section"
else
    echo "FAIL: Contract must have Negotiation Log section"
    exit 1
fi

# Test 5: Verify testability requirements
echo ""
echo "=== Phase 5: Testability Requirements ==="

# Check that template includes testable checkboxes
if grep -q "\[ \].*B" "$CONTRACT_TEMPLATE" || grep -q "\- \[ \]" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has testable behavior checkboxes"
else
    echo "FAIL: Contract should have testable behavior checkboxes"
    exit 1
fi

# Check priority levels exist (P1/P2/P3)
if grep -q "P1" "$CONTRACT_TEMPLATE" && grep -q "P2" "$CONTRACT_TEMPLATE" && grep -q "P3" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has priority levels (P1/P2/P3)"
else
    echo "FAIL: Contract should have priority levels"
    exit 1
fi

# Test 6: Verify good vs bad criteria guidance
echo ""
echo "=== Phase 6: Criteria Quality Guidance ==="

if grep -q "Good.*Criteria" "$CONTRACT_SKILL" || grep -q "Good Criteria" "$CONTRACT_SKILL"; then
    echo "PASS: Good criteria examples documented"
else
    echo "FAIL: Good criteria examples should be documented"
    exit 1
fi

if grep -q "Bad.*Criteria" "$CONTRACT_SKILL" || grep -q "Bad Criteria" "$CONTRACT_SKILL"; then
    echo "PASS: Bad criteria examples documented"
else
    echo "FAIL: Bad criteria examples should be documented"
    exit 1
fi

# Test 7: Verify Generator/Evaluator responsibilities
echo ""
echo "=== Phase 7: Agent Responsibilities ==="

# Generator responsibilities
if grep -q "Generator Responsibilities" "$CONTRACT_SKILL"; then
    echo "PASS: Generator responsibilities documented"
else
    echo "FAIL: Generator responsibilities should be documented"
    exit 1
fi

# Evaluator responsibilities
if grep -q "Evaluator Responsibilities" "$CONTRACT_SKILL"; then
    echo "PASS: Evaluator responsibilities documented"
else
    echo "FAIL: Evaluator responsibilities should be documented"
    exit 1
fi

# Test 8: Verify no implementation before approval
echo ""
echo "=== Phase 8: Implementation Approval Gate ==="

if grep -q "No implementation until" "$CONTRACT_SKILL" || grep -q "until.*approved" "$CONTRACT_SKILL"; then
    echo "PASS: Implementation approval gate documented"
else
    echo "FAIL: Should require approval before implementation"
    exit 1
fi

# Test 9: Verify sign-off section in template
echo ""
echo "=== Phase 9: Sign-off Section ==="

if grep -q "## Sign-off" "$CONTRACT_TEMPLATE" || grep -q "Signature" "$CONTRACT_TEMPLATE"; then
    echo "PASS: Contract has sign-off section"
else
    echo "FAIL: Contract should have sign-off section"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "========================================"
echo "PASS: Test Sprint Contract completed successfully"
echo "========================================"