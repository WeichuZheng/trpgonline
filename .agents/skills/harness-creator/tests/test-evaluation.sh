#!/bin/bash
set -e

# Test: Evaluation System
# Description: Tests that evaluator catches known issues, provides actionable feedback,
#              and uses correct criteria weights
# Validates evaluation criteria template and evaluation report format

echo "Running test: Evaluation"

# Setup
TEST_DIR="D:/01coding/00projects/github/harness-creator"
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Test 1: Evaluation criteria template exists
echo ""
echo "=== Phase 1: Evaluation Criteria Template ==="

CRITERIA_TEMPLATE="$TEST_DIR/references/base/evaluator/templates/evaluation-criteria.md"
if [ ! -f "$CRITERIA_TEMPLATE" ]; then
    echo "FAIL: Evaluation criteria template not found at $CRITERIA_TEMPLATE"
    exit 1
fi
echo "PASS: Evaluation criteria template exists"

# Test 2: Evaluation report template exists
echo ""
echo "=== Phase 2: Evaluation Report Template ==="

REPORT_TEMPLATE="$TEST_DIR/references/base/core/templates/evaluation-report.md"
if [ ! -f "$REPORT_TEMPLATE" ]; then
    echo "FAIL: Evaluation report template not found at $REPORT_TEMPLATE"
    exit 1
fi
echo "PASS: Evaluation report template exists"

# Test 3: Verify grading guide with scores
echo ""
echo "=== Phase 3: Grading Guide ==="

# Verify 0-10 scoring system
if grep -q "10/10" "$CRITERIA_TEMPLATE" && grep -q "0/10" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Grading guide uses 0-10 scoring system"
else
    echo "FAIL: Grading guide should use 0-10 scoring system"
    exit 1
fi

# Verify score descriptions exist
if grep -q "Perfect" "$CRITERIA_TEMPLATE" && grep -q "Fail" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Grading guide has score descriptions"
else
    echo "FAIL: Grading guide should have score descriptions"
    exit 1
fi

# Test 4: Verify PASS/FAIL determination
echo ""
echo "=== Phase 4: PASS/FAIL Determination ==="

if grep -q "PASS.*FAIL" "$CRITERIA_TEMPLATE" || grep -q "PASS/FAIL" "$CRITERIA_TEMPLATE"; then
    echo "PASS: PASS/FAIL determination documented"
else
    echo "FAIL: PASS/FAIL determination should be documented"
    exit 1
fi

# Verify threshold concept
if grep -q "threshold" "$CRITERIA_TEMPLATE" || grep -q "Threshold" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Threshold concept documented"
else
    echo "FAIL: Threshold concept should be documented"
    exit 1
fi

# Test 5: Verify priority levels and weights
echo ""
echo "=== Phase 5: Priority Levels and Weights ==="

# Verify P1/P2/P3 priorities
if grep -q "P1.*Blocker" "$CRITERIA_TEMPLATE" || grep -q "P1 (Blocker)" "$CRITERIA_TEMPLATE"; then
    echo "PASS: P1 (Blocker) priority documented"
else
    echo "FAIL: P1 (Blocker) priority should be documented"
    exit 1
fi

if grep -q "P2.*Important" "$CRITERIA_TEMPLATE" || grep -q "P2 (Important)" "$CRITERIA_TEMPLATE"; then
    echo "PASS: P2 (Important) priority documented"
else
    echo "FAIL: P2 (Important) priority should be documented"
    exit 1
fi

if grep -q "P3.*Nice" "$CRITERIA_TEMPLATE" || grep -q "P3 (Nice-to-have)" "$CRITERIA_TEMPLATE"; then
    echo "PASS: P3 (Nice-to-have) priority documented"
else
    echo "FAIL: P3 (Nice-to-have) priority should be documented"
    exit 1
fi

# Verify Weight field exists
if grep -q "Weight" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Weight field documented"
else
    echo "FAIL: Weight field should be documented"
    exit 1
fi

# Test 6: Verify criterion-by-criterion grading in report template
echo ""
echo "=== Phase 6: Criterion-by-Criterion Grading ==="

if grep -q "Criterion-by-Criterion Grading" "$REPORT_TEMPLATE" || grep -q "Criterion.*Grading" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has criterion-by-criterion grading section"
else
    echo "FAIL: Report should have criterion-by-criterion grading section"
    exit 1
fi

# Verify Status, Score, Evidence, Action fields
if grep -q "Status.*PASS.*FAIL" "$REPORT_TEMPLATE" || grep -q "Status" "$REPORT_TEMPLATE"; then
    echo "PASS: Report includes Status field"
else
    echo "FAIL: Report should include Status field"
    exit 1
fi

if grep -q "Score" "$REPORT_TEMPLATE"; then
    echo "PASS: Report includes Score field"
else
    echo "FAIL: Report should include Score field"
    exit 1
fi

if grep -q "Evidence" "$REPORT_TEMPLATE"; then
    echo "PASS: Report includes Evidence field"
else
    echo "FAIL: Report should include Evidence field"
    exit 1
fi

if grep -q "Action" "$REPORT_TEMPLATE"; then
    echo "PASS: Report includes Action field (for actionable feedback)"
else
    echo "FAIL: Report should include Action field"
    exit 1
fi

# Test 7: Verify actionable feedback examples
echo ""
echo "=== Phase 7: Actionable Feedback Examples ==="

# Check for PASS example with specific evidence
if grep -q "PASS Example" "$CRITERIA_TEMPLATE"; then
    echo "PASS: PASS example documented"
else
    echo "FAIL: PASS example should be documented"
    exit 1
fi

# Check for FAIL example with specific action items
if grep -q "FAIL Example" "$CRITERIA_TEMPLATE"; then
    echo "PASS: FAIL example documented"
else
    echo "FAIL: FAIL example should be documented"
    exit 1
fi

# Verify FAIL example includes numbered action items
if grep -q "Action:" "$CRITERIA_TEMPLATE" && grep -q "1\." "$CRITERIA_TEMPLATE"; then
    echo "PASS: FAIL example includes numbered action items"
else
    echo "FAIL: FAIL example should include numbered action items"
    exit 1
fi

# Test 8: Verify Summary Statistics section in report
echo ""
echo "=== Phase 8: Summary Statistics ==="

if grep -q "## Summary Statistics" "$REPORT_TEMPLATE" || grep -q "Summary Statistics" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has Summary Statistics section"
else
    echo "FAIL: Report should have Summary Statistics section"
    exit 1
fi

# Verify statistics track Passed, Failed, Pass Rate, Average Score
if grep -q "Passed" "$REPORT_TEMPLATE" && grep -q "Failed" "$REPORT_TEMPLATE"; then
    echo "PASS: Summary tracks Passed and Failed counts"
else
    echo "FAIL: Summary should track Passed and Failed counts"
    exit 1
fi

if grep -q "Pass Rate" "$REPORT_TEMPLATE"; then
    echo "PASS: Summary tracks Pass Rate"
else
    echo "FAIL: Summary should track Pass Rate"
    exit 1
fi

if grep -q "Average Score" "$REPORT_TEMPLATE"; then
    echo "PASS: Summary tracks Average Score"
else
    echo "FAIL: Summary should track Average Score"
    exit 1
fi

# Test 9: Verify Priority Breakdown section
echo ""
echo "=== Phase 9: Priority Breakdown ==="

if grep -q "## Priority Breakdown" "$REPORT_TEMPLATE" || grep -q "Priority Breakdown" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has Priority Breakdown section"
else
    echo "FAIL: Report should have Priority Breakdown section"
    exit 1
fi

# Verify breakdown shows P1/P2/P3 categories
if grep -q "P1.*Blockers" "$REPORT_TEMPLATE" || grep -q "P1" "$REPORT_TEMPLATE"; then
    echo "PASS: Priority breakdown shows P1 category"
else
    echo "FAIL: Priority breakdown should show P1 category"
    exit 1
fi

# Test 10: Verify Action Items section in report
echo ""
echo "=== Phase 10: Action Items Section ==="

if grep -q "## Action Items" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has Action Items section"
else
    echo "FAIL: Report must have Action Items section"
    exit 1
fi

# Verify Must Fix, Should Fix, Nice to Fix subsections
if grep -q "### Must Fix" "$REPORT_TEMPLATE" || grep -q "Must Fix" "$REPORT_TEMPLATE"; then
    echo "PASS: Action Items has Must Fix subsection (P1 failures)"
else
    echo "FAIL: Action Items should have Must Fix subsection"
    exit 1
fi

if grep -q "### Should Fix" "$REPORT_TEMPLATE" || grep -q "Should Fix" "$REPORT_TEMPLATE"; then
    echo "PASS: Action Items has Should Fix subsection (P2 failures)"
else
    echo "FAIL: Action Items should have Should Fix subsection"
    exit 1
fi

if grep -q "### Nice to Fix" "$REPORT_TEMPLATE" || grep -q "Nice to Fix" "$REPORT_TEMPLATE"; then
    echo "PASS: Action Items has Nice to Fix subsection (P3 failures)"
else
    echo "FAIL: Action Items should have Nice to Fix subsection"
    exit 1
fi

# Test 11: Verify Bugs Found section (catching additional issues)
echo ""
echo "=== Phase 11: Bugs Found Section ==="

if grep -q "## Bugs Found" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has Bugs Found section"
else
    echo "FAIL: Report should have Bugs Found section for catching additional issues"
    exit 1
fi

# Verify bug tracking includes ID, Description, Severity, Location
if grep -q "BUG-" "$REPORT_TEMPLATE"; then
    echo "PASS: Bugs tracked with unique ID format"
else
    echo "FAIL: Bugs should be tracked with unique ID format"
    exit 1
fi

if grep -q "Severity" "$REPORT_TEMPLATE"; then
    echo "PASS: Bugs tracked with Severity"
else
    echo "FAIL: Bugs should be tracked with Severity"
    exit 1
fi

# Test 12: Verify Edge Cases Tested section
echo ""
echo "=== Phase 12: Edge Cases Tested ==="

if grep -q "## Edge Cases Tested" "$REPORT_TEMPLATE"; then
    echo "PASS: Report has Edge Cases Tested section"
else
    echo "FAIL: Report should have Edge Cases Tested section"
    exit 1
fi

# Test 13: Verify common pitfalls guidance
echo ""
echo "=== Phase 13: Common Pitfalls Guidance ==="

if grep -q "Common Pitfalls" "$CRITERIA_TEMPLATE" || grep -q "Pitfalls" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Criteria template has pitfalls guidance"
else
    echo "FAIL: Criteria template should have pitfalls guidance"
    exit 1
fi

# Verify Vague, Untestable, Subjective, Missing Edge Cases pitfalls
if grep -q "Vague Criteria" "$CRITERIA_TEMPLATE" || grep -q "Vague" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Vague Criteria pitfall documented"
else
    echo "FAIL: Vague Criteria pitfall should be documented"
    exit 1
fi

if grep -q "Untestable" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Untestable Criteria pitfall documented"
else
    echo "FAIL: Untestable Criteria pitfall should be documented"
    exit 1
fi

if grep -q "Subjective" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Subjective Criteria pitfall documented"
else
    echo "FAIL: Subjective Criteria pitfall should be documented"
    exit 1
fi

# Test 14: Verify quality checklist for criteria
echo ""
echo "=== Phase 14: Quality Checklist ==="

if grep -q "Quality Checklist" "$CRITERIA_TEMPLATE" || grep -q "Checklist for Criteria" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Quality checklist for criteria exists"
else
    echo "FAIL: Quality checklist for criteria should exist"
    exit 1
fi

# Verify SMART-like attributes: Specific, Measurable, Achievable, Relevant, Testable
if grep -q "Specific" "$CRITERIA_TEMPLATE" && grep -q "Measurable" "$CRITERIA_TEMPLATE" && grep -q "Testable" "$CRITERIA_TEMPLATE"; then
    echo "PASS: Quality checklist includes Specific, Measurable, Testable"
else
    echo "FAIL: Quality checklist should include Specific, Measurable, Testable"
    exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "========================================"
echo "PASS: Test Evaluation completed successfully"
echo "========================================"