# Template Generator Prompt

> Use this prompt template to generate custom document templates for the harness framework.

---

## Input Parameters

When generating a custom template, provide the following context:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `template_name` | Unique identifier for the template (lowercase, hyphen-separated) | Yes |
| `template_purpose` | What this template is used for | Yes |
| `use_cases` | When this template should be used | Yes |
| `required_sections` | Sections that must be filled in | Yes |
| `optional_sections` | Sections that can be skipped | No |
| `example_values` | Sample filled-in values | Yes |
| `output_format` | Where the template is saved/used | No |

---

## Prompt Template

```
You are generating a new document template for the harness framework.

## Template to Generate

- **Name**: {template_name}
- **Purpose**: {template_purpose}
- **Use Cases**: {use_cases}
- **Required Sections**: {required_sections}
- **Optional Sections**: {optional_sections}
- **Example Values**: {example_values}

## Your Task

Create a complete template following the harness framework conventions.

## Template Structure

1. **Header Section**:
   - Title
   - Metadata (version, date, status)
   - Brief description/instructions

2. **Body Sections**:
   - Clear section headers
   - Instructions for each section
   - Placeholder text
   - Format examples

3. **Footer Section**:
   - Change log
   - Approval section
   - References

## Design Principles

1. **Clear Instructions**: Users know what to fill in
2. **Obvious Placeholders**: `[PLACEHOLDER]` format is clear
3. **Examples Provided**: Show what good looks like
4. **Logical Flow**: Sections follow natural order
5. **Complete but Concise**: Not overwhelming

Generate the template now.
```

---

## Output Format

The generated template should follow this structure:

```markdown
# {Template Title}

> {Brief description of what this template is for}
> **Usage**: {When and how to use this template}

---

## {Section 1}

{Instructions for this section}

- **{Field 1}**: {Description}
- **{Field 2}**: {Description}

{Example or placeholder}
```

{Section 1 Content Placeholder}
```

---

## {Section 2}

{Instructions for this section}

### {Subsection 2.1}

{Instructions}

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| {Value} | {Value} | {Value} |

---

## Optional Sections

> These sections can be included when relevant

### {Optional Section 1}

{Instructions}

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {DATE} | {Author} | Initial version |

---

## References

- {Reference 1}
- {Reference 2}
```

---

## Quality Checklist

Before finalizing the template, verify:

- [ ] **Purpose Clear**: Users understand what this is for
- [ ] **Instructions Provided**: Each section has guidance
- [ ] **Placeholders Obvious**: `[PLACEHOLDER]` format is clear
- [ ] **Examples Shown**: Users see what good looks like
- [ ] **Required vs Optional**: Clear distinction
- [ ] **Logical Flow**: Sections in natural order
- [ ] **Not Overwhelming**: Not too long or complex
- [ ] **Reusable**: Can be used multiple times
- [ ] **Consistent Format**: Follows harness conventions

---

## Template Types Reference

### Design Templates
Architecture decisions, design docs, technical specs

### Sprint Templates
Sprint contracts, feature plans, task breakdowns

### Evaluation Templates
Evaluation reports, criteria, checklists

### Documentation Templates
API docs, README, contributing guides

### Process Templates
Incident reports, change requests, retrospectives

---

## Examples

### Example 1: Technical Design Template

**Input:**
```
template_name: technical-design
template_purpose: Document technical design decisions for new features
use_cases: When proposing a new feature, making architectural changes, or documenting design decisions
required_sections: Overview, Problem Statement, Proposed Solution, Alternatives, Impact, Risks
optional_sections: Implementation Notes, Testing Strategy, Rollout Plan
example_values: Sample design for user authentication feature
```

**Output:**
```markdown
# Technical Design: [Feature Name]

> Use this template to document technical design decisions before implementation.
> **Usage**: Create before starting significant development work

---

## Overview

> Brief summary of what this design addresses

- **Feature**: [Feature name]
- **Author**: [Your name]
- **Date**: [YYYY-MM-DD]
- **Status**: DRAFT | IN_REVIEW | APPROVED | IMPLEMENTED

**Summary**: [2-3 sentence description of the feature or change]

---

## Problem Statement

> What problem are we solving? Why is this needed?

**Current State**: [Describe how things work now]

**Pain Points**:
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

**Goals**:
- [Goal 1]
- [Goal 2]

**Non-Goals**:
- [Explicitly out of scope 1]
- [Explicitly out of scope 2]

---

## Proposed Solution

> Describe the solution in detail

### Architecture Overview

```
[Diagram or description of the architecture]
```

### Components

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| [Component 1] | [What it does] | [Tech used] |
| [Component 2] | [What it does] | [Tech used] |

### Data Model

```sql
-- New tables or schema changes
CREATE TABLE [table_name] (
    [column_definitions]
);
```

### API Changes

```yaml
# New or modified endpoints
[Method] [Path]
  Request: [Schema]
  Response: [Schema]
```

### Sequence Flow

```
[Step 1] -> [Step 2] -> [Step 3]
```

---

## Alternatives Considered

> What other approaches were evaluated?

### Alternative 1: [Name]

**Description**: [Brief description]

**Pros**:
- [Pro 1]
- [Pro 2]

**Cons**:
- [Con 1]
- [Con 2]

**Why Rejected**: [Reason for not choosing this approach]

### Alternative 2: [Name]

**Description**: [Brief description]

**Pros**:
- [Pro 1]

**Cons**:
- [Con 1]

**Why Rejected**: [Reason]

---

## Impact Analysis

### Performance Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [Metric 1] | [Value] | [Value] | [+/-] |
| [Metric 2] | [Value] | [Value] | [+/-] |

### Security Considerations

- [Security consideration 1]
- [Security consideration 2]

### Backward Compatibility

- [Compatibility impact]
- [Migration strategy if needed]

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [How to mitigate] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [How to mitigate] |

---

## Implementation Notes

> Optional: Specific implementation guidance

- [Implementation note 1]
- [Implementation note 2]

---

## Testing Strategy

> Optional: How will this be tested?

### Unit Tests

- [Test case 1]
- [Test case 2]

### Integration Tests

- [Test scenario 1]
- [Test scenario 2]

### Manual Testing

- [Test procedure 1]
- [Test procedure 2]

---

## Rollout Plan

> Optional: How will this be deployed?

### Phase 1: [Name]

- [ ] [Step 1]
- [ ] [Step 2]

### Phase 2: [Name]

- [ ] [Step 1]
- [ ] [Step 2]

### Rollback Plan

1. [Rollback step 1]
2. [Rollback step 2]

---

## Approvals

| Role | Name | Status | Date |
|------|------|--------|------|
| Tech Lead | [Name] | PENDING | |
| Architect | [Name] | PENDING | |
| Security | [Name] | PENDING | |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [Author] | Initial version |

---

## References

- [Link to related document 1]
- [Link to related document 2]
```

---

### Example 2: Incident Report Template

**Input:**
```
template_name: incident-report
template_purpose: Document production incidents for post-mortem analysis
use_cases: After any production incident, outage, or significant bug
required_sections: Summary, Timeline, Impact, Root Cause, Resolution
optional_sections: Timeline Details, Customer Communication, Follow-ups
example_values: Sample incident for API timeout issue
```

**Output:**
```markdown
# Incident Report: [Incident Title]

> Use this template to document and analyze production incidents.
> **Usage**: Create within 24 hours of incident resolution

---

## Summary

> High-level overview for stakeholders

- **Incident ID**: INC-[YYYYMMDD]-[###]
- **Severity**: SEV1 | SEV2 | SEV3
- **Status**: INVESTIGATING | IDENTIFIED | MONITORING | RESOLVED
- **Duration**: [Start Time] - [End Time] ([Total Duration])
- **Author**: [Your name]
- **Date**: [YYYY-MM-DD]

**Brief Description**: [1-2 sentences describing what happened]

**Services Affected**: [List affected services]

**Customer Impact**: [Brief description of customer impact]

---

## Timeline

> All times in UTC

| Time | Event | Actor |
|------|-------|-------|
| [HH:MM] | [Event description] | [System/Person] |
| [HH:MM] | [Event description] | [System/Person] |
| [HH:MM] | [Event description] | [System/Person] |

### Detailed Timeline

**[HH:MM] - Alert Triggered**
- [Detailed description]
- [Actions taken]

**[HH:MM] - Investigation Started**
- [Detailed description]
- [Actions taken]

**[HH:MM] - Root Cause Identified**
- [Detailed description]
- [Actions taken]

**[HH:MM] - Fix Deployed**
- [Detailed description]
- [Actions taken]

**[HH:MM] - Incident Resolved**
- [Detailed description]
- [Actions taken]

---

## Impact

### Customer Impact

- **Users Affected**: [Number or percentage]
- **Features Impacted**: [List features]
- **Data Impact**: [Any data loss or corruption]

### Business Impact

- **Revenue Impact**: [Estimate if applicable]
- **SLA Impact**: [Any SLA breaches]
- **Reputation Impact**: [Social media, support tickets]

### Technical Impact

- **Systems Affected**: [List systems]
- **Dependencies**: [Downstream effects]
- **Recovery Time**: [Time to full recovery]

---

## Root Cause Analysis

### Immediate Cause

[What directly caused the incident]

### Underlying Cause

[Why the immediate cause occurred - the deeper issue]

### Contributing Factors

1. [Contributing factor 1]
2. [Contributing factor 2]
3. [Contributing factor 3]

### Detection

- **How Detected**: [Alert, customer report, internal monitoring]
- **Time to Detect**: [Duration from issue start to detection]
- **Detection Gap**: [Why it wasn't detected sooner]

---

## Resolution

### Immediate Fix

[What was done to resolve the incident]

```[language]
// Code or configuration change
[Fix details]
```

### Long-term Solution

[Permanent fix to prevent recurrence]

### Verification

How was the fix verified:
- [ ] Monitoring confirmed recovery
- [ ] Customer reports resolved
- [ ] Automated tests passing
- [ ] Manual verification completed

---

## Customer Communication

> Optional: For customer-facing incidents

### Internal Communication

- **Slack Update**: [Channel] at [Time]
- **Email Update**: [Recipients] at [Time]

### External Communication

| Channel | Time | Message |
|---------|------|---------|
| Status Page | [Time] | [Summary] |
| Twitter | [Time] | [Summary] |
| Email | [Time] | [Summary] |

---

## Follow-up Actions

| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| [Action 1] | [Owner] | P1/P2/P3 | [Date] | TODO |
| [Action 2] | [Owner] | P1/P2/P3 | [Date] | TODO |
| [Action 3] | [Owner] | P1/P2/P3 | [Date] | TODO |

---

## Lessons Learned

### What Went Well

- [Positive aspect 1]
- [Positive aspect 2]

### What Could Be Improved

- [Area for improvement 1]
- [Area for improvement 2]

### Process Improvements

1. [Improvement 1]
2. [Improvement 2]

---

## Appendix

### Logs and Evidence

```
[Relevant log snippets]
```

### Screenshots

[Links to screenshots or diagrams]

### Related Documents

- [Link to runbook]
- [Link to architecture doc]
- [Link to previous similar incident]

---

## Sign-off

| Role | Name | Date |
|------|------|------|
| Incident Commander | [Name] | [Date] |
| Tech Lead | [Name] | [Date] |
| Manager | [Name] | [Date] |

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [Author] | Initial report |
```

---

## Anti-Patterns to Avoid

1. **Vague Placeholders**: `[stuff]` is not helpful
2. **No Instructions**: Users don't know what to fill in
3. **Too Many Sections**: Overwhelming templates go unused
4. **No Examples**: Users can't see what good looks like
5. **Missing Purpose**: Why use this template?

---

## Integration Notes

After generating a template:

1. Save to `.claude/docs/templates/{template_name}.md`
2. Register in the project's template index
3. Add to relevant skill references
4. Document usage in project docs
5. Include in onboarding materials