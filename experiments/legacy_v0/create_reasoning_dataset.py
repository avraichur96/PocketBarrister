"""
Generate Legal Reasoning Dataset for LoRA Fine-Tuning
Based on Master Prompt principles - teaches HOW lawyers think, not WHAT law exists
"""

import json
import random

# Real Indian names and entities
MALE_NAMES = ["Raj", "Amit", "Vikram", "Arjun", "Rohan", "Karan", "Aditya", "Sanjay", "Rahul", "Pradeep"]
FEMALE_NAMES = ["Priya", "Anjali", "Neha", "Pooja", "Kavita", "Sunita", "Meera", "Ritu", "Divya", "Sneha"]
COMPANY_NAMES = ["TechCorp India", "Mumbai Traders", "Delhi Enterprises", "Bangalore Solutions", "Chennai Industries"]

def get_name(gender='male'):
    return random.choice(MALE_NAMES if gender == 'male' else FEMALE_NAMES)

def get_company():
    return random.choice(COMPANY_NAMES)

def get_amount():
    amounts = ["₹5 lakh", "₹10 lakh", "₹25 lakh", "₹50 lakh", "₹1 crore", "₹2 crore", "₹5 crore"]
    return random.choice(amounts)

# New format following Master Prompt principles
def make_reasoning_sample(case_id, facts, issues, principles, reasoning, conclusion, 
                          alternatives_rejected, category, difficulty, sections):
    """
    Create sample following Master Prompt format
    Teaches reasoning geometry, not legal trivia
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

CONCLUSION:
{conclusion}

WHY ALTERNATIVES FAIL:
{alternatives_rejected}<|end_of_text|>"""
    
    token_count = int((len(input_text) + len(output_text)) / 4.5)
    
    return {
        "input": input_text,
        "output": output_text,
        "metadata": {
            "case_id": case_id,
            "category": category,
            "difficulty": difficulty,  # Level 1-4
            "sections": sections,
            "jurisdiction": "India",
            "token_count": token_count
        }
    }

samples = []

# ============================================================================
# LEVEL 2 SAMPLES - Competing Doctrines (40% of dataset)
# ============================================================================

print("Generating Level 2 samples (Competing Doctrines)...")

# Sample 1: Minor's Contract - Void vs Voidable Competition
for i in range(20):
    name = get_name('male')
    amount = get_amount()
    age = random.choice([16, 17])
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-CONTRACT-{1000+i}",
        facts=f"""{name}, aged {age}, enters into a contract to purchase goods worth {amount}. The seller was unaware of {name}'s age. {name} provided no false documents but appeared mature. After delivery, {name} refuses to pay, claiming minority. The seller argues the contract should be voidable (allowing restitution) rather than void ab initio (no remedy).""",
        
        issues="""- Is minor's contract void ab initio or merely voidable?
- Does seller's ignorance of minority affect contract status?
- Can seller claim restitution under equity despite void contract?""",
        
        principles="""- Section 10 & 11, Indian Contract Act: Minor incompetent to contract
- Mohori Bibee v. Dharmodas Ghose (1903): Minor's contract void ab initio
- Section 64 & 65: Restitution principles for void contracts
- Competing doctrine: Voidable contracts (Section 19) allow restitution""",
        
        reasoning=f"""Step 1 — Doctrine Selection:
Two competing frameworks:
(a) Void ab initio (Mohori Bibee) → no contract ever existed
(b) Voidable contract (Section 19) → contract exists until avoided

Step 2 — Fact-to-Rule Mapping:
- {name} is {age} years old → minor under Section 11
- No fraud by minor (no false documents)
- Seller's ignorance is irrelevant to competency requirement
- Goods delivered and received

Step 3 — Applying Mohori Bibee Test:
Mohori Bibee holds: minor's contract void ab initio regardless of:
- minor's fraud or misrepresentation
- other party's knowledge or ignorance
- whether minor benefited
Rationale: Competency is absolute requirement, not relative

Step 4 — Rejecting Voidable Contract Framework:
Voidable contracts (Section 19) apply when:
- contract formed validly BUT
- consent vitiated by coercion/undue influence/fraud/misrepresentation
Here: Contract never formed validly (incompetent party)
Voidable ≠ Void ab initio

Step 5 — Restitution Analysis:
Section 65 allows restitution for void contracts BUT:
- Limited to benefits received
- Does not validate void contract
- Seller may recover goods if identifiable
- Cannot claim price (contract remedy)""",
        
        conclusion=f"""Contract is VOID AB INITIO under Mohori Bibee principle. Seller cannot enforce payment. Seller's only remedy is restitution under Section 65 (return of goods if identifiable), not contract damages.""",
        
        alternatives_rejected="""- Voidable contract doctrine (Section 19) → REJECTED: Applies only when valid contract formed but consent vitiated. Here, no valid contract due to incompetency.

- Estoppel against minor → REJECTED: Mohori Bibee explicitly bars estoppel from validating void contracts. Minor's appearance or behavior irrelevant.

- Seller's ignorance as defense → REJECTED: Competency is objective requirement. Seller's subjective knowledge does not create competency.

- Quantum meruit claim → REJECTED: Quasi-contractual remedies unavailable when contract void for incompetency (Mohori Bibee bars all contractual and quasi-contractual claims).""",
        
        category="capacity_void_voidable",
        difficulty=2,
        sections=["Section 10", "Section 11", "Section 19", "Section 65"]
    ))

# Sample 2: Coercion vs Undue Influence - Doctrine Competition
for i in range(20):
    father = get_name('male')
    daughter = get_name('female')
    amount = get_amount()
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-CONSENT-{2000+i}",
        facts=f"""{father}, a wealthy businessman, tells his daughter {daughter} that he will disinherit her and cut all financial support unless she transfers her inherited property worth {amount} to her brother. {daughter}, financially dependent on {father} and emotionally attached, agrees and executes the transfer. She later seeks to void the transfer claiming either coercion (Section 15) or undue influence (Section 16).""",
        
        issues="""- Does father's threat constitute coercion under Section 15?
- Alternatively, does father-daughter relationship create undue influence under Section 16?
- Which doctrine applies when both seem plausible?""",
        
        principles="""- Section 15: Coercion requires threat to commit act forbidden by IPC
- Section 16: Undue influence requires dominant position + unfair advantage
- Ranganayakamma v. Alwar Setti (1889): Threat must be of harm to another
- Inche Noriah v. Shaik Allie Bin Omar (1929): Fiduciary relationships create presumption""",
        
        reasoning=f"""Step 1 — Identifying Competing Doctrines:
Both Section 15 (coercion) and Section 16 (undue influence) potentially apply.
Must determine which framework fits facts better.

Step 2 — Testing Coercion Framework (Section 15):
Elements required:
(a) Threat to commit act forbidden by IPC
(b) Intention to induce agreement

Fact analysis:
- Threat: Disinheritance + cutting financial support
- IPC violation: Disinheritance is LEGAL (testamentary freedom)
- Cutting support: No legal duty to support adult child

Ranganayakamma test: Threat must be of unlawful act
Here: All threatened acts are lawful
Conclusion: Section 15 NOT satisfied

Step 3 — Testing Undue Influence Framework (Section 16):
Elements required:
(a) Relationship creating dominant position
(b) Use of that position
(c) To obtain unfair advantage

Fact analysis:
- Relationship: Father-daughter (fiduciary per Inche Noriah)
- Dominant position: Financial dependence + emotional bond
- Unfair advantage: Transfer of {amount} property for no consideration
- Pressure: Threat of disinheritance (lawful but exploitative)

Step 4 — Distinguishing Coercion from Undue Influence:
Coercion: Unlawful threat to ANY person
Undue Influence: Lawful pressure within SPECIAL relationship

Key distinction: Lawfulness of pressure + relationship context
Here: Lawful pressure + fiduciary relationship → Undue Influence

Step 5 — Applying Inche Noriah Presumption:
Father-daughter relationship creates rebuttable presumption
Burden shifts to {father} to prove:
- Transaction was fair
- {daughter} had independent advice
- No exploitation of dominant position

Facts show: No independent advice, gross undervalue (no consideration)
Presumption unrebutted.""",
        
        conclusion=f"""Transfer voidable under Section 16 (Undue Influence), NOT Section 15 (Coercion). Father's lawful threats within fiduciary relationship constitute undue influence. Inche Noriah presumption applies and is unrebutted.""",
        
        alternatives_rejected="""- Coercion (Section 15) → REJECTED: Disinheritance and cutting support are lawful acts. Section 15 requires threat of IPC-forbidden act. Ranganayakamma: lawful threats don't constitute coercion.

- Free consent → REJECTED: Inche Noriah creates presumption of undue influence in fiduciary relationships. Financial dependence + emotional pressure + no independent advice rebuts free consent.

- Commercial pressure defense → REJECTED: This is family relationship, not commercial dealing. Different standards apply. Fiduciary duty exists.

- Voluntary gift → REJECTED: Absence of consideration + dominant relationship + pressure = undue influence, not voluntary gift. Burden on father to prove voluntariness (Inche Noriah).""",
        
        category="consent_coercion_undue_influence",
        difficulty=2,
        sections=["Section 15", "Section 16"]
    ))

# Sample 3: Fraud vs Misrepresentation - Intent Ambiguity
for i in range(20):
    seller = get_name('male')
    buyer = get_name('female')
    amount = get_amount()
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-FRAUD-{3000+i}",
        facts=f"""{seller} sells a used car to {buyer} for {amount}, stating "the engine was overhauled last year." {seller} had been told this by the previous owner but never verified it. Later, {buyer} discovers the engine was never overhauled. {buyer} claims fraud (Section 17). {seller} argues innocent misrepresentation (Section 18) since he believed the statement was true.""",
        
        issues="""- Does seller's statement constitute fraud (Section 17) or innocent misrepresentation (Section 18)?
- Is belief in truth sufficient defense against fraud?
- Does failure to verify create reckless indifference?""",
        
        principles="""- Section 17: Fraud requires false statement made without belief in its truth
- Section 18: Misrepresentation is false statement believed to be true
- Derry v. Peek (1889): Fraud requires knowledge of falsity OR reckless indifference
- Remedies differ: Fraud allows damages + rescission; Misrepresentation only rescission""",
        
        reasoning=f"""Step 1 — Doctrine Selection Framework:
Two competing doctrines:
(a) Fraud (Section 17) → damages + rescission
(b) Innocent Misrepresentation (Section 18) → rescission only

Distinction hinges on: Belief in truth vs knowledge of falsity/recklessness

Step 2 — Analyzing Seller's Mental State:
Facts show:
- {seller} made statement based on previous owner's claim
- {seller} never verified the statement
- Statement was objectively false

Question: Does reliance on unverified third-party statement = belief in truth?

Step 3 — Applying Derry v. Peek Test:
Fraud requires ONE of:
(a) Knowledge of falsity
(b) Absence of belief in truth
(c) Reckless indifference to truth

Analyzing each:
(a) Knowledge: {seller} did not KNOW it was false
(b) Belief: {seller} claims he believed it (based on previous owner)
(c) Recklessness: Did {seller} have duty to verify?

Step 4 — Reckless Indifference Analysis:
Derry v. Peek: Honest belief negates fraud UNLESS belief is reckless

Factors indicating recklessness:
- Commercial transaction (not casual statement)
- Material fact affecting value
- Easy to verify (service records)
- {seller} made no effort to verify
- {seller} presented as fact, not opinion

Factors against recklessness:
- Previous owner's statement (some basis)
- No evidence {seller} suspected falsity

Step 5 — Balancing Test:
Honest belief based on unverified third-party claim in commercial transaction:
- If {seller} had reasonable grounds to believe → Misrepresentation
- If {seller} made no inquiry despite red flags → Reckless indifference → Fraud

Here: No red flags evident, relied on previous owner
Leans toward innocent misrepresentation""",
        
        conclusion=f"""Likely INNOCENT MISREPRESENTATION (Section 18), not fraud. {seller} had honest belief based on previous owner's statement. Absent evidence of reckless indifference or red flags, Derry v. Peek protects honest belief. {buyer} can rescind but cannot claim damages.""",
        
        alternatives_rejected="""- Fraud (Section 17) → REJECTED (probably): Derry v. Peek requires knowledge or reckless indifference. Reliance on previous owner's statement suggests honest belief. No evidence of red flags ignored.

- Mere opinion defense → REJECTED: Statement about engine overhaul is factual claim, not opinion. Presented as fact, not belief.

- Caveat emptor (buyer beware) → REJECTED: While buyers should inspect, seller's positive false statement creates liability. Caveat emptor doesn't protect affirmative misrepresentation.

- No reliance → REJECTED: {buyer} purchased based on statement. Reliance element satisfied. Material fact affecting value.""",
        
        category="fraud_misrepresentation_intent",
        difficulty=2,
        sections=["Section 17", "Section 18"]
    ))

# ============================================================================
# LEVEL 3 SAMPLES - Ambiguous Cases (30% of dataset)
# ============================================================================

print("Generating Level 3 samples (Ambiguous Cases)...")

# Sample 4: Consideration - Past vs Executed
for i in range(30):
    person1 = get_name('male')
    person2 = get_name('female')
    amount = get_amount()
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-CONSIDERATION-{4000+i}",
        facts=f"""{person1} saves {person2}'s child from drowning. Three days later, grateful {person2} promises in writing to pay {person1} {amount}. After one month, {person2} refuses to pay. {person1} sues. {person2} claims past consideration is no consideration (Durga Prasad rule). {person1} argues Section 25(2) exception for voluntary services.""",
        
        issues="""- Is saving the child past consideration (void) or voluntary service (valid exception)?
- Does timing gap (3 days) affect characterization?
- How to distinguish past consideration from Section 25(2) exception?""",
        
        principles="""- General Rule: Past consideration is no consideration (Durga Prasad v. Baldeo, 1880)
- Section 25(2) Exception: Promise to compensate for voluntary service already rendered
- Timing and voluntariness are key factors
- Promise must be in writing (Section 25 requirement)""",
        
        reasoning=f"""Step 1 — Identifying Legal Tension:
Two competing principles:
(a) Durga Prasad: Past consideration void
(b) Section 25(2): Voluntary service exception

Both seem applicable. Must determine which governs.

Step 2 — Analyzing Durga Prasad Rule:
Past consideration void because:
- Act done before promise
- No bargained-for exchange
- Promise is gratuitous, not contractual

Fact mapping:
- {person1} saved child BEFORE promise (3 days gap)
- No prior agreement or expectation of payment
- Promise made after service complete

Prima facie: Past consideration → void

Step 3 — Testing Section 25(2) Exception:
Exception requires:
(a) Voluntary service already rendered
(b) Promise to compensate for that service
(c) Promise in writing

Fact mapping:
- Service: Saving child (voluntary, no duty)
- Promise: To pay {amount} for that service
- Form: Written promise (satisfied)

Prima facie: Exception applies → valid

Step 4 — Resolving Conflict:
Both frameworks fit facts. How to choose?

Distinguishing factors:
- Nature of service: Emergency rescue vs ordinary service
- Voluntariness: True volunteer vs expectation of payment
- Social context: Moral obligation vs commercial expectation

Section 25(2) rationale: Prevent unjust enrichment for voluntary services
Durga Prasad rationale: Prevent gratuitous promises from creating liability

Step 5 — Applying Policy:
Saving child from drowning:
- Clearly voluntary (no legal duty)
- Emergency context (no time to negotiate)
- Significant benefit conferred
- Written promise (deliberate, not impulsive)

Section 25(2) designed for exactly this scenario
Durga Prasad applies to purely gratuitous promises without service

Step 6 — Timing Analysis:
3-day gap between service and promise:
- Shows promise was deliberate, not impulsive
- Confirms service was truly voluntary (no prior agreement)
- Supports Section 25(2) characterization""",
        
        conclusion=f"""Promise ENFORCEABLE under Section 25(2) exception. Saving child constitutes voluntary service. Written promise to compensate falls within exception despite past consideration. Durga Prasad rule inapplicable to voluntary services.""",
        
        alternatives_rejected="""- Durga Prasad (past consideration void) → REJECTED: Section 25(2) creates specific exception for voluntary services. Saving life is paradigmatic voluntary service. Durga Prasad applies to gratuitous promises without service.

- Moral obligation insufficient → REJECTED: While moral obligation alone doesn't create contract, Section 25(2) explicitly validates promises for voluntary services. Moral obligation + voluntary service + written promise = valid.

- No bargained-for exchange → REJECTED: Section 25(2) exception doesn't require bargain. Voluntary service + subsequent promise sufficient.

- Timing gap defeats exception → REJECTED: 3-day gap shows deliberation, doesn't negate voluntary service character. Section 25(2) doesn't require immediate promise.""",
        
        category="consideration_past_voluntary",
        difficulty=3,
        sections=["Section 25"]
    ))

# ============================================================================
# LEVEL 4 SAMPLES - Edge Cases (10% of dataset)
# ============================================================================

print("Generating Level 4 samples (Edge Cases)...")

# Sample 5: Mutual Mistake - Existence vs Quality
for i in range(10):
    seller = get_name('male')
    buyer = get_name('female')
    amount = get_amount()
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-MISTAKE-{5000+i}",
        facts=f"""{seller} sells a painting to {buyer} for {amount}. Both believe it's a reproduction. After sale, discovered to be original worth ₹10 crore. {seller} claims void contract under Section 20 (mutual mistake about essential fact). {buyer} argues mistake about value, not existence - contract valid.""",
        
        issues="""- Is mistake about painting's authenticity a mistake about existence or quality?
- Does mutual mistake about value void contract under Section 20?
- How to distinguish essential from non-essential mistakes?""",
        
        principles="""- Section 20: Mutual mistake about matter of fact essential to agreement voids contract
- Couturier v. Hastie (1856): Mistake about existence voids contract
- Bell v. Lever Brothers (1932): Mistake about quality generally doesn't void contract
- Essential vs non-essential mistake distinction""",
        
        reasoning=f"""Step 1 — Framing the Legal Question:
Section 20 voids contracts for mutual mistake about "essential" fact
Question: Is authenticity (original vs reproduction) essential or non-essential?

Two frameworks compete:
(a) Existence mistake (Couturier) → void
(b) Quality mistake (Bell v. Lever Brothers) → valid

Step 2 — Analyzing Couturier v. Hastie:
Couturier: Cargo perished before sale → void
Rationale: Subject matter ceased to exist
Mistake about existence = essential

Here: Painting exists (not perished)
Mistake is about nature/quality, not existence
Prima facie: Couturier doesn't apply

Step 3 — Analyzing Bell v. Lever Brothers:
Bell: Mistake about contract's value → not essential
Rationale: Parties got what they bargained for (the thing itself)
Quality mistakes don't void unless quality IS the essence

Question: Was authenticity the essence of this bargain?

Step 4 — Essence Analysis:
Factors suggesting authenticity IS essence:
- Reproduction vs original = different thing entirely
- Value difference extreme (₹{amount} vs ₹10 crore)
- Parties' shared assumption about nature
- Authenticity defines the thing, not just its value

Factors suggesting authenticity is NOT essence:
- Parties bargained for "this painting" (identified object)
- Physical painting unchanged (same object delivered)
- Mistake about attribute, not identity

Step 5 — Distinguishing Existence from Quality:
Spectrum:
- Existence: Thing doesn't exist (Couturier)
- Identity: Thing is different thing (closer to existence)
- Quality: Thing is same but different attribute (Bell)

Original vs reproduction:
- Not existence (painting exists)
- Not mere quality (fundamentally different category)
- Identity question: Is original a different thing than reproduction?

Step 6 — Resolution:
Indian courts have held: Mistake about fundamental nature/identity can be essential
Original vs reproduction affects:
- Legal rights (copyright)
- Economic value (100x difference)
- Intrinsic nature (artistic vs mechanical creation)

This is mistake about identity/nature, not mere quality
Falls closer to Couturier than Bell""",
        
        conclusion=f"""Contract likely VOID under Section 20. Mutual mistake about painting's authenticity (original vs reproduction) is mistake about essential fact. This is identity mistake, not mere quality mistake. Extreme value difference and fundamental nature difference support essentiality.""",
        
        alternatives_rejected="""- Bell v. Lever Brothers (quality mistake) → REJECTED: Original vs reproduction is not mere quality difference. Affects legal nature (copyright), intrinsic character (artistic vs mechanical), and identity. Bell applies to value mistakes within same category.

- Caveat emptor → REJECTED: Mutual mistake doctrine overrides caveat emptor when both parties mistaken about essential fact. No superior knowledge by either party.

- Seller's windfall → REJECTED: Section 20 is not about fairness or windfall. Focuses on whether agreement was based on shared false assumption about essential fact. Equitable considerations irrelevant.

- Painting unchanged → REJECTED: Physical object unchanged but legal and intrinsic identity changed. Section 20 concerns mistake about "matter of fact" - authenticity is factual matter affecting identity.""",
        
        category="mistake_existence_quality",
        difficulty=4,
        sections=["Section 20"]
    ))

# ============================================================================
# LEVEL 1 SAMPLES - Clear Application (20% of dataset)
# ============================================================================

print("Generating Level 1 samples (Clear Application)...")

# Sample 6: Clear Minor's Contract
for i in range(20):
    name = get_name('male')
    amount = get_amount()
    
    samples.append(make_reasoning_sample(
        case_id=f"IND-MINOR-{6000+i}",
        facts=f"""{name}, aged 15, borrows {amount} from a bank by submitting forged birth certificate showing age 25. Bank conducts due diligence and relies on certificate. {name} uses money for business which fails. Bank sues for recovery. {name} admits fraud but claims minority defense.""",
        
        issues="""- Can bank enforce contract against minor despite fraud?
- Does minor's fraud create estoppel?
- What is bank's remedy?""",
        
        principles="""- Section 10 & 11: Minor incompetent to contract
- Mohori Bibee v. Dharmodas Ghose (1903): Minor's contract void ab initio
- Estoppel cannot validate void contract
- Restitution under Section 65 limited""",
        
        reasoning=f"""Step 1 — Identifying Applicable Doctrine:
Clear case of minor's contract
Mohori Bibee directly governs

Step 2 — Applying Mohori Bibee Rule:
Minor's contract void ab initio means:
- No contract ever existed
- Fraud by minor irrelevant
- Estoppel inapplicable
- No contractual remedy available

Step 3 — Fact Application:
- {name} is 15 (minor under Section 11)
- Contract void regardless of fraud
- Bank's due diligence irrelevant
- Void ab initio = no enforcement

Step 4 — Remedy Analysis:
Bank cannot claim:
- Contract damages (no contract)
- Estoppel (Mohori Bibee bars it)

Bank may claim:
- Restitution under Section 65 (if money traceable)
- Tort remedy for fraud (separate from contract)""",
        
        conclusion=f"""Contract VOID AB INITIO. Bank cannot enforce despite {name}'s fraud. Mohori Bibee bars all contractual remedies. Bank limited to restitution (Section 65) or tort action for fraud.""",
        
        alternatives_rejected="""- Estoppel against minor → REJECTED: Mohori Bibee explicitly holds estoppel cannot validate void contract. Minor's fraud irrelevant to contract validity.

- Bank's due diligence as defense → REJECTED: Competency is objective requirement. Bank's reasonable belief doesn't create competency.

- Voidable contract → REJECTED: Minor's contract is void ab initio, not voidable. No option to ratify upon majority.

- Unjust enrichment → REJECTED: Quasi-contractual remedies unavailable when contract void for incompetency (Mohori Bibee principle).""",
        
        category="minor_clear_void",
        difficulty=1,
        sections=["Section 10", "Section 11"]
    ))

# ============================================================================
# Save Dataset
# ============================================================================

print(f"\n{'='*80}")
print(f"Saving dataset...")

with open('legal_reasoning_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print(f"✓ COMPLETE! Total samples: {len(samples)}")
print(f"\nDataset Statistics:")
print(f"  Level 1 (Clear): {sum(1 for s in samples if s['metadata']['difficulty'] == 1)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 1)/len(samples)*100:.1f}%)")
print(f"  Level 2 (Competing): {sum(1 for s in samples if s['metadata']['difficulty'] == 2)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 2)/len(samples)*100:.1f}%)")
print(f"  Level 3 (Ambiguous): {sum(1 for s in samples if s['metadata']['difficulty'] == 3)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 3)/len(samples)*100:.1f}%)")
print(f"  Level 4 (Edge Cases): {sum(1 for s in samples if s['metadata']['difficulty'] == 4)} ({sum(1 for s in samples if s['metadata']['difficulty'] == 4)/len(samples)*100:.1f}%)")
print(f"\n{'='*80}")
print("✅ Legal Reasoning Dataset ready for LoRA training!")
