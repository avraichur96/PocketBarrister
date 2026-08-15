"""
Extended Legal Reasoning Dataset - Additional 100 Samples
Maintains FINDINGS + LEGAL_EFFECT structure
Distribution: 30 duress + 25 undue influence + 20 void/voidable + 15 hard negatives + 10 short EOS
"""

import json
import random

MALE_NAMES = ["Raj", "Amit", "Vikram", "Arjun", "Rohan", "Karan", "Aditya", "Sanjay", "Rahul", "Pradeep"]
FEMALE_NAMES = ["Priya", "Anjali", "Neha", "Pooja", "Kavita", "Sunita", "Meera", "Ritu", "Divya", "Sneha"]
COMPANY_NAMES = ["TechCorp", "InfoSystems", "DataSolutions", "CloudWorks", "NetServices"]

def get_name(gender='male'):
    return random.choice(MALE_NAMES if gender == 'male' else FEMALE_NAMES)

def get_company():
    return random.choice(COMPANY_NAMES)

def get_amount():
    return random.choice(["₹5 lakh", "₹10 lakh", "₹25 lakh", "₹50 lakh", "₹1 crore", "₹2 crore"])

def make_sample(case_id, facts, issues, principles, reasoning, findings, legal_effect, 
                conclusion, alternatives, category, difficulty, sections):
    """Format with FINDINGS + LEGAL_EFFECT for consequence propagation"""
    
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

print("Generating extended dataset (100 additional samples)...")
print("="*80)

# ============================================================================
# CATEGORY 1: Role-Binding Duress Cases (30 samples)
# ============================================================================

print("Category 1: Role-Binding Duress (30 samples)...")

# Subcategory: Employment duress
for i in range(10):
    employee = get_name('male')
    employer = get_company()
    amount = get_amount()
    reduction = random.choice([20, 30, 40])
    
    samples.append(make_sample(
        case_id=f"IND-EMP-DURESS-{7000+i}",
        
        facts=f"""{employer} threatens to terminate {employee}'s employment unless he accepts {reduction}% salary reduction. {employee} has specialized skills unmarketable elsewhere and family medical expenses. No alternative employment available in 6 months. {employee} signs under protest. Later seeks to void modification claiming economic duress.""",
        
        issues="""- Economic duress in employment context?
- Is threat of lawful termination illegitimate pressure?
- Does lack of alternative employment vitiate consent?""",
        
        principles="""- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent
- Employment context: Threat of lawful act can be illegitimate if exploitative
- Modification requires free consent
- Dependency relationship affects duress analysis""",
        
        reasoning=f"""Step 1 — Duress Elements:
(a) Illegitimate pressure (b) No practical alternative (c) Vitiated consent

Step 2 — Pressure Analysis:
Threat: Termination (lawful act)
Context: Employment relationship (dependency)
Legitimacy: Using termination threat to extract wage concession
Exploitation: Leveraging employee's vulnerability (medical expenses, specialized skills)
Result: Lawful threat becomes illegitimate due to exploitative purpose

Step 3 — Alternative Analysis:
{employee}'s options: (a) Accept reduction (b) Find new employment
Alternative timeline: 6 months minimum
Specialized skills: Unmarketable elsewhere
Financial pressure: Family medical expenses
Result: No practical alternative

Step 4 — Consent Analysis:
Signed under protest (explicit lack of voluntariness)
Coerced by financial necessity and lack of alternatives
Result: Consent vitiated""",
        
        findings=f"""- ECONOMIC_DURESS_ESTABLISHED: Yes
- ILLEGITIMATE_PRESSURE: Yes (exploitative termination threat)
- PRACTICAL_ALTERNATIVE_EXISTS: No
- FREE_CONSENT: No
- EMPLOYMENT_DEPENDENCY: Yes
- MODIFICATION_VALID: No
- CONTRACT_VOIDABLE: Yes""",
        
        legal_effect=f"""Because ECONOMIC_DURESS_ESTABLISHED = Yes and FREE_CONSENT = No, the modification cannot be valid. Because EMPLOYMENT_DEPENDENCY = Yes and PRACTICAL_ALTERNATIVE_EXISTS = No, the lack of consent is established. Because MODIFICATION_VALID = No, {employee} is not bound by salary reduction. Because CONTRACT_VOIDABLE = Yes, {employee} may rescind and claim original salary.""",
        
        conclusion=f"""Modification VOIDABLE due to economic duress. Lawful termination threat becomes illegitimate when exploiting employee's vulnerability. {employee} may rescind and enforce original salary terms.""",
        
        alternatives="""- Valid modification → REJECTED: Free consent required. Economic duress vitiates consent even when threat is lawful act.
- At-will employment defense → REJECTED: Right to terminate doesn't permit exploitative use of termination threat to extract concessions.
- Employee accepted → REJECTED: Signing under protest with no alternative negates voluntariness.""",
        
        category="employment_duress",
        difficulty=2,
        sections=["Economic Duress", "Employment Law"]
    ))

# Subcategory: Supplier dependency duress
for i in range(10):
    supplier = get_company()
    buyer = get_company()
    increase = random.choice([40, 50, 60])
    
    samples.append(make_sample(
        case_id=f"IND-SUPPLIER-DURESS-{7100+i}",
        
        facts=f"""{supplier} threatens to stop deliveries mid-contract unless {buyer} agrees to {increase}% price increase. {buyer} manufactures products requiring {supplier}'s components. Finding alternative supplier requires 9 months retooling. {buyer} agrees to avoid production shutdown. Later seeks to void claiming duress.""",
        
        issues="""- Economic duress in commercial context?
- Does supplier dependency create duress?
- Is mid-contract price increase voidable?""",
        
        principles="""- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent
- Commercial context: Exploiting contractual dependency
- Good faith modification vs duress
- Retooling costs and timeline affect alternatives""",
        
        reasoning=f"""Step 1 — Duress Test:
Elements: (a) Illegitimate pressure (b) No alternative (c) Vitiated consent

Step 2 — Pressure Legitimacy:
Threat: Stop deliveries mid-contract (breach)
Existing obligation: Contract requires continued supply
Legitimacy: Using breach threat to extract price increase = illegitimate
Distinguishing: Good faith renegotiation vs exploitative threat
Result: Illegitimate pressure

Step 3 — Alternative Analysis:
{buyer}'s options: (a) Accept increase (b) Find alternative supplier
Alternative timeline: 9 months (retooling required)
Consequence: Production shutdown, business losses
Result: No practical alternative

Step 4 — Consent Analysis:
Agreement made to avoid immediate shutdown
No genuine choice between alternatives
Result: Consent vitiated by circumstances""",
        
        findings=f"""- ECONOMIC_DURESS_ESTABLISHED: Yes
- ILLEGITIMATE_PRESSURE: Yes (breach threat)
- PRACTICAL_ALTERNATIVE_EXISTS: No
- FREE_CONSENT: No
- SUPPLIER_DEPENDENCY: Yes
- MODIFICATION_VALID: No
- CONTRACT_VOIDABLE: Yes""",
        
        legal_effect=f"""Because ECONOMIC_DURESS_ESTABLISHED = Yes and FREE_CONSENT = No, the price increase cannot be valid. Because SUPPLIER_DEPENDENCY = Yes and PRACTICAL_ALTERNATIVE_EXISTS = No, {buyer}'s consent was vitiated. Because MODIFICATION_VALID = No, {buyer} is not bound by increased price. Because CONTRACT_VOIDABLE = Yes, {buyer} may rescind and enforce original contract terms.""",
        
        conclusion=f"""Price increase VOIDABLE due to economic duress. {supplier} exploited contractual dependency and lack of alternatives. {buyer} may rescind and enforce original pricing.""",
        
        alternatives="""- Good faith renegotiation → REJECTED: Threat of breach to extract concession is not good faith. Legitimate renegotiation requires genuine mutual consent.
- Commercial pressure → REJECTED: Normal commercial pressure differs from duress. Here, exploiting dependency with breach threat = illegitimate.
- {buyer} could have refused → REJECTED: Production shutdown and business losses eliminate practical choice.""",
        
        category="supplier_duress",
        difficulty=2,
        sections=["Economic Duress", "Contract Modification"]
    ))

# Subcategory: Creditor duress
for i in range(10):
    creditor = get_company()
    debtor = get_name('male')
    original_debt = get_amount()
    additional = random.choice(["₹5 lakh", "₹10 lakh", "₹15 lakh"])
    
    samples.append(make_sample(
        case_id=f"IND-CREDITOR-DURESS-{7200+i}",
        
        facts=f"""{creditor} threatens to file criminal complaint against {debtor} for {original_debt} unless {debtor} agrees to pay additional {additional} as "processing fees." {debtor} fears reputational damage and business license revocation. {debtor} agrees. Later seeks to void additional payment claiming duress.""",
        
        issues="""- Economic duress via threat of legal action?
- Is threat of criminal complaint legitimate pressure?
- Does fear of reputation damage vitiate consent?""",
        
        principles="""- Economic Duress: Illegitimate pressure + no alternative + vitiated consent
- Threat of legal action: Generally lawful but can be illegitimate if improper purpose
- Criminal complaint for civil debt: Improper use of criminal process
- Reputational harm affects duress analysis""",
        
        reasoning=f"""Step 1 — Duress Elements:
(a) Illegitimate pressure (b) No alternative (c) Vitiated consent

Step 2 — Pressure Legitimacy:
Threat: Criminal complaint for civil debt
Legal right: Creditor may have right to file complaint
Purpose: Extract additional payment beyond debt
Improper use: Criminal process used for civil collection
Result: Threat is illegitimate despite lawfulness

Step 3 — Alternative Analysis:
{debtor}'s options: (a) Pay additional amount (b) Face criminal complaint
Consequences: Reputational damage, license revocation, business loss
Practical choice: No genuine alternative given consequences
Result: No practical alternative

Step 4 — Consent Analysis:
Agreement made under threat of criminal process
Fear of reputational and business consequences
Result: Consent vitiated""",
        
        findings=f"""- ECONOMIC_DURESS_ESTABLISHED: Yes
- ILLEGITIMATE_PRESSURE: Yes (improper use of criminal process)
- PRACTICAL_ALTERNATIVE_EXISTS: No
- FREE_CONSENT: No
- IMPROPER_PURPOSE: Yes
- ADDITIONAL_PAYMENT_VALID: No
- VOIDABLE: Yes""",
        
        legal_effect=f"""Because ECONOMIC_DURESS_ESTABLISHED = Yes and IMPROPER_PURPOSE = Yes, the additional payment cannot be valid. Because FREE_CONSENT = No, {debtor}'s agreement was vitiated. Because ADDITIONAL_PAYMENT_VALID = No, {debtor} is only liable for original debt. Because VOIDABLE = Yes, {debtor} may recover the additional {additional}.""",
        
        conclusion=f"""Additional payment VOIDABLE due to economic duress. Using criminal complaint threat to extract payment beyond debt is illegitimate pressure. {debtor} liable only for original {original_debt}, may recover additional {additional}.""",
        
        alternatives="""- Lawful threat defense → REJECTED: Even lawful threats can be illegitimate if used for improper purpose. Criminal process for civil debt collection = improper.
- Voluntary payment → REJECTED: Payment under threat of criminal complaint and reputational harm negates voluntariness.
- Creditor's right → REJECTED: Right to file complaint doesn't permit using threat to extract excessive payment.""",
        
        category="creditor_duress",
        difficulty=3,
        sections=["Economic Duress", "Improper Pressure"]
    ))

# ============================================================================
# CATEGORY 2: Role-Binding Undue Influence Cases (25 samples)
# ============================================================================

print("Category 2: Role-Binding Undue Influence (25 samples)...")

# Subcategory: Doctor-patient undue influence
for i in range(8):
    doctor = get_name('male')
    patient = get_name('female')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-MEDICAL-INFLUENCE-{8000+i}",
        
        facts=f"""Dr. {doctor} treats {patient} for terminal illness over 2 years. {patient} becomes emotionally dependent. Dr. {doctor} suggests {patient} transfer property worth {amount} to him for "continued quality care." {patient}, fearful of losing doctor's attention, agrees. No independent advice. Later, family seeks to void claiming undue influence.""",
        
        issues="""- Undue influence in doctor-patient relationship?
- Does medical dependency create dominant position?
- Is property transfer voidable?""",
        
        principles="""- Section 16: Undue influence = dominant position + unfair advantage
- Doctor-patient: Fiduciary relationship (trust and confidence)
- Medical dependency creates vulnerability
- Inche Noriah (1929): Fiduciary relationship creates presumption
- Independent advice requirement""",
        
        reasoning=f"""Step 1 — Section 16 Elements:
(a) Dominant position (b) Use of position (c) Unfair advantage

Step 2 — Relationship Analysis:
Relationship: Doctor-patient (fiduciary)
Duration: 2 years of treatment
Dependency: Terminal illness creates emotional and medical reliance
Trust: {patient} depends on Dr. {doctor} for life-sustaining care
Result: Dominant position established

Step 3 — Unfair Advantage:
Transaction: Property transfer worth {amount}
Consideration: "Continued quality care" (already owed under medical duty)
Procedural fairness: No independent advice
Substantive fairness: Property transfer for existing obligation
Result: Unfair advantage

Step 4 — Inche Noriah Presumption:
Fiduciary relationship: Yes (doctor-patient)
Presumption: Undue influence presumed
Burden: Shifts to Dr. {doctor} to prove fairness
Evidence: No independent advice, emotional dependency
Result: Presumption unrebutted""",
        
        findings=f"""- UNDUE_INFLUENCE_ESTABLISHED: Yes
- FIDUCIARY_RELATIONSHIP: Yes (doctor-patient)
- DOMINANT_POSITION: Yes
- UNFAIR_ADVANTAGE: Yes
- INDEPENDENT_ADVICE: No
- FREE_CONSENT: No
- TRANSFER_VALID: No
- VOIDABLE: Yes""",
        
        legal_effect=f"""Because FIDUCIARY_RELATIONSHIP = Yes, Inche Noriah presumption applies. Because DOMINANT_POSITION = Yes and UNFAIR_ADVANTAGE = Yes, Section 16 elements satisfied. Because INDEPENDENT_ADVICE = No and FREE_CONSENT = No, presumption unrebutted. Because TRANSFER_VALID = No, {patient} not bound. Because VOIDABLE = Yes, transfer may be set aside.""",
        
        conclusion=f"""Transfer VOIDABLE under Section 16. Doctor-patient relationship creates fiduciary duty. Medical dependency + no independent advice + transfer for existing obligation = undue influence. Transfer may be set aside.""",
        
        alternatives="""- Voluntary gift → REJECTED: Inche Noriah presumption applies in fiduciary relationships. Burden on Dr. {doctor} to prove voluntariness with independent advice.
- Consideration provided → REJECTED: "Continued quality care" is existing medical duty, not fresh consideration. Cannot charge for duty already owed.
- No coercion → REJECTED: Undue influence doesn't require coercion. Exploitation of dominant position sufficient.""",
        
        category="medical_influence",
        difficulty=2,
        sections=["Section 16", "Fiduciary Duty"]
    ))

# Subcategory: Lawyer-client undue influence
for i in range(8):
    lawyer = get_name('male')
    client = get_name('female')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-LEGAL-INFLUENCE-{8100+i}",
        
        facts=f"""{lawyer} represents {client} in complex property dispute for 3 years. {client}, elderly and illiterate, relies entirely on {lawyer}'s advice. {lawyer} suggests {client} transfer disputed property worth {amount} to him at 30% market value as "settlement strategy." {client} agrees without understanding. Later seeks to void claiming undue influence.""",
        
        issues="""- Undue influence in lawyer-client relationship?
- Does legal dependency create dominant position?
- Is undervalued transfer voidable?""",
        
        principles="""- Section 16: Dominant position + unfair advantage
- Lawyer-client: Fiduciary relationship (highest trust)
- Elderly + illiterate = enhanced vulnerability
- Inche Noriah: Presumption in fiduciary relationships
- Gross undervaluation indicates exploitation""",
        
        reasoning=f"""Step 1 — Section 16 Test:
Elements: (a) Dominant position (b) Unfair advantage

Step 2 — Dominant Position:
Relationship: Lawyer-client (fiduciary - highest trust)
Duration: 3 years of representation
Client vulnerability: Elderly, illiterate, complex legal matter
Dependency: {client} relies entirely on {lawyer}'s advice
Result: Strong dominant position

Step 3 — Unfair Advantage:
Transaction: Property transfer at 30% market value (70% undervaluation)
Explanation: "Settlement strategy" (client doesn't understand)
Procedural: No independent legal advice
Substantive: Gross undervaluation
Result: Clear unfair advantage

Step 4 — Inche Noriah Application:
Fiduciary: Yes (lawyer-client = highest fiduciary duty)
Presumption: Undue influence strongly presumed
Burden: On {lawyer} to prove transaction fair
Evidence: Gross undervaluation + no independent advice + client confusion
Result: Presumption cannot be rebutted""",
        
        findings=f"""- UNDUE_INFLUENCE_ESTABLISHED: Yes
- FIDUCIARY_RELATIONSHIP: Yes (lawyer-client)
- DOMINANT_POSITION: Yes (strong)
- UNFAIR_ADVANTAGE: Yes (70% undervaluation)
- CLIENT_UNDERSTANDING: No
- INDEPENDENT_ADVICE: No
- FREE_CONSENT: No
- TRANSFER_VALID: No
- VOIDABLE: Yes""",
        
        legal_effect=f"""Because FIDUCIARY_RELATIONSHIP = Yes (lawyer-client), strongest Inche Noriah presumption applies. Because DOMINANT_POSITION = Yes and UNFAIR_ADVANTAGE = Yes (70% undervaluation), Section 16 clearly satisfied. Because CLIENT_UNDERSTANDING = No and INDEPENDENT_ADVICE = No, presumption unrebutted. Because TRANSFER_VALID = No, {client} not bound. Because VOIDABLE = Yes, transfer must be set aside.""",
        
        conclusion=f"""Transfer VOIDABLE under Section 16. Lawyer-client fiduciary relationship + elderly illiterate client + 70% undervaluation + no independent advice = clear undue influence. Transfer must be set aside.""",
        
        alternatives="""- Voluntary transaction → REJECTED: Lawyer-client relationship creates highest fiduciary duty. Inche Noriah presumption strongest here. No evidence of voluntariness.
- Settlement strategy → REJECTED: Transferring client's property to lawyer at massive undervalue cannot be legitimate strategy. Breach of fiduciary duty.
- Client agreed → REJECTED: Agreement without understanding + no independent advice + gross undervaluation negates consent.""",
        
        category="legal_influence",
        difficulty=2,
        sections=["Section 16", "Fiduciary Duty"]
    ))

# Subcategory: Religious advisor undue influence
for i in range(9):
    advisor = get_name('male')
    devotee = get_name('female')
    amount = get_amount()
    
    samples.append(make_sample(
        case_id=f"IND-RELIGIOUS-INFLUENCE-{8200+i}",
        
        facts=f"""{advisor}, spiritual guru, has {devotee} as devoted follower for 5 years. {devotee} believes {advisor} has divine powers. {advisor} tells {devotee} that donating {amount} to him will cure her son's illness and ensure family prosperity. {devotee}, desperate, transfers property. Son's condition unchanged. Later seeks to void claiming undue influence.""",
        
        issues="""- Undue influence in spiritual advisor relationship?
- Does religious authority create dominant position?
- Is donation based on false promise voidable?""",
        
        principles="""- Section 16: Dominant position + unfair advantage
- Spiritual advisor-devotee: Relationship of trust and confidence
- Religious authority creates psychological dominance
- Exploitation of vulnerability (sick child)
- False promise of divine intervention""",
        
        reasoning=f"""Step 1 — Section 16 Elements:
(a) Dominant position (b) Unfair advantage

Step 2 — Dominant Position:
Relationship: Spiritual guru-devotee (trust and reverence)
Duration: 5 years of devotion
Belief: {devotee} believes {advisor} has divine powers
Psychological control: Religious authority creates dominance
Vulnerability: Desperate mother with sick child
Result: Strong dominant position

Step 3 — Unfair Advantage:
Transaction: Property transfer worth {amount}
Inducement: False promise of cure and prosperity
Exploitation: Using child's illness to extract property
Consideration: Divine intervention (illusory)
Result: Clear unfair advantage through exploitation

Step 4 — Consent Analysis:
Motivation: Desperation for son's cure
Voluntariness: Induced by false promise and religious authority
Genuine choice: No - acted under psychological dominance
Result: Consent vitiated""",
        
        findings=f"""- UNDUE_INFLUENCE_ESTABLISHED: Yes
- RELATIONSHIP_OF_TRUST: Yes (spiritual advisor)
- DOMINANT_POSITION: Yes (religious authority)
- UNFAIR_ADVANTAGE: Yes (exploitation of vulnerability)
- FALSE_PROMISE: Yes
- PSYCHOLOGICAL_DOMINANCE: Yes
- FREE_CONSENT: No
- DONATION_VALID: No
- VOIDABLE: Yes""",
        
        legal_effect=f"""Because RELATIONSHIP_OF_TRUST = Yes and DOMINANT_POSITION = Yes, Section 16 framework applies. Because UNFAIR_ADVANTAGE = Yes and FALSE_PROMISE = Yes, exploitation established. Because PSYCHOLOGICAL_DOMINANCE = Yes and FREE_CONSENT = No, consent vitiated. Because DONATION_VALID = No, {devotee} not bound. Because VOIDABLE = Yes, transfer may be set aside and property recovered.""",
        
        conclusion=f"""Donation VOIDABLE under Section 16. Spiritual advisor exploited religious authority and mother's desperation. False promise of divine cure + psychological dominance + exploitation of vulnerability = undue influence. Transfer may be set aside.""",
        
        alternatives="""- Voluntary donation → REJECTED: Religious authority creates dominant position. Exploitation of child's illness and false promise negate voluntariness.
- Religious belief → REJECTED: Freedom of religion doesn't permit exploitation. Using false promises to extract property = undue influence.
- No coercion → REJECTED: Undue influence doesn't require force. Psychological dominance and exploitation of vulnerability sufficient.""",
        
        category="religious_influence",
        difficulty=3,
        sections=["Section 16", "Exploitation"]
    ))

# ============================================================================
# CATEGORY 3: Void/Voidable Consequence Cases (20 samples)
# ============================================================================

print("Category 3: Void/Voidable Consequence Cases (20 samples)...")

for i in range(20):
    party_a = get_name('male')
    party_b = get_name('female')
    amount = get_amount()
    age = random.choice([17, 16, 15])
    scenario_type = i % 4
    
    if scenario_type == 0:
        # Minor ratification attempt
        samples.append(make_sample(
            case_id=f"IND-RATIFICATION-{9000+i}",
            
            facts=f"""{party_a}, aged {age}, borrows {amount} by misrepresenting age. Upon turning 18, {party_a} writes letter acknowledging debt and promising to pay. After 6 months, {party_a} refuses payment claiming original contract was void. Lender argues ratification upon majority validates contract.""",
            
            issues="""- Can minor ratify void contract upon attaining majority?
- Does acknowledgment after majority create new contract?
- What is effect of Mohori Bibee on ratification?""",
            
            principles="""- Mohori Bibee: Minor's contract void ab initio, cannot be ratified
- Void vs voidable: Only voidable contracts can be ratified
- Acknowledgment after majority: May create new contract if consideration present
- Ratification requires valid original contract""",
            
            reasoning=f"""Step 1 — Ratification Requirements:
Ratification validates contract only if:
(a) Contract was voidable (not void)
(b) Ratification after removal of incapacity
(c) Ratification with full knowledge

Step 2 — Original Contract Status:
{party_a} was {age} at contract formation
Mohori Bibee: Minor's contract void ab initio
Void vs voidable: Void = no contract exists; Voidable = contract exists until avoided
Result: No valid contract to ratify

Step 3 — Effect of Acknowledgment:
Acknowledgment after majority: {party_a} now 18
Can acknowledgment create new contract? Only if fresh consideration
Here: Acknowledgment of past debt (no fresh consideration)
Past consideration: No consideration (Durga Prasad rule)
Result: Acknowledgment doesn't create new contract

Step 4 — Mohori Bibee Application:
Void ab initio means: Never was a contract
Ratification requires: Valid original contract
Conclusion: Cannot ratify what never existed""",
            
            findings=f"""- ORIGINAL_CONTRACT_VOID: Yes (minor's contract)
- RATIFICATION_POSSIBLE: No
- VALID_CONTRACT_TO_RATIFY: No
- ACKNOWLEDGMENT_CREATES_NEW_CONTRACT: No
- FRESH_CONSIDERATION: No
- CONTRACTUAL_OBLIGATION: No
- LENDER_CAN_ENFORCE: No""",
            
            legal_effect=f"""Because ORIGINAL_CONTRACT_VOID = Yes, there is no valid contract to ratify. Because RATIFICATION_POSSIBLE = No (Mohori Bibee bars ratification of void contracts), acknowledgment has no legal effect. Because FRESH_CONSIDERATION = No, acknowledgment doesn't create new contract. Because CONTRACTUAL_OBLIGATION = No, {party_a} not bound. Because LENDER_CAN_ENFORCE = No, lender has no remedy.""",
            
            conclusion=f"""Acknowledgment INEFFECTIVE. Mohori Bibee: void ab initio contracts cannot be ratified. Acknowledgment without fresh consideration doesn't create new contract. {party_a} not bound despite acknowledgment after majority.""",
            
            alternatives="""- Ratification upon majority → REJECTED: Mohori Bibee explicitly bars ratification of void contracts. Only voidable contracts can be ratified.
- New contract by acknowledgment → REJECTED: Acknowledgment of past debt without fresh consideration is past consideration (void per Durga Prasad).
- Estoppel by acknowledgment → REJECTED: Estoppel cannot validate void contract. Mohori Bibee principle applies.""",
            
            category="ratification_void",
            difficulty=3,
            sections=["Mohori Bibee", "Ratification"]
        ))
    
    elif scenario_type == 1:
        # Voidable contract ratification
        samples.append(make_sample(
            case_id=f"IND-VOIDABLE-RAT-{9100+i}",
            
            facts=f"""{party_a} enters contract with {party_b} under undue influence. After 2 years, {party_a} discovers the influence and writes to {party_b} affirming contract and waiving right to avoid. After 6 months, {party_a} seeks to void claiming undue influence. {party_b} argues ratification bars avoidance.""",
            
            issues="""- Can voidable contract be ratified?
- Does ratification with knowledge bar subsequent avoidance?
- What constitutes valid ratification?""",
            
            principles="""- Voidable contracts (Section 19): Can be ratified or avoided
- Ratification requirements: Full knowledge + free consent + unequivocal act
- Effect of ratification: Bars subsequent avoidance
- Distinction from void contracts (cannot be ratified)""",
            
            reasoning=f"""Step 1 — Contract Status:
Original contract: Voidable (undue influence)
Void vs voidable: Voidable = valid until avoided
Ratification: Possible for voidable contracts

Step 2 — Ratification Requirements:
(a) Full knowledge of right to avoid
(b) Free consent (no continuing influence)
(c) Unequivocal act of ratification

Step 3 — Analyzing Ratification:
Knowledge: {party_a} discovered influence (full knowledge)
Consent: 2 years passed, influence likely dissipated
Act: Written affirmation and waiver (unequivocal)
Timing: After discovery but before avoidance
Result: Valid ratification

Step 4 — Effect of Ratification:
Valid ratification: Affirms contract
Legal effect: Bars subsequent avoidance
{party_a}'s position: Cannot avoid after ratification""",
            
            findings=f"""- ORIGINAL_CONTRACT_VOIDABLE: Yes
- RATIFICATION_POSSIBLE: Yes (voidable contracts)
- FULL_KNOWLEDGE: Yes
- FREE_CONSENT_AT_RATIFICATION: Yes
- UNEQUIVOCAL_ACT: Yes
- VALID_RATIFICATION: Yes
- SUBSEQUENT_AVOIDANCE_BARRED: Yes
- CONTRACT_BINDING: Yes""",
            
            legal_effect=f"""Because ORIGINAL_CONTRACT_VOIDABLE = Yes, ratification is possible. Because FULL_KNOWLEDGE = Yes and FREE_CONSENT_AT_RATIFICATION = Yes, ratification requirements satisfied. Because UNEQUIVOCAL_ACT = Yes and VALID_RATIFICATION = Yes, contract affirmed. Because SUBSEQUENT_AVOIDANCE_BARRED = Yes, {party_a} cannot now avoid. Because CONTRACT_BINDING = Yes, {party_a} bound by ratified contract.""",
            
            conclusion=f"""Contract BINDING due to valid ratification. Voidable contracts can be ratified with full knowledge and free consent. {party_a}'s written affirmation after discovering influence constitutes valid ratification. Subsequent avoidance barred.""",
            
            alternatives="""- Continuing undue influence → REJECTED: 2 years passed and {party_a} had full knowledge. Influence dissipated. Ratification was with free consent.
- Ratification ineffective → REJECTED: All requirements satisfied (knowledge, consent, unequivocal act). Voidable contracts can be ratified.
- Can still avoid → REJECTED: Valid ratification bars subsequent avoidance. {party_a} made informed choice to affirm.""",
            
            category="voidable_ratification",
            difficulty=2,
            sections=["Section 19", "Ratification"]
        ))
    
    elif scenario_type == 2:
        # Partial performance of void contract
        samples.append(make_sample(
            case_id=f"IND-PARTIAL-VOID-{9200+i}",
            
            facts=f"""{party_a}, aged {age}, purchases goods worth {amount} on credit. {party_a} pays 50% before seller discovers minority. Seller refuses further delivery and demands return of goods already delivered. {party_a} claims right to retain goods based on partial payment.""",
            
            issues="""- Effect of partial performance of void contract?
- Can minor retain goods based on partial payment?
- What are seller's remedies?""",
            
            principles="""- Mohori Bibee: Minor's contract void ab initio
- Partial performance: Doesn't validate void contract
- Restitution: Limited and fact-dependent
- No estoppel against minor""",
            
            reasoning=f"""Step 1 — Contract Status:
{party_a} was {age} at formation
Mohori Bibee: Contract void ab initio
Effect: No contract ever existed

Step 2 — Partial Performance Analysis:
Payment made: 50% of price
Goods delivered: Partial delivery
Question: Does partial performance validate void contract?
Mohori Bibee rule: Void contract remains void regardless of performance
Result: Partial performance doesn't create obligation

Step 3 — Minor's Rights:
Can minor retain goods? No contractual right (no contract)
Restitution: Seller may recover goods if identifiable
Payment made: Not contractual price (no contract to pay price)
Result: No right to retain based on payment

Step 4 — Seller's Remedies:
Contractual remedy: None (no contract)
Restitution: May recover goods delivered
Payment received: Must return 50% paid (unjust enrichment)
Result: Mutual restitution""",
            
            findings=f"""- CONTRACT_VOID: Yes (minor's contract)
- PARTIAL_PERFORMANCE_VALIDATES: No
- CONTRACTUAL_OBLIGATION: No
- MINOR_RIGHT_TO_RETAIN: No
- SELLER_RIGHT_TO_RECOVER_GOODS: Yes
- SELLER_MUST_RETURN_PAYMENT: Yes
- MUTUAL_RESTITUTION_REQUIRED: Yes""",
            
            legal_effect=f"""Because CONTRACT_VOID = Yes, partial performance doesn't create obligation. Because PARTIAL_PERFORMANCE_VALIDATES = No, Mohori Bibee principle applies regardless of performance. Because CONTRACTUAL_OBLIGATION = No, neither party bound. Because MINOR_RIGHT_TO_RETAIN = No and SELLER_RIGHT_TO_RECOVER_GOODS = Yes, seller may recover goods. Because SELLER_MUST_RETURN_PAYMENT = Yes, mutual restitution required.""",
            
            conclusion=f"""Partial performance DOESN'T validate void contract. Mohori Bibee: void ab initio regardless of performance. Seller may recover goods, must return 50% payment. Mutual restitution restores parties to original positions.""",
            
            alternatives="""- Partial performance validates → REJECTED: Mohori Bibee: void contract remains void regardless of performance. No estoppel against minor.
- Minor can retain goods → REJECTED: No contractual right (no contract). Restitution principle allows seller to recover goods.
- Seller keeps payment → REJECTED: No contractual basis to retain payment. Unjust enrichment requires return.""",
            
            category="partial_performance_void",
            difficulty=2,
            sections=["Mohori Bibee", "Restitution"]
        ))
    
    else:
        # Third party rights in void contract
        samples.append(make_sample(
            case_id=f"IND-THIRD-PARTY-{9300+i}",
            
            facts=f"""{party_a}, aged {age}, purchases car worth {amount} from seller. {party_a} sells car to {party_b} (innocent third party) who pays market price. Seller discovers {party_a}'s minority and demands car return from {party_b}. {party_b} argues she is bona fide purchaser for value.""",
            
            issues="""- Can seller recover from innocent third party?
- Does bona fide purchaser defense apply?
- Effect of void contract on subsequent transfers?""",
            
            principles="""- Mohori Bibee: Minor's contract void ab initio
- Nemo dat quod non habet: Cannot transfer better title than possessed
- Void contract: No title passes
- Bona fide purchaser: Requires valid title from transferor""",
            
            reasoning=f"""Step 1 — Original Contract Status:
{party_a} was {age} at purchase
Mohori Bibee: Contract void ab initio
Effect on title: No title passed to {party_a}

Step 2 — Nemo Dat Principle:
Rule: Cannot give what you don't have
{party_a}'s title: None (void contract)
Transfer to {party_b}: Cannot transfer non-existent title
Result: {party_b} acquired no title

Step 3 — Bona Fide Purchaser Defense:
Requirements: (a) Good faith (b) For value (c) Without notice
{party_b}'s status: Good faith, paid value, no notice
Question: Does defense protect against void title?
Answer: No - bona fide purchaser requires valid title from transferor
Result: Defense inapplicable when transferor has no title

Step 4 — Seller's Rights:
Original title: Remains with seller (never passed)
Right to recover: Yes (still owns car)
{party_b}'s position: No title, must return car
{party_b}'s remedy: Claim against {party_a} (not seller)""",
            
            findings=f"""- ORIGINAL_CONTRACT_VOID: Yes
- TITLE_PASSED_TO_MINOR: No
- MINOR_COULD_TRANSFER_TITLE: No
- THIRD_PARTY_ACQUIRED_TITLE: No
- BONA_FIDE_PURCHASER_DEFENSE: Not applicable
- SELLER_RETAINS_TITLE: Yes
- SELLER_CAN_RECOVER: Yes
- THIRD_PARTY_REMEDY: Against minor only""",
            
            legal_effect=f"""Because ORIGINAL_CONTRACT_VOID = Yes, no title passed to {party_a}. Because TITLE_PASSED_TO_MINOR = No, {party_a} had nothing to transfer. Because MINOR_COULD_TRANSFER_TITLE = No (nemo dat principle), {party_b} acquired no title. Because BONA_FIDE_PURCHASER_DEFENSE = Not applicable (requires valid title from transferor), {party_b} not protected. Because SELLER_RETAINS_TITLE = Yes, seller may recover car. Because THIRD_PARTY_REMEDY = Against minor only, {party_b} must claim from {party_a}.""",
            
            conclusion=f"""Seller may RECOVER car from {party_b}. Void contract passes no title (nemo dat). Bona fide purchaser defense inapplicable when transferor has no title. {party_b} must return car, may claim against {party_a}.""",
            
            alternatives="""- Bona fide purchaser protected → REJECTED: Defense requires transferor have valid title. Void contract passes no title (nemo dat principle).
- {party_b} acquired title → REJECTED: Cannot acquire title from one who has none. Mohori Bibee: void contract passes no rights.
- Seller's fault → REJECTED: Seller's inability to verify age doesn't transfer title. Competency is objective requirement.""",
            
            category="third_party_void",
            difficulty=3,
            sections=["Mohori Bibee", "Nemo Dat"]
        ))

# ============================================================================
# CATEGORY 4: Hard Negatives (15 samples)
# ============================================================================

print("Category 4: Hard Negatives (15 samples)...")

for i in range(15):
    party_a = get_name('male')
    party_b = get_name('female')
    amount = get_amount()
    
    if i < 5:
        # Looks like duress but isn't
        samples.append(make_sample(
            case_id=f"IND-HARD-NEG-DURESS-{10000+i}",
            
            facts=f"""{party_a} owes {party_b} {amount} under valid contract. {party_b} threatens to sue unless {party_a} pays within 7 days. {party_a}, facing financial difficulty, borrows from family to pay. Later claims duress, arguing threat of lawsuit forced payment.""",
            
            issues="""- Does threat of lawsuit constitute duress?
- Is payment under threat of legal action voidable?
- Legitimate vs illegitimate pressure?""",
            
            principles="""- Economic Duress: Illegitimate pressure + no alternative + vitiated consent
- Threat of legal action: Generally legitimate if valid claim
- Financial difficulty: Doesn't create duress if obligation valid
- Legitimate commercial pressure vs duress""",
            
            reasoning=f"""Step 1 — Duress Test:
Elements: (a) Illegitimate pressure (b) No alternative (c) Vitiated consent

Step 2 — Pressure Analysis:
Threat: Lawsuit for valid debt
Legal right: {party_b} entitled to sue for breach
Legitimacy: Asserting legal rights = legitimate
Purpose: Collect valid debt (not extract excessive payment)
Result: Legitimate pressure

Step 3 — Alternative Analysis:
{party_a}'s options: (a) Pay debt (b) Face lawsuit
Financial difficulty: {party_a} borrowed from family (alternative existed)
Practical choice: Yes - could have defended lawsuit if debt invalid
Result: Practical alternatives existed

Step 4 — Consent Analysis:
Obligation: Valid debt owed
Pressure: Legitimate assertion of rights
Choice: {party_a} chose to pay rather than litigate
Result: Consent not vitiated""",
            
            findings=f"""- ECONOMIC_DURESS_ESTABLISHED: No
- ILLEGITIMATE_PRESSURE: No (legitimate legal threat)
- VALID_UNDERLYING_OBLIGATION: Yes
- PRACTICAL_ALTERNATIVE_EXISTS: Yes
- FREE_CONSENT: Yes
- PAYMENT_VALID: Yes
- VOIDABLE: No""",
            
            legal_effect=f"""Because ILLEGITIMATE_PRESSURE = No, duress not established. Because VALID_UNDERLYING_OBLIGATION = Yes, {party_b} entitled to assert rights. Because PRACTICAL_ALTERNATIVE_EXISTS = Yes (could have defended if debt invalid), no vitiation of consent. Because FREE_CONSENT = Yes, payment was voluntary. Because PAYMENT_VALID = Yes, {party_a} cannot recover. Because VOIDABLE = No, payment stands.""",
            
            conclusion=f"""Payment VALID, not duress. Threat of lawsuit for valid debt is legitimate pressure. Financial difficulty doesn't create duress when obligation valid. {party_a} cannot recover payment.""",
            
            alternatives="""- Economic duress → REJECTED: Threat of legal action for valid claim is legitimate. Duress requires illegitimate pressure.
- No alternative → REJECTED: {party_a} could have defended lawsuit. Borrowed from family (alternative existed). Financial difficulty ≠ no alternative.
- Vitiated consent → REJECTED: Legitimate commercial pressure doesn't vitiate consent. {party_a} chose to pay valid debt.""",
            
            category="hard_negative_duress",
            difficulty=3,
            sections=["Economic Duress", "Legitimate Pressure"]
        ))
    
    elif i < 10:
        # Looks like undue influence but isn't
        samples.append(make_sample(
            case_id=f"IND-HARD-NEG-INFLUENCE-{10100+i}",
            
            facts=f"""{party_a}, wealthy businessman, gifts {amount} to {party_b}, his personal assistant of 10 years. {party_b} provided exceptional service and loyalty. Gift made after {party_b} received independent legal advice. {party_a}'s family claims undue influence due to employer-employee relationship.""",
            
            issues="""- Undue influence in employer-employee relationship?
- Does long-term employment create dominant position?
- Effect of independent advice?""",
            
            principles="""- Section 16: Dominant position + unfair advantage
- Employer-employee: Not automatically fiduciary
- Independent advice: Rebuts presumption
- Voluntary gift vs exploitation
- Inche Noriah: Presumption can be rebutted""",
            
            reasoning=f"""Step 1 — Section 16 Test:
Elements: (a) Dominant position (b) Unfair advantage

Step 2 — Relationship Analysis:
Relationship: Employer-employee (10 years)
Fiduciary: Not automatic (unlike doctor-patient, lawyer-client)
Dependency: Employment relationship (some dependency)
Question: Does employment create dominant position for Section 16?
Answer: Not automatically - depends on circumstances

Step 3 — Transaction Analysis:
Gift: {amount} for exceptional service
Consideration: Past services (gratuitous gift)
Procedural: Independent legal advice obtained
Substantive: Reasonable gift for long service
Context: Recognition of loyalty and service
Result: No exploitation evident

Step 4 — Independent Advice:
{party_b} received independent legal advice
Effect: Rebuts any presumption of undue influence
Inche Noriah: Independent advice shows voluntariness
Result: Presumption rebutted""",
            
            findings=f"""- UNDUE_INFLUENCE_ESTABLISHED: No
- FIDUCIARY_RELATIONSHIP: No (employer-employee not automatic)
- DOMINANT_POSITION: No (insufficient for Section 16)
- UNFAIR_ADVANTAGE: No
- INDEPENDENT_ADVICE: Yes
- FREE_CONSENT: Yes
- GIFT_VALID: Yes
- VOIDABLE: No""",
            
            legal_effect=f"""Because FIDUCIARY_RELATIONSHIP = No, Inche Noriah presumption doesn't automatically apply. Because DOMINANT_POSITION = No (employer-employee insufficient alone), Section 16 not satisfied. Because INDEPENDENT_ADVICE = Yes, any potential presumption rebutted. Because UNFAIR_ADVANTAGE = No and FREE_CONSENT = Yes, gift was voluntary. Because GIFT_VALID = Yes, family cannot challenge. Because VOIDABLE = No, gift stands.""",
            
            conclusion=f"""Gift VALID, not undue influence. Employer-employee relationship doesn't automatically create dominant position. Independent advice + reasonable gift for long service = voluntary transaction. Family cannot challenge.""",
            
            alternatives="""- Undue influence → REJECTED: Employer-employee not automatically fiduciary. No evidence of exploitation. Independent advice obtained.
- Dominant position → REJECTED: Employment relationship alone insufficient for Section 16. No evidence of psychological dominance or exploitation.
- Inche Noriah presumption → REJECTED: Even if presumed, independent legal advice rebuts presumption. Gift reasonable for 10 years service.""",
            
            category="hard_negative_influence",
            difficulty=3,
            sections=["Section 16", "Independent Advice"]
        ))
    
    else:
        # Looks like void but is voidable
        samples.append(make_sample(
            case_id=f"IND-HARD-NEG-VOID-{10200+i}",
            
            facts=f"""{party_a}, aged 19, enters contract with {party_b} while intoxicated. {party_b} unaware of intoxication. {party_a} appears normal. Contract for {amount}. Next day, {party_a} sobers up and claims contract void due to lack of capacity (intoxication = unsound mind).""",
            
            issues="""- Is intoxication contract void or voidable?
- Does temporary intoxication = unsound mind under Section 12?
- Effect of other party's lack of knowledge?""",
            
            principles="""- Section 12: Unsound mind = inability to understand and form rational judgment
- Temporary vs permanent incapacity
- Intoxication: Voidable if incapacity proven, not automatically void
- Burden on intoxicated party to prove incapacity
- Void vs voidable distinction""",
            
            reasoning=f"""Step 1 — Capacity Analysis:
{party_a}'s age: 19 (major, not minor)
Condition: Intoxicated at contract formation
Question: Does intoxication = void or voidable?

Step 2 — Section 12 Test:
Unsound mind: Inability to understand terms and form rational judgment
Intoxication: Temporary condition (unlike permanent mental illness)
Appeared normal: {party_b} unaware of intoxication
Burden: On {party_a} to prove inability to understand

Step 3 — Void vs Voidable:
Void: Permanent incapacity (minor, permanently unsound mind)
Voidable: Temporary incapacity (intoxication, temporary unsoundness)
Intoxication: Temporary condition → voidable, not void
Rationale: Party can ratify upon sobering up

Step 4 — Effect of Knowledge:
{party_b} unaware of intoxication
{party_a} appeared normal
Effect: If voidable, {party_a} must avoid promptly
Delay: May constitute ratification""",
            
            findings=f"""- PARTY_A_INTOXICATED: Yes
- PERMANENT_INCAPACITY: No (temporary)
- CONTRACT_VOID: No
- CONTRACT_VOIDABLE: Yes (if incapacity proven)
- BURDEN_ON_INTOXICATED_PARTY: Yes
- OTHER_PARTY_KNOWLEDGE: No
- MUST_AVOID_PROMPTLY: Yes
- RATIFICATION_POSSIBLE: Yes""",
            
            legal_effect=f"""Because PERMANENT_INCAPACITY = No, contract not void ab initio. Because CONTRACT_VOIDABLE = Yes (temporary incapacity), {party_a} may avoid if proves inability to understand. Because BURDEN_ON_INTOXICATED_PARTY = Yes, {party_a} must prove incapacity. Because OTHER_PARTY_KNOWLEDGE = No and MUST_AVOID_PROMPTLY = Yes, delay may constitute ratification. Because RATIFICATION_POSSIBLE = Yes, {party_a} must act quickly.""",
            
            conclusion=f"""Contract VOIDABLE, not void. Intoxication is temporary incapacity (unlike minority). {party_a} may avoid if proves inability to understand, but must act promptly. Delay may constitute ratification.""",
            
            alternatives="""- Void contract → REJECTED: Intoxication is temporary incapacity, not permanent like minority. Voidable, not void.
- Automatic avoidance → REJECTED: {party_a} must prove inability to understand. Burden on intoxicated party. Appeared normal suggests capacity.
- No ratification → REJECTED: Voidable contracts can be ratified. Sobering up + delay may constitute ratification.""",
            
            category="hard_negative_void",
            difficulty=3,
            sections=["Section 12", "Void vs Voidable"]
        ))

# ============================================================================
# CATEGORY 5: Short Direct-Answer EOS Cases (10 samples)
# ============================================================================

print("Category 5: Short Direct-Answer EOS (10 samples)...")

for i in range(10):
    party = get_name('male')
    amount = get_amount()
    age = random.choice([14, 15, 16])
    
    samples.append(make_sample(
        case_id=f"IND-SHORT-{11000+i}",
        
        facts=f"""{party}, aged {age}, buys goods worth {amount}. Can seller enforce contract?""",
        
        issues="""- Enforceability of minor's contract?""",
        
        principles="""- Section 11: Minor incompetent
- Mohori Bibee: Minor's contract void ab initio""",
        
        reasoning=f"""Step 1 — Capacity:
{party} is {age} → minor under Section 11

Step 2 — Mohori Bibee:
Minor's contract void ab initio

Step 3 — Enforceability:
Void contract cannot be enforced""",
        
        findings=f"""- MINORITY: Yes
- CONTRACT_VOID: Yes
- ENFORCEABLE: No""",
        
        legal_effect=f"""Because MINORITY = Yes and CONTRACT_VOID = Yes, seller cannot enforce. Because ENFORCEABLE = No, no remedy available.""",
        
        conclusion=f"""NO. Contract void ab initio under Mohori Bibee. Seller cannot enforce.""",
        
        alternatives="""- Enforceable → REJECTED: Mohori Bibee bars enforcement of minor's contracts.""",
        
        category="short_direct",
        difficulty=1,
        sections=["Section 11"]
    ))

# ============================================================================
# Combine with existing dataset
# ============================================================================

print(f"\n{'='*80}")
print("Loading existing dataset...")

with open('legal_reasoning_improved.json', 'r', encoding='utf-8') as f:
    existing_samples = json.load(f)

print(f"Existing samples: {len(existing_samples)}")
print(f"New samples: {len(samples)}")

combined_samples = existing_samples + samples

print(f"Total samples: {len(combined_samples)}")

# Save combined dataset
with open('legal_reasoning_final.json', 'w', encoding='utf-8') as f:
    json.dump(combined_samples, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print("✓ COMPLETE! Extended dataset saved to legal_reasoning_final.json")
print(f"\nFinal Dataset Statistics:")
print(f"  Total samples: {len(combined_samples)}")
print(f"\nNew samples breakdown:")
print(f"  Role-binding duress: 30")
print(f"  Role-binding undue influence: 25")
print(f"  Void/voidable consequences: 20")
print(f"  Hard negatives: 15")
print(f"  Short direct EOS: 10")
print(f"\n{'='*80}")
print("✅ Production-ready dataset with 200 samples!")
