## Spec-driven development

This repo uses spec-driven development for features that take more than one
sitting, touch several files, or have testable behavior. Small fixes skip it.
Full guide: https://github.com/cwarloe/lessons-learned/blob/main/SPEC_DRIVEN_DEVELOPMENT.md

- Specs live in `specs/<feature-slug>/` (requirements.md, design.md, tasks.md).
  Start a new one by copying `specs/_template/`.
- Before writing code for a feature, read its spec. If there is no spec and the
  change qualifies, write `requirements.md` first and wait for Charles to
  approve it, then design, then tasks.
- Work one task at a time; check it off in the commit that completes it.
- If the code needs to differ from the spec, update the spec first.
- A feature is done when every acceptance criterion maps to a passing test or a
  named manual check.
