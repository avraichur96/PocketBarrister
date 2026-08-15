# Phase 1 Legal Adjudication Matrix

Status: **In progress**

This matrix is the approval gate between the legacy dataset audit and creation of a canonical dataset. It starts from the 13 candidate families recommended by the audit; it does not treat any legacy output as legally correct merely because it is structured or cites an authority.

## Progress

| Measure | Complete |
|---|---:|
| Candidate families inventoried | 13/13 |
| Source lineage recorded | 13/13 |
| Known structural issues triaged | 13/13 |
| Controlling authorities verified | 0/13 |
| Expected legal states approved | 0/13 |
| Canonical admission decisions approved | 0/13 |

## Review states

- `Pending`: not yet adjudicated; legacy labels must not be reused as canonical truth.
- `Needs revision`: the family is useful, but its facts, authority, or expected state must change.
- `Approved`: authority, expected state, remedies, and required fact repairs have been reviewed together.
- `Excluded`: the family will not enter the first canonical dataset.

Only an `Approved` family may be used to author canonical training records. Approval applies to the reviewed family specification, not automatically to every cosmetic legacy row.

## Candidate matrix

| Candidate family | Legacy source | Proposed behavioral role | Known issue to resolve | Authority | Expected state | Status |
|---|---|---|---|---|---|---|
| `void_voidable` | Improved 100 | Capacity and void/voidable routing | Verify capacity, estoppel, and remedy distinctions | Pending | Pending | Pending |
| `consent` | Improved 100 | Coercion versus undue-influence routing | Correct statutory route, burden analysis, and voidability basis | Pending | Pending | Pending |
| `fraud_misrepresentation` | Improved 100 | Intent/recklessness boundary | Repair placeholders; review causation, diligence, and remedies | Pending | Pending | Pending |
| `minor_clear` | Improved 100 | Clear minority/capacity control | Reconcile restitution language across minor families | Pending | Pending | Pending |
| `mistake_edge` | Improved 100 | Essential-fact mistake boundary | Distinguish essential fact from quality or value | Pending | Pending | Pending |
| `supplier_duress` | Final 200 addition | Positive pressure/dependency case | Repair placeholders and five opposing-party collisions | Pending | Pending | Pending |
| `hard_negative_duress` | Final 200 addition | Negative duress boundary | Repair placeholders; verify doctrine for lawful pressure and alternatives | Pending | Pending | Pending |
| `hard_negative_influence` | Final 200 addition | Negative undue-influence boundary | Verify dominance and effect of genuinely independent advice | Pending | Pending | Pending |
| `hard_negative_void` | Final 200 addition | Temporary incapacity versus minority | Repair placeholders; verify status and consequences under incapacity | Pending | Pending | Pending |
| `ratification_void` | Final 200 addition | Void agreement cannot simply be affirmed | Review post-majority promise, consideration, and restitution | Pending | Pending | Pending |
| `voidable_ratification` | Final 200 addition | Informed affirmation of voidable agreement | Repair placeholders; define knowledge, free consent, and effect | Pending | Pending | Pending |
| `medical_influence` | Final 200 addition | Doctor/patient role binding and dominance | Repair placeholders; verify dominance and unfair-advantage findings | Pending | Pending | Pending |
| `legal_influence` | Final 200 addition | Lawyer/client role binding and advice | Verify fiduciary facts, comprehension, undervalue, and advice | Pending | Pending | Pending |

## Conditional candidate

`creditor_duress` remains outside the 13-family initial matrix. It may be added only after a preliminary review resolves whether its criminal-threat/additional-payment facts fit the experiment's doctrine and remedy scope.

## Required adjudication record

For each family, a review must eventually record:

1. Controlling statute and any case authority, with traceable sources.
2. Legally relevant party roles and facts.
3. Primary doctrine, rejected competing doctrines, and element findings.
4. Capacity or consent state and normalized agreement status.
5. Exercise or affirmation state, remedies, and downstream consequences.
6. Exact changes required before canonical examples are authored.
7. Reviewer, review date, notes, and final admission decision.

## Evidence boundary

The matrix may cite and quote legacy files for audit purposes, but all corrected specifications and future records belong outside `experiments/legacy_v0/`. The legacy snapshot remains immutable.
