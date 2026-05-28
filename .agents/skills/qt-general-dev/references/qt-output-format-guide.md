# Qt Output Format Guide

Use this reference when the user asks for a structured design, review, or debugging answer.

## Architecture Or Module Design

1. Goal
2. Assumptions
3. Recommended Qt approach
4. Module/class design
5. Directory structure
6. Key signal/slot flow
7. Core implementation
8. CMake/resource changes
9. Risks and extension points

## Code Review

Lead with findings:

```markdown
## Findings

- [High][Confirmed] path/file.cpp:42 - Short title.
  Evidence, trigger, consequence, and minimal fix.

## Open Questions

## Suggested Fixes

## Summary
```

Use severity only when it helps prioritization:

- Critical: crash, data race, deadlock, data corruption, severe leak, security issue.
- High: likely production bug, UI freeze, wrong thread ownership, failed cleanup, broken build.
- Medium: fragile lifetime, missing error handling, risky copy cost, strong coupling, duplicated logic.
- Low: local cleanup, small inconsistency, minor inefficiency.

## Debugging Or Crash Analysis

1. Symptom summary
2. Known facts
3. Failure classification
4. Ranked hypotheses
5. Verification steps
6. Minimal fixes
7. Instrumentation/prevention

Separate facts from assumptions. Do not claim a root cause without a supporting log, stack frame, code path, or reproduction clue.
