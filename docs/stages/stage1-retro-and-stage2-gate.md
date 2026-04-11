# Stage 1 Retro & Stage 2 Start Gate

> Post-Stage 1 retrospective and pre-conditions for entering Stage 2.

---

## Root Causes

| Issue | Root Cause | Trigger Point |
|-------|------------|---------------|
| GitHub CLI auth failure | Token expiration without refresh mechanism; no pre-flight auth check | Attempted PR/issue creation |
| Wrong directory/repo assumption | Skipped repo identity verification; assumed workspace == target repo | Initial session entry |
| Local main branch pollution | Continuous development on main without stage boundaries | Needed clean branch for Stage 1 isolation |
| PR checks failing (non-Stage-1) | CI baseline issues (missing pytest, missing schema files) separated from business logic | PR created before CI health check |

---

## Preventive Rules

### Pre-Flight Checklist (Every Session)
```bash
gh auth status                    # Verify GitHub auth
git remote -v                     # Confirm target repo
git branch --show-current         # Confirm current branch
git log origin/main..HEAD --oneline | wc -l   # Check unpushed commits
```

### Branch Discipline
- **Never develop on main** — Each stage starts from `origin/main` on isolated branch
- **Branch naming**: `pr/stage{N}-{short-description}`
- **Freeze after push** — No new features after branch push; only review feedback

### Stage Deliverables (Mandatory)
- [ ] `docs/stages/stage{N}-summary.md` — Scope boundary document
- [ ] Targeted tests pass: `pytest tests/... -q`
- [ ] Clean diff: `git diff --stat origin/main` reviewed for unrelated files
- [ ] CI baseline known: If CI broken, document in separate issue before PR

### Agent Execution Gate
Before any git/GitHub operation, confirm:
1. **Path**: `pwd` + `git rev-parse --show-toplevel`
2. **Remote**: `git remote -v` matches target
3. **Branch**: Not on `main`
4. **Auth**: `gh auth status` valid

---

## Open Follow-ups

### Must Record
| Issue | Location | Status |
|-------|----------|--------|
| CI/test missing pytest | Issue #2 | Recorded and root-caused |
| Schema Validation missing files | Issue #2 | Recorded and root-caused |
| gh CLI token refresh process | This document | Establish periodic verification |

### Should Resolve Before Stage 2
| Issue | Suggested Fix | Priority |
|-------|---------------|----------|
| Fix CI/test workflow | Add `pip install pytest` to `.github/workflows/ci.yml` | High |
| Fix Schema Validation | Commit missing schema files or update validation script | High |

### Can Defer
| Issue | Rationale | When |
|-------|-----------|------|
| Full CI matrix (multi-Python) | Single version sufficient for Stage 1-2 | Stage 3+ |
| Schema file versioning | No frequent changes expected | When schema changes |
| Automated gh auth refresh | Manual check cost acceptable | Team scaling |

---

## Stage 2 Start Gate

**Do not start Stage 2 implementation until:**

1. ✅ PR #1 merged or review feedback received and triaged
2. ✅ Issue #2 (CI baseline) recorded and root-caused (resolution can be parallel)
3. ✅ Local `main` synced with `origin/main`
4. ✅ New Stage 2 branch cut from clean `origin/main`: `git checkout -b pr/stage2-xxx origin/main`
5. ✅ **Stage 2 theme frozen** and `docs/stages/stage2-scope.md` exists (scope only, no implementation)

**Stage 2 Scope Definition Requirements:**
- One-paragraph theme statement
- Explicit in-scope / out-of-scope boundaries
- Success criteria (testable)
- Suggested timeline (can be rough)

---

*Document created: 2026-03-19*  
*Stage 1 status: Closed*  
*Stage 2 status: Awaiting scope definition*
