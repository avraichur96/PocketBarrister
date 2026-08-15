"""
Improved Legal Reasoning Dataset with FINDINGS + LEGAL_EFFECT
Teaches legal consequence propagation, not just doctrine explanation
"""

import json
import random

MALE_NAMES = ["Raj", "Amit", "Vikram", "Arjun", "Rohan", "Karan", "Aditya", "Sanjay", "Rahul", "Pradeep"]
FEMALE_NAMES = ["Priya", "Anjali", "Neha", "Pooja", "Kavita", "Sunita", "Meera", "Ritu", "Divya", "Sneha"]

def get_name(gender='male'):
    return random.choice(MALE_NAMES if gender == 'male' else FEMALE_NAMES)

def get_amount():
    return random.choice(["₹5 lakh", "₹10 lakh", "₹25 lakh", "₹50 lakh", "₹1 crore", "₹2 crore"])

def make_sample(case_id, facts, issues, principles, reasoning, findings, legal_effect, 
                conclusion, alternatives, category, difficulty, sections):
    """
    New format with FINDINGS and LEGAL_EFFECT for consequence propagation
    Shorter, sharper samples optimized for Gemma-2B
    """
    
    input_text = f"""CASE_ID: {case_id}

FACTS:
{facts}

ISSUES:
{issues}

APPLICABLE PRINCIPLES:
{principles}"""
    
    output_text = f"""REASONING:
{reasoning}

FINDINGS:
{findings}

LEGAL_EFFECT:
{legal_effect}

CONCLUSION:
{conclusion}

WHY ALTERNATIVES FAIL:
{alternatives}<|end_of_text|>"""
    
    return {
        "input": input_text,
        "output": output_text,
        "metadata": {
            "case_id": case_id,
            "category": category,
            "difficulty": difficulty,
            "sections": sections,
            "jurisdiction": "India",
            "token_count": int((len(input_text) + len(output_text)) / 4.5)
        }
    }

samples = []

print("Generating improved dataset with FINDINGS + LEGAL_EFFECT...")
print("="*80)

# ============================================================================
# LEVEL 2 - Void vs Voidable (Competing Doctrines)
# ============================================================================

print("Level 2: Void vs Voidable (20 samples)...")

for i in range(20):
    name = get_name('male')
    amount = get_amount()
    age = random.choice([16, 17])
    
    samples.append(make_sample(
        case_id=f"IND-VOID-{1000+i}",
        
        facts=f"""{name}, aged {age}, purchases goods worth {amount}. Seller unaware of age. No fraud by {name}. After delivery, {name} refuses payment claiming minority. Seller argues contract should be voidable (allowing restitution) not void (no remedy).""",
        
        issues="""- Void ab initio or voidable?
- Does seller's ignorance affect status?
- Restitution available?""",
        
        principles="""- Section 11: Minor incompetent
- Mohori Bibee (1903): Minor's contract void ab initio
- Section 19: Voidable contracts
- Restitution: Limited equitable recovery may be considered, but no contractual price claim""",
        
        reasoning=f"""Step 1 — Competing Frameworks:
(a) Void ab initio (Mohori Bibee) → no contract exists
(b) Voidable (Section 19) → contract exists until avoided

Step 2 — Fact Mapping:
- {name} is {age} → minor under Section 11
- No fraud by minor
- Seller ignorant of age
- Goods delivered

Step 3 — Doctrine Selection:
Voidable applies when: valid contract + vitiated consent
Void applies when: no valid contract (incompetent party)
Here: No competent party → no valid contract formed""",
        
        findings=f"""- MINORITY_ESTABLISHED: Yes
- CONTRACTUAL_CAPACITY: No
- VALID_CONTRACT_FORMED: No
- VOIDABLE_FRAMEWORK_APPLIES: No
- VOID_AB_INITIO_APPLIES: Yes
- CONTRACTUAL_REMEDY_AVAILABLE: No
- RESTITUTION_AVAILABLE: Limited / fact-dependent""",
        
        legal_effect=f"""Because VALID_CONTRACT_FORMED = No, voidable doctrine cannot apply. Voidable requires valid contract first. Because VOID_AB_INITIO_APPLIES = Yes and CONTRACTUAL_REMEDY_AVAILABLE = No, seller cannot recover the price. Any restitution is limited and fact-dependent, such as recovery of identifiable goods, and does not validate the contract.""",
        
        conclusion=f"""Contract VOID AB INITIO. Seller cannot enforce payment. Limited equitable restitution may be available (e.g., identifiable goods recovery) but does not validate contract.""",
        
        alternatives="""- Voidable doctrine → REJECTED: Requires valid contract. Here no valid contract due to incompetency.
- Estoppel → REJECTED: Mohori Bibee bars estoppel for void contracts.
- Seller's ignorance → REJECTED: Competency is objective, not dependent on knowledge.""",
        
        category="void_voidable",
        difficulty=2,
        sections=["Section 11", "Section 19", "Section 65"]
    ))

# ============================================================================
# LEVEL 2 - Coercion vs Undue Influence
# ============================================================================

print("Level 2: Coercion vs Undue Influence (20 samples)...")

for i in range(20):
    father = get_name('male')
    daughter = get_name('female')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-CONSENT-{2000+i}",
        
        facts=f"""{father} threatens to disinherit {daughter} unless she transfers property worth {amount} to her brother. {daughter}, financially dependent, agrees. Later seeks to void claiming coercion (Section 15) or undue influence (Section 16).""",
        
        issues="""- Coercion under Section 15?
- Undue influence under Section 16?
- Which doctrine applies?""",
        
        principles="""- Section 15: Coercion = threat of IPC-forbidden act
- Section 16: Undue influence = dominant position + unfair advantage
- Ranganayakamma (1889): Threat must harm another
- Inche Noriah (1929): Fiduciary relationship creates presumption""",
        
        reasoning=f"""Step 1 — Competing Frameworks:
(a) Coercion (Section 15) → unlawful threat
(b) Undue Influence (Section 16) → relationship exploitation

Step 2 — Testing Coercion:
Requires: Threat of IPC-forbidden act
Here: Disinheritance is LAWFUL (testamentary freedom)
Cutting support is LAWFUL (no duty to support adult)
Ranganayakamma test: Threat must be unlawful
Result: Section 15 NOT satisfied

Step 3 — Testing Undue Influence:
Requires: Dominant position + unfair advantage
Here: Father-daughter (fiduciary per Inche Noriah)
Financial dependence = dominant position
Transfer without consideration = unfair advantage
Result: Section 16 satisfied""",
        
        findings=f"""- COERCION_ESTABLISHED: No (lawful threats)
- UNDUE_INFLUENCE_ESTABLISHED: Yes
- FIDUCIARY_RELATIONSHIP: Yes
- DOMINANT_POSITION: Yes
- UNFAIR_ADVANTAGE: Yes
- FREE_CONSENT: No
- CONTRACT_VOIDABLE: Yes""",
        
        legal_effect=f"""Because COERCION_ESTABLISHED = No, Section 15 does not apply. Because UNDUE_INFLUENCE_ESTABLISHED = Yes and FREE_CONSENT = No, the transfer is voidable under Section 16. Because FIDUCIARY_RELATIONSHIP = Yes, Inche Noriah presumption applies and burden shifts to {father}.""",
        
        conclusion=f"""Transfer VOIDABLE under Section 16 (undue influence), NOT Section 15 (coercion). {daughter} may rescind. Lawful pressure within fiduciary relationship = undue influence.""",
        
        alternatives="""- Coercion (Section 15) → REJECTED: Disinheritance and cutting support are lawful acts. Section 15 requires IPC-forbidden threat.
- Free consent → REJECTED: Inche Noriah presumption applies in fiduciary relationships. Financial dependence + no independent advice = vitiated consent.
- Commercial pressure → REJECTED: Family relationship, not commercial. Fiduciary duties apply.""",
        
        category="consent",
        difficulty=2,
        sections=["Section 15", "Section 16"]
    ))

# ============================================================================
# LEVEL 2 - Economic Duress (NEW - addresses test failure)
# ============================================================================

print("Level 2: Economic Duress (20 samples)...")

for i in range(20):
    company_a = f"Company {chr(65+i%5)}"  # A, B, C, D, E
    company_b = f"Company {chr(70+i%5)}"  # F, G, H, I, J
    reduction = random.choice([30, 40, 50])
    
    samples.append(make_sample(
        case_id=f"IND-DURESS-{3000+i}",
        
        facts=f"""{company_a} threatens to breach existing supply contract unless {company_b} reduces price by {reduction}%. {company_b} depends entirely on {company_a}'s supplies. Finding alternative would take 8 months causing bankruptcy. {company_b} agrees. Later seeks to void modification claiming economic duress.""",
        
        issues="""- Economic duress established?
- Is contract modification valid?
- Can modification be voided?""",
        
        principles="""- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent
- Contract Modification: Requires fresh consideration + free consent
- Threat of lawful act can constitute duress if illegitimate
- No alternative = vitiated consent""",
        
        reasoning=f"""Step 1 — Economic Duress Test:
Elements: (a) Illegitimate pressure (b) No practical alternative (c) Vitiated consent

Step 2 — Analyzing Pressure:
Threat: Breach of existing contract
Lawfulness: Breach is unlawful (contract violation)
Legitimacy: Using breach threat to extract concession = illegitimate
Result: Illegitimate pressure established

Step 3 — Analyzing Alternatives:
{company_b}'s options: (a) Accept reduction (b) Find alternative supplier
Alternative timeline: 8 months
Consequence of delay: Bankruptcy
Result: No practical alternative

Step 4 — Consent Analysis:
Choice made under: Threat of bankruptcy
Voluntariness: Coerced by circumstances
Result: Consent vitiated""",
        
        findings=f"""- ECONOMIC_DURESS_ESTABLISHED: Yes
- ILLEGITIMATE_PRESSURE: Yes (breach threat)
- PRACTICAL_ALTERNATIVE_EXISTS: No
- FREE_CONSENT: No
- MODIFICATION_VALID: No
- CONTRACT_VOIDABLE: Yes""",
        
        legal_effect=f"""Because ECONOMIC_DURESS_ESTABLISHED = Yes and FREE_CONSENT = No, the modification cannot be valid. Because MODIFICATION_VALID = No, {company_b} is not bound by the price reduction. Because CONTRACT_VOIDABLE = Yes, {company_b} may rescind and revert to original contract terms.""",
        
        conclusion=f"""Modification VOIDABLE due to economic duress. {company_b} may rescind and enforce original contract price. Threat of breach + no alternative + vitiated consent = economic duress.""",
        
        alternatives="""- Valid modification → REJECTED: Modification requires free consent. Economic duress vitiates consent.
- Commercial pressure defense → REJECTED: Legitimate commercial pressure differs from duress. Here, breach threat is illegitimate.
- No alternative argument → REJECTED: {company_a} cannot benefit from creating situation where {company_b} has no choice.""",
        
        category="duress",
        difficulty=2,
        sections=["Economic Duress", "Contract Modification"]
    ))

# ============================================================================
# LEVEL 3 - Fraud vs Misrepresentation (Intent Ambiguity)
# ============================================================================

print("Level 3: Fraud vs Misrepresentation (15 samples)...")

for i in range(15):
    seller = get_name('male')
    buyer = get_name('female')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-FRAUD-{4000+i}",
        
        facts=f"""{seller} sells car to {buyer} for {amount}, stating "engine overhauled last year." {seller} was told this by previous owner but never verified. Later, {buyer} discovers engine was never overhauled. {buyer} claims fraud. {seller} argues innocent misrepresentation (believed statement true).""",
        
        issues="""- Fraud (Section 17) or misrepresentation (Section 18)?
- Is belief in truth sufficient defense?
- Does failure to verify = recklessness?""",
        
        principles="""- Section 17: Fraud = false statement without belief in truth
- Section 18: Misrepresentation = false statement believed true
- Derry v. Peek (1889): Fraud requires knowledge OR reckless indifference
- Remedies: Fraud = damages + rescission; Misrepresentation = rescission only""",
        
        reasoning=f"""Step 1 — Doctrine Selection:
(a) Fraud (Section 17) → knowledge/recklessness
(b) Misrepresentation (Section 18) → honest belief

Step 2 — Analyzing Mental State:
Statement: "Engine overhauled" (objectively false)
Basis: Previous owner's claim
Verification: None
{seller}'s belief: Claims honest belief

Step 3 — Derry v. Peek Test:
Fraud requires: (a) Knowledge OR (b) Reckless indifference
Honest belief defense: Valid if reasonable grounds
Recklessness: Failure to verify material fact in commercial transaction

Step 4 — Balancing:
For recklessness: Material fact, easy to verify, commercial context
Against recklessness: Relied on previous owner, no red flags
Conclusion: Leans toward innocent misrepresentation""",
        
        findings=f"""- FALSE_STATEMENT: Yes
- KNOWLEDGE_OF_FALSITY: No
- HONEST_BELIEF: Yes (claimed)
- RECKLESS_INDIFFERENCE: Unclear
- FRAUD_ESTABLISHED: No (likely)
- MISREPRESENTATION_ESTABLISHED: Yes
- DAMAGES_AVAILABLE: No
- RESCISSION_AVAILABLE: Yes""",
        
        legal_effect=f"""Because FRAUD_ESTABLISHED = No and MISREPRESENTATION_ESTABLISHED = Yes, {buyer} cannot claim damages. Because RESCISSION_AVAILABLE = Yes, {buyer} may rescind contract. Because DAMAGES_AVAILABLE = No, {buyer}'s remedy is limited to rescission (return car, recover price).""",
        
        conclusion=f"""Likely INNOCENT MISREPRESENTATION (Section 18), not fraud. {seller}'s honest belief based on previous owner negates fraud. {buyer} may rescind but cannot claim damages.""",
        
        alternatives="""- Fraud (Section 17) → REJECTED (likely): Derry v. Peek requires knowledge or recklessness. Reliance on previous owner suggests honest belief absent red flags.
- Caveat emptor → REJECTED: Buyer beware doesn't protect affirmative false statements.
- No reliance → REJECTED: {buyer} purchased based on statement. Material fact affecting value.""",
        
        category="fraud_misrepresentation",
        difficulty=3,
        sections=["Section 17", "Section 18"]
    ))

# ============================================================================
# LEVEL 1 - Clear Application (10 samples)
# ============================================================================

print("Level 1: Clear Application (10 samples)...")

for i in range(10):
    name = get_name('male')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-MINOR-{5000+i}",
        
        facts=f"""{name}, aged 15, borrows {amount} from bank using forged birth certificate showing age 25. Bank conducts due diligence. {name} uses money for business which fails. Bank sues for recovery. {name} admits fraud but claims minority defense.""",
        
        issues="""- Can bank enforce despite fraud?
- Does fraud create estoppel?
- What is bank's remedy?""",
        
        principles="""- Section 11: Minor incompetent
- Mohori Bibee (1903): Minor's contract void ab initio
- Estoppel cannot validate void contract
- Restitution: Limited and fact-dependent, does not validate contract""",
        
        reasoning=f"""Step 1 — Applicable Doctrine:
Mohori Bibee directly governs minor's contracts

Step 2 — Mohori Bibee Rule:
Minor's contract void ab initio means:
- No contract ever existed
- Fraud by minor irrelevant
- Estoppel inapplicable

Step 3 — Fact Application:
{name} is 15 → minor under Section 11
Contract void regardless of fraud
Bank's due diligence irrelevant""",
        
        findings=f"""- MINORITY_ESTABLISHED: Yes
- FRAUD_BY_MINOR: Yes
- CONTRACTUAL_CAPACITY: No
- VALID_CONTRACT_FORMED: No
- VOID_AB_INITIO: Yes
- ESTOPPEL_APPLIES: No
- CONTRACTUAL_REMEDY_AVAILABLE: No
- RESTITUTION_AVAILABLE: Limited / fact-dependent""",
        
        legal_effect=f"""Because VALID_CONTRACT_FORMED = No, bank cannot enforce contract. Because ESTOPPEL_APPLIES = No (Mohori Bibee bars estoppel for void contracts), fraud is irrelevant. Because CONTRACTUAL_REMEDY_AVAILABLE = No, bank cannot claim price. Any restitution is limited and fact-dependent (e.g., if money traceable) and does not validate the contract.""",
        
        conclusion=f"""Contract VOID AB INITIO. Bank cannot enforce despite fraud. Mohori Bibee bars contractual remedies. Bank may pursue limited equitable restitution if money traceable, or tort action for fraud.""",
        
        alternatives="""- Estoppel → REJECTED: Mohori Bibee explicitly bars estoppel for void contracts.
- Due diligence defense → REJECTED: Competency is objective. Bank's belief doesn't create capacity.
- Unjust enrichment → REJECTED: Quasi-contractual remedies unavailable for incompetency (Mohori Bibee).""",
        
        category="minor_clear",
        difficulty=1,
        sections=["Section 11"]
    ))

# ============================================================================
# LEVEL 4 - Edge Cases (15 samples)
# ============================================================================

print("Level 4: Edge Cases (15 samples)...")

for i in range(15):
    seller = get_name('male')
    buyer = get_name('female')
    amount = get_amount()
    value = random.choice(["₹5 crore", "₹10 crore", "₹15 crore"])
    
    samples.append(make_sample(
        case_id=f"IND-MISTAKE-{6000+i}",
        
        facts=f"""{seller} sells painting to {buyer} for {amount}. Both believe it's reproduction. After sale, discovered to be original worth {value}. {seller} claims void under Section 20 (mutual mistake about essential fact). {buyer} argues mistake about value, not existence.""",
        
        issues="""- Mistake about authenticity = existence or quality?
- Does mutual mistake about value void contract?
- Essential vs non-essential mistake?""",
        
        principles="""- Section 20: Mutual mistake about essential fact voids contract
- Couturier v. Hastie (1856): Mistake about existence voids
- Bell v. Lever Brothers (1932): Mistake about quality doesn't void
- Essential = identity/nature; Non-essential = value/quality""",
        
        reasoning=f"""Step 1 — Frameworks:
(a) Existence mistake (Couturier) → void
(b) Quality mistake (Bell) → valid

Step 2 — Categorizing Mistake:
Not existence: Painting exists
Not mere quality: Original vs reproduction = different category
Identity question: Is original different thing than reproduction?

Step 3 — Essence Analysis:
Original vs reproduction affects:
- Legal rights (copyright)
- Economic value (100x difference)
- Intrinsic nature (artistic vs mechanical)
This is identity/nature mistake, not mere quality

Step 4 — Section 20 Application:
Essential fact: Fundamental nature/identity
Here: Authenticity defines identity
Both parties mistaken about identity
Mistake is essential""",
        
        findings=f"""- MUTUAL_MISTAKE: Yes
- MISTAKE_ABOUT_EXISTENCE: No
- MISTAKE_ABOUT_QUALITY: No
- MISTAKE_ABOUT_IDENTITY: Yes
- ESSENTIAL_FACT_MISTAKE: Yes
- CONTRACT_VOID: Yes (likely)
- RESTITUTION_REQUIRED: Yes""",
        
        legal_effect=f"""Because MISTAKE_ABOUT_IDENTITY = Yes and ESSENTIAL_FACT_MISTAKE = Yes, Section 20 applies. Because CONTRACT_VOID = Yes, neither party bound. Because RESTITUTION_REQUIRED = Yes, parties must restore original positions ({buyer} returns painting, {seller} returns {amount}).""",
        
        conclusion=f"""Contract likely VOID under Section 20. Mutual mistake about authenticity (original vs reproduction) is mistake about essential fact (identity/nature, not mere quality). Extreme value difference and fundamental nature support essentiality.""",
        
        alternatives="""- Bell v. Lever Brothers (quality) → REJECTED: Original vs reproduction is identity difference, not quality. Affects legal nature, intrinsic character, and category.
- Caveat emptor → REJECTED: Mutual mistake overrides when both parties mistaken about essential fact.
- Painting unchanged → REJECTED: Physical object same but legal/intrinsic identity changed. Section 20 concerns factual matter affecting identity.""",
        
        category="mistake_edge",
        difficulty=4,
        sections=["Section 20"]
    ))

# ============================================================================
# Save Dataset
# ============================================================================

print(f"\n{'='*80}")
print(f"Saving improved dataset...")

with open('legal_reasoning_improved.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print(f"✓ COMPLETE! Total samples: {len(samples)}")
print(f"\nDataset Statistics:")
print(f"  Level 1 (Clear): {sum(1 for s in samples if s['metadata']['difficulty'] == 1)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 1)/len(samples)*100:.1f}%)")
print(f"  Level 2 (Competing): {sum(1 for s in samples if s['metadata']['difficulty'] == 2)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 2)/len(samples)*100:.1f}%)")
print(f"  Level 3 (Ambiguous): {sum(1 for s in samples if s['metadata']['difficulty'] == 3)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 3)/len(samples)*100:.1f}%)")
print(f"  Level 4 (Edge Cases): {sum(1 for s in samples if s['metadata']['difficulty'] == 4)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 4)/len(samples)*100:.1f}%)")
print(f"\n{'='*80}")
print("✅ Improved dataset with FINDINGS + LEGAL_EFFECT ready!")
print("\nKey improvements:")
print("  ✓ FINDINGS block teaches state variables")
print("  ✓ LEGAL_EFFECT block teaches consequence propagation")
print("  ✓ Shorter samples optimized for Gemma-2B")
print("  ✓ Economic duress examples added")
print("  ✓ Logical dependency chains enforced")
