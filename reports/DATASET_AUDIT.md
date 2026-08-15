# Phase 1 Dataset Audit

Audit date: 2026-08-15

Scope: `legal_reasoning_improved.json` (100 records) and `legal_reasoning_final.json` (200 records).

This report completes the Phase 1 dataset audit only. It does not modify source records, create splits, implement evaluation, or establish that either dataset trained the surviving legacy adapter.

## Executive recommendation

Do not use either primary dataset as-is.

Derive a smaller canonical dataset from the behavioral families in the 100-record set plus selected contrastive families from the added 100 records in the 200-set. The canonical unit of value should be a genuinely distinct template/behavior family, not a row with a different name, amount, age, or company.

The 100-set is the better semantic starting point because it is narrow and contract-focused, but it has only six underlying templates and 35 structurally defective records. The 200-set is exactly the 100-set followed by 100 additional records. Its added portion contributes 14 genuinely new generator/template families, including important negative and consequence cases, but it also adds further structural defects and legally complex claims.

Recommended initial behavioral target: 13 reviewed families, with one additional doctrine-competition family admitted only if legal review clears it. This is a family-level recommendation, not authorization to transform the data yet.

## Sources and method

Repository evidence inspected:

- The two primary JSON files.
- `create_improved_dataset.py` and `create_extended_dataset.py`.
- Earlier/later datasets only for lineage and format comparison.
- Existing dataset summaries as historical notes, not measured results.

Reproducible measurements are implemented in `analysis/audit_datasets.py`:

```powershell
python -B analysis/audit_datasets.py
```

The script is deterministic, uses only the Python standard library, writes its JSON report to standard output, and never writes to a source dataset.

Template-family grouping replaces case IDs, known generator person/company names, currency values, percentages, and numeric scalars, then groups identical normalized inputs. The resulting groups match the `for`-loop families in the surviving generators. This is stronger evidence than filename order, but it is still a provisional family assignment rather than a semantic embedding or legal judgment.

The entity audit detects known generated names/companies appearing only in the output and explicitly checks supplier cases for same-company role collisions. It does not fully resolve generic labels such as “seller,” “bank,” or “lender.”

### Immutable source measurements

| Dataset | Records | SHA-256 |
|---|---:|---|
| `legal_reasoning_improved.json` | 100 | `d8bb3cce5dd784f50ba7ff4f96ac1eaa71e7b1125f84e2f6ff76c664f5758234` |
| `legal_reasoning_final.json` | 200 | `12c462fc8ff46768fb5d4e517bd2984fcf095c90a1718455bd9cf9794150bd10` |

## Structural audit

### Comparative measurements

| Check | Improved 100 | Final 200 |
|---|---:|---:|
| Exact records | 100 | 200 |
| Top-level schema | `input`, `output`, `metadata` in 100/100 | Same in 200/200 |
| Complete metadata schema | 100/100 | 200/200 |
| Malformed JSON/record types | 0 | 0 |
| Missing required fields | 0 | 0 |
| Input/metadata case-ID mismatches | 0 | 0 |
| Duplicate case IDs | 0 | 0 |
| Exact duplicate inputs | 0 | 0 |
| Exact duplicate-output records beyond first copy | 28 | 37 |
| Exact duplicate-output groups | 14 | 23 |
| Largest exact duplicate-output group | 4 | 4 |
| Unique exact outputs | 72 | 163 |
| Surface-normalized input/template families | 6 | 20 |
| Cosmetic variant records beyond first family member | 94 | 180 |
| Surface-normalized output templates | 6 | 20 |
| Records with unexpanded `{placeholder}` text | 35 | 73 |
| Obvious opposing-role collisions | 0 | 5 |
| Missing/reordered/repeated output headings | 0 | 0 |
| Missing/repeated/non-terminal EOS marker | 0 | 0 |
| Records without parseable `FINDINGS` state | 0 | 0 |
| Unique `FINDINGS` keys | 36 | 84 |
| Known output-only generated entities | 0 | 0 |

“Structurally valid” and “structurally clean” are different labels here. All records are well-formed JSON with complete declared fields. However, at least 35/100 and 73/200 are structurally defective content because they contain literal generator placeholders. Five of the supplier records additionally collapse opposing parties into one company.

### Shared schema

Every record has:

```text
input
output
metadata
  case_id
  category
  difficulty
  sections
  jurisdiction
  token_count
```

Every output has exactly one of each section in the expected order:

```text
REASONING
FINDINGS
LEGAL_EFFECT
CONCLUSION
WHY ALTERNATIVES FAIL
<|end_of_text|>
```

The `token_count` metadata is a character-length estimate produced by `int((len(input) + len(output)) / 4.5)`, not a count from the Gemma tokenizer. It should not be treated as measured token length.

### Structural defects

#### Unexpanded placeholders

The following records contain literal values such as `{company_a}`, `{company_b}`, `{seller}`, `{buyer}`, or similar generator variables inside the output:

| Dataset | Affected category | Records affected |
|---|---|---:|
| Improved 100 | `duress` | 20/20 |
| Improved 100 | `fraud_misrepresentation` | 15/15 |
| Final 200 | Inherited two categories above | 35 |
| Final 200 | `supplier_duress` | 10/10 |
| Final 200 | `medical_influence` | 8/8 |
| Final 200 | `voidable_ratification` | 5/5 |
| Final 200 | `third_party_void` | 5/5 |
| Final 200 | `hard_negative_duress` | 5/5 |
| Final 200 | `hard_negative_void` | 5/5 |
| **Final 200 total** | | **73/200** |

These defects come from non-f-string `alternatives` arguments in the generators. The affected source records must not be promoted unchanged.

#### Supplier role collisions

`create_extended_dataset.py` independently samples supplier and buyer company names without enforcing distinctness. Five of ten saved supplier cases therefore describe a company threatening itself, depending on its own components, and seeking relief against itself:

- `IND-SUPPLIER-DURESS-7100`
- `IND-SUPPLIER-DURESS-7102`
- `IND-SUPPLIER-DURESS-7105`
- `IND-SUPPLIER-DURESS-7107`
- `IND-SUPPLIER-DURESS-7109`

This is a direct role-binding failure in the expected training answer, not merely awkward prose.

#### Generator reproducibility

Neither primary generator sets a random seed. Re-running it does not reproduce the saved JSON bytes. The generator also performs file writes at import/runtime rather than through a safe CLI.

## Improved 100 audit

### Distribution

| Category | Records | Difficulty | Normalized input templates | Normalized output/state templates |
|---|---:|---:|---:|---:|
| `void_voidable` | 20 | 2 | 1 | 1 |
| `consent` | 20 | 2 | 1 | 1 |
| `duress` | 20 | 2 | 1 | 1 |
| `fraud_misrepresentation` | 15 | 3 | 1 | 1 |
| `minor_clear` | 10 | 1 | 1 | 1 |
| `mistake_edge` | 15 | 4 | 1 | 1 |
| **Total** | **100** | 10 level 1; 60 level 2; 15 level 3; 15 level 4 | **6** | **6** |

All 100 rows belong to a repeated normalized input family. Once one representative of each family is counted, the remaining 94 rows change only generated surface values.

### Behavioral families

| Provisional family | Records | Behavior/state represented | Positive, negative, or boundary | Meaningful within-family outcome variation |
|---|---:|---|---|---|
| Minor: void vs voidable | 20 | Minority means no valid contract; void framework selected over voidable | Competing-doctrine positive | None |
| Parent/daughter consent | 20 | Coercion rejected; undue influence accepted; consent not free; transfer voidable | Competing-doctrine positive/negative | None |
| Supply modification duress | 20 | Duress accepted; no practical alternative; modification voidable | Positive | None |
| Fraud vs misrepresentation | 15 | Fraud rejected; innocent misrepresentation accepted; rescission but no damages | Boundary/competing doctrine | None |
| Minor with forged age | 10 | Minority defense; contract void; estoppel rejected | Clear positive | None |
| Painting authenticity mistake | 15 | Mutual essential-fact mistake; contract void; restitution | Boundary | None |

The dataset looks behaviorally balanced by row count, but it has only six fact structures and six expected state patterns. No category contains both a positive and negative example under its own family. The only contrast comes from competing labels embedded inside a single fixed answer.

### Existing state representation

All 100 outputs expose parseable key/value findings. Useful recurring keys include:

- `MINORITY_ESTABLISHED`
- `VALID_CONTRACT_FORMED`
- `COERCION_ESTABLISHED`
- `UNDUE_INFLUENCE_ESTABLISHED`
- `ECONOMIC_DURESS_ESTABLISHED`
- `PRACTICAL_ALTERNATIVE_EXISTS`
- `FREE_CONSENT`
- `CONTRACT_VOID`
- `CONTRACT_VOIDABLE`
- `MODIFICATION_VALID`
- `FRAUD_ESTABLISHED`
- `MISREPRESENTATION_ESTABLISHED`
- `RESCISSION_AVAILABLE`
- `DAMAGES_AVAILABLE`

This makes the 100-set a useful semantic seed despite its defects. It already expresses the local states needed by the research question.

## Final 200 audit

### Lineage

The first 100 records of `legal_reasoning_final.json` are exactly equal, in order and content, to all 100 records of `legal_reasoning_improved.json`. No improved record is absent or modified. The final 100 records add 14 categories/templates.

The 200-set is therefore an append-only expansion, not a corrected successor. Every defect in the 100-set remains present.

### Distribution

| Family group | Categories | Records |
|---|---|---:|
| Original improved families | 6 | 100 |
| Added duress contexts | employment, supplier, creditor | 30 |
| Added influence contexts | medical, legal, religious | 25 |
| Added void/voidable consequences | void ratification, voidable ratification, partial performance, third-party title | 20 |
| Added hard negatives | duress, influence, void/voidable | 15 |
| Added short EOS | direct minor answer | 10 |
| **Total** | **20 normalized families** | **200** |

Difficulty distribution: 20 level 1, 106 level 2, 59 level 3, and 15 level 4.

The added 100 rows contain 14 normalized input families and 14 normalized output/state templates. Eighty-six of those 100 rows are cosmetic repetitions beyond the first representative of their family.

## 100 → 200 delta analysis

### Present in both

The six original behavioral families are copied verbatim. The 200-set does not improve or repair their role binding, placeholders, authorities, or expected consequences.

### Genuinely new families in the added 100

Each added category below is a new generator/template family relative to the 100-set. “New family” does not mean legally reviewed or automatically recommended.

| Added family | Records | What it genuinely adds | Audit disposition |
|---|---:|---|---|
| `employment_duress` | 10 | Employment-role pressure and alleged lawful-act duress | Do not import initially: scope drift and legal theory needs authority-specific review. |
| `supplier_duress` | 10 | More appropriate price-increase modification and explicit supplier/buyer dependency | Use as the semantic replacement for the flawed base duress family after fixing 5 role collisions, placeholders, and legal provenance. |
| `creditor_duress` | 10 | Threat of criminal complaint used to extract payment beyond a debt; useful competing-doctrine scenario | Conditional import after review of coercion/undue-influence/economic-duress routing and remedies. |
| `medical_influence` | 8 | Doctor/patient roles, illness-based dominance, independent-advice factor | Import one reviewed family for role-binding coverage; Section 16 itself contains a medical-attendant illustration. |
| `legal_influence` | 8 | Lawyer/client fiduciary roles, undervalue, comprehension, independent advice | Import one reviewed family for professional-role binding and unfair-advantage analysis. |
| `religious_influence` | 9 | Psychological/religious authority and alleged false promise | Do not import initially: higher factual and legal sensitivity with little new state structure beyond other positive influence families. |
| `ratification_void` | 5 | Tests inability to ratify an agreement treated as void and the effect of later acknowledgment | Import only as a reviewed pair with `voidable_ratification`; legal consideration analysis needs correction/review. |
| `voidable_ratification` | 5 | Contrasts valid affirmation of a voidable contract with attempted ratification of a void agreement | Import as the matched contrast above; fix placeholders and verify knowledge/free-consent requirements. |
| `partial_performance_void` | 5 | Adds performance and restitution consequences after a minor transaction | Do not import initially: remedy statements are categorical and require detailed review under restitution/relief authorities. |
| `third_party_void` | 5 | Adds title transfer, innocent third party, and nemo-dat consequences | Exclude from initial scope: it introduces sale-of-goods/title law, has placeholders, and requires separate authority. |
| `hard_negative_duress` | 5 | Legitimate lawsuit threat, practical alternative, free consent, and a negative duress outcome | Import after placeholder repair; essential counterexample to the all-positive base duress family. |
| `hard_negative_influence` | 5 | Employer/assistant relationship without automatic dominance, plus independent advice | Import after legal review; essential negative influence outcome. |
| `hard_negative_void` | 5 | Temporary intoxication contrasted with minority; void rejected and voidable selected | Import conditionally after Section 12/consequence review and placeholder repair; valuable void/voidable contrast. |
| `short_direct` | 10 | Short-output/EOS behavior | Reserve for evaluation or a separately labeled response-length track; it does not teach the full structured output target. |

### Redundant expansion

Within every category in both datasets, the facts, issues, authorities, reasoning, findings, legal effect, and conclusion follow one generator template with one invariant expected outcome. Names, ages, amounts, percentages, or company names vary, but the legal decision boundary does not.

Measured redundancy:

- Improved 100: 6 templates and 94 cosmetic variants.
- Final 200: 20 templates and 180 cosmetic variants.
- Added half alone: 14 templates and 86 cosmetic variants.
- Normalized outputs collapse to the same counts as normalized inputs: 6 and 20 respectively.

Exact output duplication is lower because generated names and amounts sometimes differ, but it understates the template repetition.

## Template-family and leakage analysis

### Provisional family map

The category field maps one-to-one to the 20 observed normalized generator families. The largest are:

- `void_voidable`, `consent`, and `duress`: 20 rows each.
- `fraud_misrepresentation` and `mistake_edge`: 15 each.
- `minor_clear`, each added duress context, and `short_direct`: 10 each.
- Added influence families: 8–9 each.
- Consequence and hard-negative families: 5 each.

### Leakage risk

A random row split is not credible for this data. If members of one family occur in both training and evaluation, the model sees essentially the same facts, issues, principles, state keys, consequence chain, and conclusion during training. Only surface values differ.

The current datasets also cannot support a strong template-family-disjoint evaluation while preserving every category in both train and test: each behavioral category has only one underlying template family. Holding out a family means holding out the entire category/fact structure.

Before a future split, each target behavior needs multiple independently authored fact structures—not more outputs from the same generator loop. At least one family per behavior must be held entirely outside training.

No split is created in this audit.

## Legal-effect-chain analysis

### What is mechanically recoverable now

Every record contains a parseable `FINDINGS` block followed by natural-language `LEGAL_EFFECT` and `CONCLUSION` sections. This supports mechanical checks such as:

```text
role assignment
  → doctrine selected/rejected
  → normalized fact findings
  → consent/capacity state
  → agreement status
  → remedy/consequence
  → final conclusion
```

The datasets use 36 distinct finding keys in the 100-set and 84 in the 200-set. The expansion increases coverage but also introduces inconsistent names for similar states, including:

- `CONTRACT_VOIDABLE` versus `VOIDABLE`
- `CONTRACT_VOID` versus `ORIGINAL_CONTRACT_VOID`
- `VOID_AB_INITIO` versus `VOID_AB_INITIO_APPLIES`
- `CONTRACT_BINDING`, `MODIFICATION_VALID`, `PAYMENT_VALID`, `TRANSFER_VALID`, and `ENFORCEABLE`

These should be mapped into a controlled vocabulary before evaluation.

### Preliminary contradiction rubric

Future evaluation should test these layers separately:

1. **Role binding** — correct entity is assigned to each legally relevant role.
2. **Doctrine routing** — primary and rejected doctrines match the expected issue.
3. **Element findings** — each doctrine element has a normalized value and supporting fact reference.
4. **Capacity/consent state** — capacity and free-consent status agree with the findings.
5. **Agreement status** — use a controlled enum such as `valid`, `void`, `voidable`, `unenforceable`, or `requires_review`.
6. **Exercise/affirmation status** — distinguish having a right to avoid from actually avoiding, rescinding, affirming, or ratifying.
7. **Remedy/consequence** — represent enforcement, rescission, restitution, damages, recovery, and third-party effects separately.
8. **Final conclusion** — must agree with all applicable upstream states.

Example mechanical rules:

- `economic_duress = established` cannot coexist with `free_consent = yes` for the same assent without an explicit later affirmation event.
- `capacity = minor` and `agreement_status = void` cannot lead to ordinary contractual enforcement.
- `agreement_status = void` cannot be “ratified”; a later enforceable promise would require its own legal basis.
- `agreement_status = voidable` does not itself prove rescission; exercise of the avoidance right must be modeled.
- A negative primary doctrine must not produce the remedy tied solely to that doctrine.
- Role identities used in findings, remedies, and conclusions must exist in the facts and remain consistent.

The rubric should compare compact expected states and visible explanations. It should not require reproducing a hidden natural-language chain of thought.

## Legal correctness and provenance

### What repository evidence establishes

- Both datasets were synthetically generated by Python templates.
- All metadata says jurisdiction `India`.
- Metadata contains short section/case labels, but no source URLs, versions, pinpoints, provenance type, author, reviewer, review date, or review status.
- Zero records in either dataset contain a source URL.
- Zero records contain provenance/reviewer metadata.
- The generator comments describe desired teaching behavior; they are not legal validation.

Case/reference mentions by record:

| Reference | Improved 100 | Final 200 |
|---|---:|---:|
| `Mohori Bibee` | 30 | 55 |
| `Ranganayakamma` | 20 | 20 |
| `Inche Noriah` | 20 | 41 |
| `Derry v. Peek` | 15 | 15 |
| `Couturier v. Hastie` | 15 | 15 |
| `Bell v. Lever Brothers` | 15 | 15 |
| `Durga Prasad` | 0 | 5 |
| `Nemo dat` | 0 | 5 |

These are bare references, not traceable citations.

For audit orientation, the official [India Code entry](https://www.indiacode.nic.in/handle/123456789/12845?locale=en) and [official Contract Act PDF](https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf) confirm the relevant statutory structure: competency and sound mind in sections 10–12; free consent and its causes in sections 14–18; voidability under sections 19 and 19A; mutual mistake under section 20; and distinct restoration provisions in sections 64–65. These sources do not validate the dataset’s application of those provisions to every synthetic fact pattern.

### Review labels

At present:

- **Structurally valid JSON:** 100/100 and 200/200.
- **Structurally defective content:** at least 35/100 and 73/200.
- **Legally reviewed:** 0/100 and 0/200 based on repository evidence.
- **Legally unreviewed:** 100/100 and 200/200.
- **Candidate for manual review:** every family recommended for the canonical pool.

### Legally suspicious or internally questionable families

“Suspicious” here means the output needs authority-specific review; it does not declare a final legal answer.

1. **Base duress (`IND-DURESS-3000`–`3019`)** — the supplier threatens breach unless the dependent buyer *reduces* the price, reversing the ordinary economic incentive. All 20 cases then reason from this same questionable fact direction.
2. **Economic-duress families generally** — “economic duress” is not itself one of the named free-consent categories in sections 14–18. The intended mapping to Indian doctrine and remedies requires case-law authority rather than an uncited imported common-law test.
3. **Consent family** — the records treat the relationship and presumption categorically and refer to voidability under section 16. Section 16 defines undue influence; section 19A addresses the power to set aside a contract induced by it. The family needs more precise authority and burden analysis.
4. **Fraud/misrepresentation family** — the output always resolves the same ambiguous verification facts as likely innocent misrepresentation and states a fixed remedy. Section 19 contains causation and ordinary-diligence qualifications that need fact-specific review.
5. **Mistake family** — every original-versus-reproduction case is labeled likely void as an identity/nature mistake. Section 20 expressly excludes an erroneous opinion as to value; whether authenticity is an essential fact rather than quality/value cannot be assumed across all cases.
6. **Minor/restitution families** — remedies vary across the dataset: “limited/fact-dependent restitution,” “no remedy,” mandatory mutual restitution, tort recovery, and third-party recovery all appear. Sections 64, 65, 68, and 70 and the `Mohori Bibee` line of cases require more careful separation. A case-law mirror discussing `Mohori Bibee` also shows that restitution depended on statutory basis and facts rather than a single blanket rule: [Limbaji Ravji Hajare v. Rahi Ravji Hajare](https://indiankanoon.org/docfragment/1160793/).
7. **Ratification void** — the generator states broadly that past consideration is no consideration and invokes `Durga Prasad`. Section 25 contains exceptions involving past voluntary acts and written promises for limitation-barred debts; the actual post-majority promise analysis needs review rather than a categorical slogan.
8. **Hard-negative intoxication** — section 12 tests whether the person could understand and form a rational judgment at the time. The dataset’s fixed “voidable, not void” consequence requires supporting authority beyond the statutory capacity test.
9. **Third-party title** — the family invokes nemo dat and title consequences without citing the governing sale-of-goods authority; this expands beyond the narrow initial experiment.
10. **Cross-family inconsistency** — `short_direct` says no remedy is available, while other minor families preserve limited restitution or recovery. Even if context could reconcile them, the state schema does not express the factual conditions that would do so.
11. **Independent advice** — the influence families often treat advice as mechanically conclusive. The cases invoking `Inche Noriah` need nuanced review; a case-law mirror notes that advice must be informed and genuinely independent rather than merely present: [Mahboob Khan v. Hakim Abdul Rahim](https://indiankanoon.org/doc/269316/).

## Canonical dataset recommendation

### Decision

Derive a new canonical dataset from selected, repaired, and legally reviewed families. Do not declare either source file canonical as-is.

Use `legal_reasoning_improved.json` as the semantic lineage/base, not as a 100-row training artifact. Preserve five of its six core behaviors provisionally and replace its flawed positive-duress template with the better-directed supplier-duress semantics from the 200-set.

### Recommended family-level source pool

#### Preserve from the 100-set, subject to legal review and structural repair

1. `void_voidable` — core capacity and competing-status behavior.
2. `consent` — coercion versus undue-influence routing.
3. `fraud_misrepresentation` — intent/recklessness doctrine boundary.
4. `minor_clear` — simple capacity control case.
5. `mistake_edge` — difficult essential-fact boundary, retained only if review produces a defensible rubric.

Do not preserve the current `duress` facts as canonical; replace the reversed price-reduction scenario.

#### Import from the added 100 because each adds required coverage

1. `supplier_duress` — repaired positive duress/dependency case and direct replacement for the flawed base scenario.
2. `hard_negative_duress` — establishes a negative duress boundary with legitimate pressure and a practical alternative.
3. `hard_negative_influence` — establishes a negative undue-influence boundary and tests independent advice.
4. `hard_negative_void` — contrasts temporary capacity questions with minority and forces void/voidable routing.
5. `ratification_void` — adds the downstream rule that a void agreement cannot simply be affirmed as though voidable.
6. `voidable_ratification` — provides the matched contrast showing how later informed affirmation can affect a voidable contract.
7. `medical_influence` — adds illness, doctor/patient role binding, dominance, and unfair-advantage facts recognized by the structure of section 16.
8. `legal_influence` — adds lawyer/client role binding, comprehension, undervalue, and independent-advice factors.

#### Conditional import

- `creditor_duress` — adds a valuable criminal-threat/additional-payment fact structure, but import it only after doctrine routing and remedies are legally adjudicated.

#### Exclude from the initial canonical training pool

- `employment_duress` — employment scope drift and unresolved lawful-act theory.
- `religious_influence` — sensitive factual claims with little new state structure beyond the professional influence families.
- `partial_performance_void` — restitution complexity should not be trained before legal review establishes a precise state model.
- `third_party_void` — sale/title scope expansion and missing governing authority.
- `short_direct` — reserve for EOS/response-length evaluation rather than mixing it into full structured-supervision training.

This yields 13 provisional target families, or 14 if the creditor family passes review. It does not imply retaining every cosmetic row. Phase 2 should decide the minimum number of independently authored fact structures per behavior after review; simply sampling several existing rows from one family does not create template diversity.

## Proposed canonical schema

The future schema should separate provenance, facts, expected state, and rendered training text:

```yaml
sample_id: PB-ICA-0001
dataset_version: 1.0.0
category: free_consent
behavior_family: undue_influence_negative
template_family: independent-advice-employment-gift-v1
variant_id: null
jurisdiction: India

facts:
  text: "..."
issues:
  - "..."

authorities:
  - type: statute
    citation: Indian Contract Act, 1872, section 16
    source_url: "..."
    source_version_or_access_date: "..."

provenance:
  type: synthetic_template | manually_authored | adapted
  generator: null
  parent_sample_id: null
  seed: null

difficulty:
  level: 3
  rationale: "Competing doctrine and negative relationship presumption"

review:
  structural_status: passed | failed
  legal_status: unreviewed | suspicious | reviewed
  reviewer: null
  reviewed_at: null
  notes: []

expected_state:
  roles:
    - entity: "..."
      role: alleged_influencer
    - entity: "..."
      role: affected_party
  primary_doctrine: undue_influence
  doctrine_applies: false
  rejected_doctrines:
    - doctrine: coercion
      reason_code: no_forbidden_or_unlawful_threat
  fact_findings:
    dominant_position: false
    unfair_advantage: false
    independent_advice: true
  consent_status: free
  agreement_status: valid
  exercise_status: not_applicable
  legal_effects:
    enforceable: true
    rescission_available: false
    restitution_status: not_applicable
    damages_status: not_applicable
  final_conclusion:
    label: agreement_valid
    text: "..."

rendered:
  instruction: "..."
  input: "..."
  output: "..."
```

The schema should use controlled enums for core states, allow family-specific findings, and preserve a concise human-readable explanation. `template_family` must identify the underlying fact structure, while `variant_id` is only for legitimate surface variants. Review status must never be inferred from the presence of a statute or case name.

## Remaining uncertainties

- No repository evidence identifies a legally qualified reviewer or confirms that any record was manually validated.
- The exact historical authoring process within each template is not recorded beyond generator code and comments.
- The current files cannot establish which dataset version, if any, trained the legacy adapter.
- File timestamps help reconstruct order but do not prove experimental intent or data lineage beyond the exact 100-record append relationship measured here.
- Template normalization can identify generator-level repetition but cannot decide whether a fact difference is legally material; that requires manual review.
- The repository does not contain raw base or LoRA predictions needed to verify remembered behavioral improvements.
- Economic-duress treatment, minor restitution, ratification, mistake/authenticity, and third-party-title consequences remain legally unresolved for canonical labeling.

## Single recommended next action

Perform a family-level legal adjudication pass on the 13 recommended template families using an explicit authority-and-state matrix. For each family, record the controlling authority, correct doctrine, normalized findings, agreement status, remedies, and any fact changes required. Do not generate variants or create a split until that matrix is approved.

