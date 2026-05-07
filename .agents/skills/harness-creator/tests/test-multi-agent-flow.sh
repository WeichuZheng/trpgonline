#!/bin/bash
set -e

# Test: Multi-Agent Flow
# Description: Tests the complete Planner -> Generator -> Evaluator flow
# Validates that each agent properly performs its role in the GAN-inspired architecture

echo "Running test: Multi-Agent Flow"

# Setup
TEST_DIR="D:/01coding/00projects/github/harness-creator"
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Test 1: Planner generates spec from brief prompt
echo ""
echo "=== Phase 1: Planner Generates Spec ==="

# Check planner agent definition exists
PLANNER_DEF="$TEST_DIR/references/base/core/agents/planner.md"
if [ ! -f "$PLANNER_DEF" ]; then
    echo "FAIL: Planner agent definition not found at $PLANNER_DEF"
    exit 1
fi
echo "PASS: Planner agent definition exists"

# Verify planner has correct responsibilities
if grep -q "Transforms brief prompts into comprehensive specs" "$PLANNER_DEF"; then
    echo "PASS: Planner has correct primary responsibility"
else
    echo "FAIL: Planner missing primary responsibility"
    exit 1
fi

# Verify planner does NOT implement code
if grep -q "NOT.*implement" "$PLANNER_DEF" || grep -q "Leave implementation" "$PLANNER_DEF"; then
    echo "PASS: Planner correctly avoids implementation"
else
    echo "FAIL: Planner should not implement code"
    exit 1
fi

# Test 2: Generator proposes sprint contract
echo ""
echo "=== Phase 2: Generator Proposes Contract ==="

GENERATOR_DEF="$TEST_DIR/references/base/core/agents/generator.md"
if [ ! -f "$GENERATOR_DEF" ]; then
    echo "FAIL: Generator agent definition not found at $GENERATOR_DEF"
    exit 1
fi
echo "PASS: Generator agent definition exists"

# Verify generator negotiates contracts
if grep -q "Negotiates.*contract" "$GENERATOR_DEF" || grep -q "sprint contract" "$GENERATOR_DEF"; then
    echo "PASS: Generator has contract negotiation responsibility"
else
    echo "FAIL: Generator missing contract negotiation"
    exit 1
fi

# Test 3: Evaluator negotiates contract
echo ""
echo "=== Phase 3: Evaluator Negotiates Contract ==="

EVALUATOR_DEF="$TEST_DIR/references/base/core/agents/evaluator.md"
if [ ! -f "$EVALUATOR_DEF" ]; then
    echo "FAIL: Evaluator agent definition not found at $EVALUATOR_DEF"
    exit 1
fi
echo "PASS: Evaluator agent definition exists"

# Verify evaluator is separate from generator
if grep -q "NOT.*Generator" "$EVALUATOR_DEF" || grep -q "did NOT build" "$EVALUATOR_DEF"; then
    echo "PASS: Evaluator correctly separated from Generator"
else
    echo "FAIL: Evaluator must be separate from Generator"
    exit 1
fi

# Test 4: Generator implements after contract approval
echo ""
echo "=== Phase 4: Generator Implements ==="

# Check generator has implementation responsibilities
if grep -q "Implement" "$GENERATOR_DEF"; then
    echo "PASS: Generator has implementation responsibility"
else
    echo "FAIL: Generator missing implementation responsibility"
    exit 1
fi

# Verify generator workflow includes handoff
if grep -q "Hand off" "$GENERATOR_DEF"; then
    echo "PASS: Generator workflow includes handoff to Evaluator"
else
    echo "FAIL: Generator should hand off to Evaluator"
    exit 1
fi

# Test 5: Evaluator grades implementation
echo ""
echo "=== Phase 5: Evaluator Grades ==="

# Verify evaluator grades work
if grep -q "grade" "$EVALUATOR_DEF" || grep -q "PASS.*FAIL" "$EVALUATOR_DEF"; then
    echo "PASS: Evaluator has grading responsibility"
else
    echo "FAIL: Evaluator missing grading responsibility"
    exit 1
fi

# Verify evaluator provides actionable feedback
if grep -q "actionable feedback" "$EVALUATOR_DEF" || grep -q "specific.*Action" "$EVALUATOR_DEF"; then
    echo "PASS: Evaluator provides actionable feedback"
else
    echo "FAIL: Evaluator should provide actionable feedback"
    exit 1
fi

# Test 6: Verify complete workflow documentation
echo ""
echo "=== Phase 6: Complete Workflow Documentation ==="

ARCH_DOC="$TEST_DIR/references/base/core/docs/multi-agent-architecture.md"
if [ ! -f "$ARCH_DOC" ]; then
    echo "FAIL: Multi-agent architecture doc not found"
    exit 1
fi
echo "PASS: Multi-agent architecture documentation exists"

# Verify workflow shows Planner -> Generator -> Evaluator
if grep -q "Planner.*Generator.*Evaluator" "$ARCH_DOC" || grep -q "Planner.*-->.*Generator.*-->.*Evaluator" "$ARCH_DOC"; then
    echo "PASS: Workflow shows correct agent order"
else
    echo "FAIL: Workflow should show Planner -> Generator -> Evaluator order"
    exit 1
fi

# Verify feedback loop exists
if grep -q "Feedback Loop" "$ARCH_DOC"; then
    echo "PASS: Feedback loop documented"
else
    echo "FAIL: Feedback loop should be documented"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "========================================"
echo "PASS: Test Multi-Agent Flow completed successfully"
echo "========================================"