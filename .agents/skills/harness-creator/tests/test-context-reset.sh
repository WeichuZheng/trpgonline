#!/bin/bash
set -e

# Test: Context Reset Protocol
# Description: Tests checkpoint with handoff, resume from handoff, and context preservation
# Validates that the handoff artifact contains all necessary information for continuation

echo "Running test: Context Reset"

# Setup
TEST_DIR="D:/01coding/00projects/github/harness-creator"
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Test 1: Handoff artifact template exists
echo ""
echo "=== Phase 1: Handoff Artifact Template ==="

HANDOFF_TEMPLATE="$TEST_DIR/references/base/progress/templates/handoff-artifact.md"
if [ ! -f "$HANDOFF_TEMPLATE" ]; then
    echo "FAIL: Handoff artifact template not found at $HANDOFF_TEMPLATE"
    exit 1
fi
echo "PASS: Handoff artifact template exists"

# Test 2: Verify Session Summary section
echo ""
echo "=== Phase 2: Session Summary ==="

if grep -q "## Session Summary" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Session Summary section"
else
    echo "FAIL: Handoff must have Session Summary section"
    exit 1
fi

# Test 3: Verify Completed Work section
echo ""
echo "=== Phase 3: Completed Work ==="

if grep -q "## Completed Work" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Completed Work section"
else
    echo "FAIL: Handoff must have Completed Work section"
    exit 1
fi

# Verify subsections for Done, Verified, Committed
if grep -q "### Done" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Done subsection"
else
    echo "FAIL: Handoff must have Done subsection"
    exit 1
fi

if grep -q "### Verified" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Verified subsection"
else
    echo "FAIL: Handoff must have Verified subsection"
    exit 1
fi

if grep -q "### Committed" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Committed subsection"
else
    echo "FAIL: Handoff must have Committed subsection"
    exit 1
fi

# Test 4: Verify Current State section
echo ""
echo "=== Phase 4: Current State ==="

if grep -q "## Current State" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Current State section"
else
    echo "FAIL: Handoff must have Current State section"
    exit 1
fi

# Verify Files Modified tracking
if grep -q "### Files Modified" "$HANDOFF_TEMPLATE" || grep -q "Files Modified" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff tracks Files Modified"
else
    echo "FAIL: Handoff should track Files Modified"
    exit 1
fi

# Verify Test Status section
if grep -q "### Test Status" "$HANDOFF_TEMPLATE" || grep -q "Test Status" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff tracks Test Status"
else
    echo "FAIL: Handoff should track Test Status"
    exit 1
fi

# Verify Git State section
if grep -q "### Git State" "$HANDOFF_TEMPLATE" || grep -q "Git State" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff tracks Git State"
else
    echo "FAIL: Handoff should track Git State"
    exit 1
fi

# Test 5: Verify Next Immediate Step section
echo ""
echo "=== Phase 5: Next Immediate Step ==="

if grep -q "## Next Immediate Step" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Next Immediate Step section"
else
    echo "FAIL: Handoff must have Next Immediate Step section"
    exit 1
fi

# Verify it includes What, How, Expected outcome, Blockers
if grep -q "What to do next" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff specifies what to do next"
else
    echo "FAIL: Handoff should specify what to do next"
    exit 1
fi

if grep -q "How to do it" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff specifies how to do it"
else
    echo "FAIL: Handoff should specify how to do it"
    exit 1
fi

if grep -q "Expected outcome" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff specifies expected outcome"
else
    echo "FAIL: Handoff should specify expected outcome"
    exit 1
fi

if grep -q "Blockers" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff specifies blockers"
else
    echo "FAIL: Handoff should specify blockers"
    exit 1
fi

# Test 6: Verify Key Decisions section
echo ""
echo "=== Phase 6: Key Decisions ==="

if grep -q "## Key Decisions" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Key Decisions section"
else
    echo "FAIL: Handoff must have Key Decisions section"
    exit 1
fi

# Verify decision captures rationale and alternatives
if grep -q "Rationale" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff captures decision rationale"
else
    echo "FAIL: Handoff should capture decision rationale"
    exit 1
fi

if grep -q "Alternatives" "$HANDOFF_TEMPLATE" || grep -q "Alternatives Considered" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff captures alternatives considered"
else
    echo "FAIL: Handoff should capture alternatives considered"
    exit 1
fi

# Test 7: Verify Commands to Resume section
echo ""
echo "=== Phase 7: Commands to Resume ==="

if grep -q "## Commands to Resume" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Commands to Resume section"
else
    echo "FAIL: Handoff must have Commands to Resume section"
    exit 1
fi

# Verify Quick Resume command
if grep -q "Quick Resume" "$HANDOFF_TEMPLATE" || grep -q "/start" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff includes Quick Resume command"
else
    echo "FAIL: Handoff should include Quick Resume command"
    exit 1
fi

# Test 8: Verify Checklist for New Session
echo ""
echo "=== Phase 8: New Session Checklist ==="

if grep -q "## Checklist for New Session" "$HANDOFF_TEMPLATE" || grep -q "Checklist" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Checklist for New Session"
else
    echo "FAIL: Handoff should have Checklist for New Session"
    exit 1
fi

# Verify checklist items exist
if grep -q "Read this entire handoff" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Checklist includes reading handoff"
else
    echo "FAIL: Checklist should include reading handoff"
    exit 1
fi

if grep -q "Reviewed git status" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Checklist includes reviewing git status"
else
    echo "FAIL: Checklist should include reviewing git status"
    exit 1
fi

# Test 9: Verify Context Reset vs Compaction distinction
echo ""
echo "=== Phase 9: Context Reset Definition ==="

if grep -q "Context Reset" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff defines Context Reset"
else
    echo "FAIL: Handoff should define Context Reset"
    exit 1
fi

# Verify it explains why Context Reset matters
if grep -q "Why Context Reset Matters" "$HANDOFF_TEMPLATE" || grep -q "Fresh Evaluator" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff explains why Context Reset matters"
else
    echo "FAIL: Handoff should explain why Context Reset matters"
    exit 1
fi

# Test 10: Verify Handoff Metadata section
echo ""
echo "=== Phase 10: Handoff Metadata ==="

if grep -q "## Handoff Metadata" "$HANDOFF_TEMPLATE" || grep -q "Metadata" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff has Metadata section"
else
    echo "FAIL: Handoff should have Metadata section"
    exit 1
fi

# Verify metadata includes Created, Session ID, TTL
if grep -q "Created" "$HANDOFF_TEMPLATE" && grep -q "Session ID" "$HANDOFF_TEMPLATE"; then
    echo "PASS: Handoff metadata includes Created and Session ID"
else
    echo "FAIL: Handoff metadata should include Created and Session ID"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "========================================"
echo "PASS: Test Context Reset completed successfully"
echo "========================================"