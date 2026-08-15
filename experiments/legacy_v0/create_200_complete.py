"""
Generate complete 200-sample section-marked legal reasoning dataset
Distribution: Contract 80 | Tort 40 | Criminal 30 | Corporate 30 | Evidence 20
"""
import json

def make_sample(case_id, facts, issues, principles, role_binding, doctrine_routing, 
                fact_findings, legal_effect, final_answer, category, difficulty):
    input_text = f"CASE_ID: {case_id}\n\nFACTS:\n{facts}\n\nISSUES:\n{issues}\n\nAPPLICABLE PRINCIPLES:\n{principles}"
    output_text = f"""<ROLE_BINDING>
{role_binding}
</ROLE_BINDING>

<DOCTRINE_ROUTING>
{doctrine_routing}
</DOCTRINE_ROUTING>

<FACT_FINDINGS>
{fact_findings}
</FACT_FINDINGS>

<LEGAL_EFFECT>
{legal_effect}
</LEGAL_EFFECT>

<FINAL_ANSWER>
{final_answer}
</FINAL_ANSWER>
<|end_of_text|>"""
    return {
        "input": input_text,
        "output": output_text,
        "metadata": {"case_id": case_id, "category": category, "difficulty": difficulty, "jurisdiction": "India"}
    }

samples = []
print("Generating 200 section-marked legal reasoning samples...")
print("=" * 80)

# CONTRACT LAW (80 samples)
print("\n[1/5] Contract Law (80 samples)")

# Economic Duress - 20 pairs (40 samples)
print("  - Economic Duress (40 samples: 20 established, 20 negative)")
for i in range(20):
    # Established
    samples.append(make_sample(
        case_id=f"IND-DURESS-EST-{1000+i}",
        facts=f"Company A and Company B have existing supply contract for specialized components at ₹{100+i*5} per unit (annual value ₹{50+i*2} crore). Mid-contract, Company A threatens to stop deliveries unless Company B pays only ₹{60+i*3} per unit ({40-i}% reduction). Company B's manufacturing depends entirely on these components. No alternative supplier available. Switching would require {9+i%5} months retooling at ₹{8+i%3} crore cost, causing production shutdown and bankruptcy. Company B signs under protest.",
        issues="- Is economic duress established?\n- Is undue influence applicable?\n- Is modification valid?",
        principles="- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent\n- Undue Influence: Relationship-based dominance\n- Duress vs Influence: Threat vs relationship",
        role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nWHOSE_CONSENT_MATTERS: Company B",
        doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Economic Duress\nREASON_FOR_SELECTION: Immediate threat with no practical alternative.\nREJECTED_DOCTRINE: Undue Influence\nREASON_REJECTED: Commercial dependency is not relationship dominance.",
        fact_findings=f"IMMEDIATE_THREAT: Yes\nNO_PRACTICAL_ALTERNATIVE: Yes\nSWITCHING_COST: ₹{8+i%3} crore\nSWITCHING_TIME: {9+i%5} months\nBANKRUPTCY_RISK: Yes\nFREE_CONSENT: No\nMODIFICATION_VALID: No",
        legal_effect="Because IMMEDIATE_THREAT = Yes and NO_PRACTICAL_ALTERNATIVE = Yes, economic duress is established.\nBecause FREE_CONSENT = No, modification is voidable.",
        final_answer="Economic duress established. Modification voidable.",
        category="economic_duress",
        difficulty=2
    ))
    
    # Not established
    samples.append(make_sample(
        case_id=f"IND-DURESS-NEG-{2000+i}",
        facts=f"Company A and Company B have supply contract for standard components at ₹{50+i*2} per unit (annual value ₹{10+i} crore). Company A threatens to stop deliveries unless Company B accepts ₹{40+i} per unit ({20-i%5}% reduction). Company B has {3+i%3} other qualified suppliers. Switching requires only updating purchase orders, completed within {1+i%3} weeks with no retooling cost. Company B agrees to avoid hassle.",
        issues="- Is economic duress established?\n- Does alternative availability matter?\n- Is modification valid?",
        principles="- Economic Duress: Requires no practical alternative\n- Practical alternative test\n- Convenience vs necessity",
        role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nWHOSE_CONSENT_MATTERS: Company B",
        doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Economic Duress (not established)\nREASON_FOR_SELECTION: Threat scenario but elements not met.",
        fact_findings=f"IMMEDIATE_THREAT: Yes\nPRACTICAL_ALTERNATIVE_EXISTS: Yes ({3+i%3} suppliers, {1+i%3} weeks)\nCONVENIENCE_NOT_NECESSITY: Yes\nFREE_CONSENT: Yes\nMODIFICATION_VALID: Yes",
        legal_effect="Because PRACTICAL_ALTERNATIVE_EXISTS = Yes, no-alternative element fails.\nBecause CONVENIENCE_NOT_NECESSITY = Yes, agreement was voluntary.\nBecause FREE_CONSENT = Yes, modification is enforceable.",
        final_answer="Economic duress not established. Modification valid.",
        category="economic_duress_negative",
        difficulty=2
    ))

# Undue Influence (10 samples)
print("  - Undue Influence (10 samples)")
relationships = [
    ("Dr. Sharma", "patient Ramesh", "doctor-patient", "₹2 crore property", "78, illiterate, terminal illness"),
    ("Lawyer Gupta", "client Sunita", "lawyer-client", "₹5 crore estate", "elderly widow"),
    ("Guru Anand", "devotee Priya", "spiritual advisor-devotee", "₹3 crore donation", "isolated follower"),
    ("Trustee Kapoor", "beneficiary Amit", "trustee-beneficiary", "₹4 crore trust assets", "young, inexperienced"),
    ("Guardian Mehta", "ward Kavita", "guardian-ward", "₹1.5 crore inheritance", "orphan, dependent"),
    ("Elder brother Raj", "sister Neha", "family dominance", "₹2.5 crore land", "uneducated, dependent"),
    ("Employer Singh", "employee Rohan", "employer-employee", "₹50 lakh loan waiver", "debt-ridden employee"),
    ("Teacher Verma", "student Divya", "teacher-student", "₹1 crore gift", "impressionable student"),
    ("Doctor Patel", "patient Kumar", "doctor-patient", "₹3.5 crore villa", "85 years, dementia"),
    ("Swami Ji", "follower Asha", "spiritual authority", "₹4.5 crore donation", "devoted, isolated")
]

for i, (dominant, vulnerable, relationship, benefit, vulnerability) in enumerate(relationships):
    samples.append(make_sample(
        case_id=f"IND-INFLUENCE-{3000+i}",
        facts=f"{dominant} in {relationship} relationship with {vulnerable} ({vulnerability}) persuades transfer of {benefit}. No independent legal/financial advice. Family challenges transfer.",
        issues="- Is undue influence established?\n- Is economic duress applicable?\n- Is transfer valid?",
        principles="- Undue Influence: Dominant position + unfair advantage + no independent advice\n- Fiduciary relationships create presumption\n- Economic Duress: Threat-based, not relationship-based",
        role_binding=f"DOMINANT_PARTY: {dominant}\nVULNERABLE_PARTY: {vulnerable}\nCHALLENGING_PARTY: Family\nWHOSE_CONSENT_MATTERS: {vulnerable}",
        doctrine_routing="PRIMARY_DOCTRINE: Undue Influence\nBEST_FRAMEWORK: Undue Influence\nREASON_FOR_SELECTION: Fiduciary relationship creates dominance.\nREJECTED_DOCTRINE: Economic Duress\nREASON_REJECTED: No threat. Relationship exploitation, not coercion.",
        fact_findings=f"FIDUCIARY_RELATIONSHIP: Yes ({relationship})\nDOMINANT_POSITION: Yes\nVULNERABLE_STATUS: Yes ({vulnerability})\nUNFAIR_ADVANTAGE: Yes ({benefit})\nINDEPENDENT_ADVICE: No\nFREE_CONSENT: No\nTRANSFER_VALID: No",
        legal_effect="Because FIDUCIARY_RELATIONSHIP = Yes and DOMINANT_POSITION = Yes, presumption arises.\nBecause INDEPENDENT_ADVICE = No and UNFAIR_ADVANTAGE = Yes, presumption not rebutted.\nBecause FREE_CONSENT = No, transfer is voidable.",
        final_answer="Undue influence established. Transfer voidable.",
        category="undue_influence",
        difficulty=2
    ))

# Void vs Voidable (15 samples: 10 void, 5 voidable)
print("  - Void vs Voidable (15 samples)")
for i in range(10):
    samples.append(make_sample(
        case_id=f"IND-VOID-{4000+i}",
        facts=f"Minor ({16+i%2}) purchases goods worth ₹{40+i*5} lakh using fake ID showing age 22. Seller unaware of minority. After delivery, minor refuses payment claiming minority. Seller argues contract should be voidable not void.",
        issues="- Is contract void ab initio or voidable?\n- Does seller's ignorance matter?\n- Can seller claim restitution?",
        principles="- Section 11: Minor incompetent to contract\n- Mohori Bibee: Minor's contract void ab initio\n- Void vs Voidable: Void = no contract; Voidable = valid until avoided",
        role_binding="INCOMPETENT_PARTY: Minor\nOTHER_PARTY: Seller\nCHALLENGING_PARTY: Minor\nWHOSE_CAPACITY_MATTERS: Minor",
        doctrine_routing="PRIMARY_DOCTRINE: Void ab initio\nBEST_FRAMEWORK: Void ab initio\nREASON_FOR_SELECTION: No competent party = no valid contract.\nREJECTED_DOCTRINE: Voidable\nREASON_REJECTED: Voidable requires valid contract first.",
        fact_findings=f"MINORITY_ESTABLISHED: Yes ({16+i%2} years)\nCONTRACTUAL_CAPACITY: No\nVALID_CONTRACT_FORMED: No\nVOID_AB_INITIO: Yes\nVOIDABLE_APPLIES: No\nCONTRACTUAL_REMEDY: No\nRESTITUTION: Limited/fact-dependent",
        legal_effect="Because CONTRACTUAL_CAPACITY = No, no valid contract formed.\nBecause VALID_CONTRACT_FORMED = No, voidable doctrine cannot apply.\nBecause VOID_AB_INITIO = Yes, seller cannot enforce payment.",
        final_answer="Contract void ab initio. Seller cannot enforce payment.",
        category="void",
        difficulty=2
    ))

for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-VOIDABLE-{5000+i}",
        facts=f"Seller fraudulently misrepresents property condition to Buyer through false documents. Buyer discovers fraud after purchase. Both parties competent adults.",
        issues="- Is contract void or voidable?\n- Can Buyer rescind?\n- What remedies available?",
        principles="- Fraud vitiates consent but doesn't void contract\n- Voidable: Valid until avoided\n- Void: No contract from inception",
        role_binding="DECEIVING_PARTY: Seller\nDECEIVED_PARTY: Buyer\nCHALLENGING_PARTY: Buyer\nWHOSE_CONSENT_MATTERS: Buyer",
        doctrine_routing="PRIMARY_DOCTRINE: Voidable contract\nBEST_FRAMEWORK: Voidable\nREASON_FOR_SELECTION: Valid contract with vitiated consent.\nREJECTED_DOCTRINE: Void ab initio\nREASON_REJECTED: Both parties competent. Contract validly formed.",
        fact_findings="COMPETENT_PARTIES: Yes\nVALID_CONTRACT_FORMED: Yes\nFRAUD_ESTABLISHED: Yes\nCONSENT_VITIATED: Yes\nVOID_AB_INITIO: No\nVOIDABLE: Yes\nRESCISSION_AVAILABLE: Yes",
        legal_effect="Because COMPETENT_PARTIES = Yes, valid contract was formed.\nBecause FRAUD_ESTABLISHED = Yes, consent was vitiated.\nBecause VOIDABLE = Yes, Buyer can rescind.",
        final_answer="Contract voidable, not void. Buyer can rescind.",
        category="voidable",
        difficulty=2
    ))

# Fraud vs Misrepresentation (10 samples: 5 each)
print("  - Fraud vs Misrepresentation (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-FRAUD-{6000+i}",
        facts=f"Seller knowingly sells defective machinery, actively concealing defects and providing false inspection reports. Buyer discovers defects after installation.",
        issues="- Is fraud or misrepresentation established?\n- Does intent matter?\n- What remedies available?",
        principles="- Fraud: False representation + knowledge + intent to deceive\n- Misrepresentation: False representation without intent\n- Intent distinguishes fraud from misrepresentation",
        role_binding="DECEIVING_PARTY: Seller\nDECEIVED_PARTY: Buyer\nCHALLENGING_PARTY: Buyer\nWHOSE_CONSENT_MATTERS: Buyer",
        doctrine_routing="PRIMARY_DOCTRINE: Fraud\nBEST_FRAMEWORK: Fraud\nREASON_FOR_SELECTION: Active concealment + false reports = intent.\nREJECTED_DOCTRINE: Innocent Misrepresentation\nREASON_REJECTED: Knowingly providing false reports negates innocence.",
        fact_findings="FALSE_REPRESENTATION: Yes\nKNOWLEDGE_OF_FALSITY: Yes\nINTENT_TO_DECEIVE: Yes\nINNOCENT_MISREPRESENTATION: No\nFRAUD_ESTABLISHED: Yes\nFREE_CONSENT: No\nCONTRACT_VOIDABLE: Yes\nDAMAGES_AVAILABLE: Yes",
        legal_effect="Because KNOWLEDGE_OF_FALSITY = Yes and INTENT_TO_DECEIVE = Yes, fraud is established.\nBecause FRAUD_ESTABLISHED = Yes, Buyer can claim rescission and damages.",
        final_answer="Fraud established. Rescission and damages available.",
        category="fraud",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-MISREP-{7000+i}",
        facts=f"Seller genuinely believes property is {2000+i*100} sq ft based on old documents. Actually {1800+i*100} sq ft. Buyer discovers discrepancy.",
        issues="- Is fraud or misrepresentation established?\n- Does honest belief matter?\n- What remedies available?",
        principles="- Misrepresentation: False representation without intent\n- Fraud requires intent to deceive\n- Honest belief negates fraud",
        role_binding="REPRESENTING_PARTY: Seller\nRELYING_PARTY: Buyer\nCHALLENGING_PARTY: Buyer\nWHOSE_CONSENT_MATTERS: Buyer",
        doctrine_routing="PRIMARY_DOCTRINE: Innocent Misrepresentation\nBEST_FRAMEWORK: Misrepresentation\nREASON_FOR_SELECTION: Honest belief based on available information.\nREJECTED_DOCTRINE: Fraud\nREASON_REJECTED: No intent to deceive. Genuine mistake.",
        fact_findings="FALSE_REPRESENTATION: Yes\nHONEST_BELIEF: Yes\nINTENT_TO_DECEIVE: No\nFRAUD_ESTABLISHED: No\nMISREPRESENTATION_ESTABLISHED: Yes\nRESCISSION_AVAILABLE: Yes\nDAMAGES_AVAILABLE: No",
        legal_effect="Because HONEST_BELIEF = Yes and INTENT_TO_DECEIVE = No, fraud not established.\nBecause FALSE_REPRESENTATION = Yes, misrepresentation is established.\nBecause MISREPRESENTATION_ESTABLISHED = Yes, rescission available but not damages.",
        final_answer="Innocent misrepresentation established. Rescission available, not damages.",
        category="misrepresentation",
        difficulty=2
    ))

# Coercion (5 samples)
print("  - Coercion (5 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-COERCION-{8000+i}",
        facts=f"Creditor threatens criminal complaint for civil debt of ₹{10+i*5} lakh unless debtor pays immediately. Debtor pays under protest to avoid criminal proceedings.",
        issues="- Is coercion established?\n- Is threat of criminal complaint legitimate?\n- Can payment be recovered?",
        principles="- Section 15: Coercion requires IPC-forbidden act\n- Threat of criminal complaint for civil debt = coercion\n- Legitimate vs illegitimate pressure",
        role_binding="THREATENING_PARTY: Creditor\nTHREATENED_PARTY: Debtor\nWHOSE_CONSENT_MATTERS: Debtor",
        doctrine_routing="PRIMARY_DOCTRINE: Coercion\nBEST_FRAMEWORK: Coercion\nREASON_FOR_SELECTION: Criminal threat for civil debt is illegitimate.\nREJECTED_DOCTRINE: Legitimate Pressure\nREASON_REJECTED: Criminal threat exceeds legitimate pressure.",
        fact_findings="THREAT_MADE: Yes (criminal complaint)\nCIVIL_DEBT: Yes\nILLEGITIMATE_PRESSURE: Yes\nCOERCION_ESTABLISHED: Yes\nFREE_CONSENT: No\nPAYMENT_VOIDABLE: Yes",
        legal_effect="Because THREAT_MADE = Yes and CIVIL_DEBT = Yes, threat is illegitimate.\nBecause ILLEGITIMATE_PRESSURE = Yes, coercion is established.\nBecause FREE_CONSENT = No, payment is voidable.",
        final_answer="Coercion established. Payment voidable.",
        category="coercion",
        difficulty=2
    ))

print(f"  ✓ Contract Law complete: {len([s for s in samples if any(x in s['metadata']['category'] for x in ['duress', 'influence', 'void', 'voidable', 'fraud', 'misrep', 'coercion'])])} samples")

# TORT LAW (40 samples)
print("\n[2/5] Tort Law (40 samples)")

# Negligence (20 samples: 10 established, 10 not)
print("  - Negligence (20 samples)")
for i in range(10):
    samples.append(make_sample(
        case_id=f"IND-TORT-NEG-{10000+i}",
        facts=f"Doctor performs surgery without sterilizing instruments. Patient develops severe infection requiring additional treatment. Standard protocol mandates sterilization.",
        issues="- Is negligence established?\n- Was duty breached?\n- Is causation proven?",
        principles="- Negligence: Duty + Breach + Causation + Damage\n- Professional standard: Bolam test\n- Causation: But-for test",
        role_binding="DUTY_HOLDER: Doctor\nRIGHT_HOLDER: Patient\nINJURED_PARTY: Patient\nLIABLE_PARTY: Doctor",
        doctrine_routing="PRIMARY_DOCTRINE: Negligence\nBEST_FRAMEWORK: Negligence\nREASON_FOR_SELECTION: Professional duty breach with causation.",
        fact_findings="DUTY_OF_CARE: Yes (doctor-patient)\nSTANDARD_PROTOCOL: Yes (sterilization required)\nBREACH: Yes (no sterilization)\nCAUSATION: Yes (infection from unsterilized instruments)\nDAMAGE: Yes (severe infection)\nNEGLIGENCE_ESTABLISHED: Yes",
        legal_effect="Because DUTY_OF_CARE = Yes and BREACH = Yes, duty was breached.\nBecause CAUSATION = Yes and DAMAGE = Yes, negligence is established.\nBecause NEGLIGENCE_ESTABLISHED = Yes, Doctor is liable.",
        final_answer="Negligence established. Doctor liable.",
        category="negligence",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-TORT-NEG-NO-{11000+i}",
        facts=f"Doctor follows all standard protocols. Patient suffers rare complication (1 in 10,000). Complication unavoidable even with proper care. Expert testimony confirms standard met.",
        issues="- Is negligence established?\n- Does bad outcome = negligence?\n- Was standard of care met?",
        principles="- Negligence requires breach of duty\n- Bad outcome alone insufficient\n- Standard of care: Reasonable professional",
        role_binding="DUTY_HOLDER: Doctor\nRIGHT_HOLDER: Patient\nINJURED_PARTY: Patient\nALLEGED_LIABLE_PARTY: Doctor",
        doctrine_routing="PRIMARY_DOCTRINE: Negligence (not established)\nBEST_FRAMEWORK: No negligence\nREASON_FOR_SELECTION: Standard of care met despite bad outcome.",
        fact_findings="DUTY_OF_CARE: Yes\nSTANDARD_PROTOCOL_FOLLOWED: Yes\nBREACH: No\nBAD_OUTCOME: Yes\nCAUSATION_BY_BREACH: No\nNEGLIGENCE_ESTABLISHED: No",
        legal_effect="Because STANDARD_PROTOCOL_FOLLOWED = Yes, no breach occurred.\nBecause BREACH = No, negligence is not established.\nBecause BAD_OUTCOME = Yes but CAUSATION_BY_BREACH = No, Doctor not liable.",
        final_answer="Negligence not established. Bad outcome alone insufficient.",
        category="negligence_negative",
        difficulty=2
    ))

# Strict Liability (10 samples)
print("  - Strict Liability (10 samples)")
for i in range(10):
    samples.append(make_sample(
        case_id=f"IND-TORT-STRICT-{12000+i}",
        facts=f"Factory stores hazardous chemicals. Leak occurs causing damage to neighboring properties. Factory followed all safety regulations and obtained permits.",
        issues="- Is strict liability applicable?\n- Does compliance with regulations matter?\n- Is fault required?",
        principles="- Strict Liability: Dangerous activity + escape + damage\n- Rylands v Fletcher: Non-natural use\n- No fault required for strict liability",
        role_binding="ACTIVITY_CONDUCTOR: Factory\nINJURED_PARTY: Neighbors\nLIABLE_PARTY: Factory",
        doctrine_routing="PRIMARY_DOCTRINE: Strict Liability\nBEST_FRAMEWORK: Strict Liability\nREASON_FOR_SELECTION: Hazardous activity with escape.\nREJECTED_DOCTRINE: Negligence\nREASON_REJECTED: Fault not required for dangerous activities.",
        fact_findings="DANGEROUS_ACTIVITY: Yes (hazardous chemicals)\nESCAPE: Yes (leak)\nDAMAGE: Yes (neighboring properties)\nCOMPLIANCE_WITH_REGULATIONS: Yes\nFAULT_REQUIRED: No\nSTRICT_LIABILITY_APPLIES: Yes",
        legal_effect="Because DANGEROUS_ACTIVITY = Yes and ESCAPE = Yes, strict liability applies.\nBecause STRICT_LIABILITY_APPLIES = Yes, fault is not required.\nBecause COMPLIANCE_WITH_REGULATIONS = Yes but STRICT_LIABILITY_APPLIES = Yes, Factory still liable.",
        final_answer="Strict liability applies. Factory liable despite compliance.",
        category="strict_liability",
        difficulty=2
    ))

# Vicarious Liability (10 samples)
print("  - Vicarious Liability (10 samples)")
for i in range(10):
    samples.append(make_sample(
        case_id=f"IND-TORT-VICARIOUS-{13000+i}",
        facts=f"Employee driver causes accident while delivering goods for employer during working hours. Victim sues employer for damages.",
        issues="- Is employer vicariously liable?\n- Was act in course of employment?\n- Does employer's fault matter?",
        principles="- Vicarious Liability: Employer liable for employee's tort in course of employment\n- Course of employment test\n- Employer's personal fault not required",
        role_binding="TORTFEASOR: Employee driver\nEMPLOYER: Employer\nVICTIM: Accident victim\nVICARIOUSLY_LIABLE_PARTY: Employer",
        doctrine_routing="PRIMARY_DOCTRINE: Vicarious Liability\nBEST_FRAMEWORK: Vicarious Liability\nREASON_FOR_SELECTION: Employee tort in course of employment.",
        fact_findings="EMPLOYMENT_RELATIONSHIP: Yes\nTORT_BY_EMPLOYEE: Yes (accident)\nCOURSE_OF_EMPLOYMENT: Yes (delivering goods)\nWORKING_HOURS: Yes\nEMPLOYER_PERSONAL_FAULT: No\nVICARIOUS_LIABILITY_APPLIES: Yes",
        legal_effect="Because EMPLOYMENT_RELATIONSHIP = Yes and COURSE_OF_EMPLOYMENT = Yes, vicarious liability applies.\nBecause VICARIOUS_LIABILITY_APPLIES = Yes, employer liable.\nBecause EMPLOYER_PERSONAL_FAULT = No but VICARIOUS_LIABILITY_APPLIES = Yes, employer still liable.",
        final_answer="Employer vicariously liable. Personal fault not required.",
        category="vicarious_liability",
        difficulty=2
    ))

print(f"  ✓ Tort Law complete: {len([s for s in samples if 'tort' in s['metadata']['case_id'].lower()])} samples")

# CRIMINAL LAW (30 samples)
print("\n[3/5] Criminal Law (30 samples)")

# Intention vs Knowledge (10 samples: 5 each)
print("  - Intention vs Knowledge (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-CRIM-INTENT-{14000+i}",
        facts=f"A plans to kill B. Purchases weapon, conducts surveillance, waits at B's residence, shoots B when B arrives. B dies from gunshot wound.",
        issues="- Is intention established?\n- Is knowledge sufficient?\n- What is the mens rea?",
        principles="- Intention: Purpose to cause result\n- Knowledge: Awareness result will follow\n- Intention vs Knowledge: Intention requires purpose",
        role_binding="ACCUSED: A\nVICTIM: B\nMENS_REA_HOLDER: A",
        doctrine_routing="PRIMARY_DOCTRINE: Intention (Murder)\nBEST_FRAMEWORK: Intention\nREASON_FOR_SELECTION: Planned killing with purpose.\nREJECTED_DOCTRINE: Knowledge only\nREASON_REJECTED: Planning and surveillance shows purpose, not mere awareness.",
        fact_findings="PLANNING: Yes (weapon, surveillance)\nPURPOSE_TO_KILL: Yes\nINTENTION_ESTABLISHED: Yes\nKNOWLEDGE_ONLY: No\nMURDER_MENS_REA: Yes",
        legal_effect="Because PLANNING = Yes and PURPOSE_TO_KILL = Yes, intention is established.\nBecause INTENTION_ESTABLISHED = Yes, murder mens rea is proven.",
        final_answer="Intention established. Murder mens rea proven.",
        category="intention",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-CRIM-KNOWLEDGE-{15000+i}",
        facts=f"A throws heavy stone from tall building knowing people walk below. Stone hits B causing death. A did not intend to kill specific person but knew death likely.",
        issues="- Is intention or knowledge established?\n- Does lack of specific target matter?\n- What is the mens rea?",
        principles="- Intention: Purpose to cause result\n- Knowledge: Awareness result likely\n- Knowledge sufficient for culpable homicide",
        role_binding="ACCUSED: A\nVICTIM: B\nMENS_REA_HOLDER: A",
        doctrine_routing="PRIMARY_DOCTRINE: Knowledge (Culpable Homicide)\nBEST_FRAMEWORK: Knowledge\nREASON_FOR_SELECTION: Awareness of likely result without specific purpose.\nREJECTED_DOCTRINE: Intention\nREASON_REJECTED: No specific purpose to kill particular person.",
        fact_findings="AWARENESS_OF_RISK: Yes (knew people below)\nPURPOSE_TO_KILL_SPECIFIC_PERSON: No\nKNOWLEDGE_ESTABLISHED: Yes\nINTENTION_ESTABLISHED: No\nCULPABLE_HOMICIDE_MENS_REA: Yes",
        legal_effect="Because AWARENESS_OF_RISK = Yes and PURPOSE_TO_KILL_SPECIFIC_PERSON = No, knowledge is established.\nBecause KNOWLEDGE_ESTABLISHED = Yes but INTENTION_ESTABLISHED = No, culpable homicide not murder.",
        final_answer="Knowledge established, not intention. Culpable homicide, not murder.",
        category="knowledge",
        difficulty=2
    ))

# Preparation vs Attempt (10 samples: 5 each)
print("  - Preparation vs Attempt (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-CRIM-ATTEMPT-{16000+i}",
        facts=f"A enters B's house with loaded weapon intending to kill B. B not home. A caught waiting inside by police.",
        issues="- Is attempt established?\n- Is this mere preparation?\n- What is the actus reus?",
        principles="- Attempt: Act proximate to completion\n- Preparation: Remote acts\n- Proximity test: How close to completion",
        role_binding="ACCUSED: A\nINTENDED_VICTIM: B\nACTUS_REUS_PERFORMER: A",
        doctrine_routing="PRIMARY_DOCTRINE: Attempt\nBEST_FRAMEWORK: Attempt\nREASON_FOR_SELECTION: Entered victim's house with weapon - proximate act.\nREJECTED_DOCTRINE: Mere Preparation\nREASON_REJECTED: Entering victim's house with weapon exceeds preparation.",
        fact_findings="ENTERED_VICTIM_LOCATION: Yes\nWEAPON_PRESENT: Yes (loaded)\nPROXIMATE_TO_COMPLETION: Yes\nMERE_PREPARATION: No\nATTEMPT_ESTABLISHED: Yes",
        legal_effect="Because ENTERED_VICTIM_LOCATION = Yes and WEAPON_PRESENT = Yes, act is proximate.\nBecause PROXIMATE_TO_COMPLETION = Yes, attempt is established.",
        final_answer="Attempt established. Proximate act proven.",
        category="attempt",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-CRIM-PREP-{17000+i}",
        facts=f"A purchases weapon intending to kill B. Weapon stored at home. No surveillance or approach to victim. No further action taken.",
        issues="- Is attempt established?\n- Is this mere preparation?\n- What is the actus reus?",
        principles="- Attempt: Act proximate to completion\n- Preparation: Remote acts\n- Purchasing weapon alone is preparation",
        role_binding="ACCUSED: A\nINTENDED_VICTIM: B\nACTUS_REUS_PERFORMER: A",
        doctrine_routing="PRIMARY_DOCTRINE: Mere Preparation\nBEST_FRAMEWORK: Preparation\nREASON_FOR_SELECTION: Weapon purchase without further action is remote.\nREJECTED_DOCTRINE: Attempt\nREASON_REJECTED: No proximate act toward victim.",
        fact_findings="WEAPON_PURCHASED: Yes\nFURTHER_ACTION: No\nPROXIMATE_TO_COMPLETION: No\nMERE_PREPARATION: Yes\nATTEMPT_ESTABLISHED: No",
        legal_effect="Because WEAPON_PURCHASED = Yes but FURTHER_ACTION = No, act is remote.\nBecause PROXIMATE_TO_COMPLETION = No, attempt is not established.",
        final_answer="Mere preparation. Attempt not established.",
        category="preparation",
        difficulty=2
    ))

# Common Intention vs Common Object (10 samples: 5 each)
print("  - Common Intention vs Common Object (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-CRIM-COMMON-INT-{18000+i}",
        facts=f"A and B plan to rob bank. Both enter bank together. A holds gun and threatens staff, B collects money. Security guard shot by A during robbery.",
        issues="- Is common intention established?\n- Is B liable for shooting?\n- What is the shared mens rea?",
        principles="- Common Intention (Section 34): Pre-arranged plan + participation\n- All liable for acts in furtherance\n- Shared mens rea required",
        role_binding="PRINCIPAL_ACTOR: A (shooter)\nCO_PARTICIPANT: B\nVICTIM: Security guard\nSHARED_MENS_REA_HOLDERS: A and B",
        doctrine_routing="PRIMARY_DOCTRINE: Common Intention (Section 34)\nBEST_FRAMEWORK: Common Intention\nREASON_FOR_SELECTION: Pre-arranged plan with participation.",
        fact_findings="PRE_ARRANGED_PLAN: Yes (planned robbery)\nPARTICIPATION_BY_BOTH: Yes\nACT_IN_FURTHERANCE: Yes (shooting during robbery)\nCOMMON_INTENTION_ESTABLISHED: Yes\nB_LIABLE_FOR_SHOOTING: Yes",
        legal_effect="Because PRE_ARRANGED_PLAN = Yes and PARTICIPATION_BY_BOTH = Yes, common intention is established.\nBecause ACT_IN_FURTHERANCE = Yes, shooting is within common intention.\nBecause COMMON_INTENTION_ESTABLISHED = Yes, B liable for A's act.",
        final_answer="Common intention established. B liable for shooting.",
        category="common_intention",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-CRIM-COMMON-OBJ-{19000+i}",
        facts=f"Five persons assemble to protest. No pre-arranged plan for violence. During protest, one member assaults police officer. Others present but did not participate in assault.",
        issues="- Is common object established?\n- Are all members liable?\n- Is pre-arrangement required?",
        principles="- Common Object (Section 149): Unlawful assembly + shared object\n- No pre-arrangement required\n- Liable for acts in prosecution of common object",
        role_binding="PRINCIPAL_ACTOR: One member\nCO_MEMBERS: Other four\nVICTIM: Police officer\nASSEMBLY_MEMBERS: All five",
        doctrine_routing="PRIMARY_DOCTRINE: Common Object (Section 149)\nBEST_FRAMEWORK: Common Object\nREASON_FOR_SELECTION: Unlawful assembly without pre-arrangement.\nREJECTED_DOCTRINE: Common Intention\nREASON_REJECTED: No pre-arranged plan proven.",
        fact_findings="UNLAWFUL_ASSEMBLY: Yes (5+ persons)\nPRE_ARRANGED_PLAN: No\nCOMMON_OBJECT: Yes (protest)\nACT_IN_PROSECUTION: Yes (assault during protest)\nALL_MEMBERS_LIABLE: Yes",
        legal_effect="Because UNLAWFUL_ASSEMBLY = Yes and COMMON_OBJECT = Yes, Section 149 applies.\nBecause ACT_IN_PROSECUTION = Yes, all members liable.\nBecause PRE_ARRANGED_PLAN = No, common intention does not apply but common object does.",
        final_answer="Common object established. All members liable.",
        category="common_object",
        difficulty=2
    ))

print(f"  ✓ Criminal Law complete: {len([s for s in samples if 'crim' in s['metadata']['case_id'].lower()])} samples")

# CORPORATE LAW (30 samples)
print("\n[4/5] Corporate Law (30 samples)")

# Director Fiduciary Duty (15 samples)
print("  - Director Fiduciary Duty (15 samples)")
for i in range(15):
    samples.append(make_sample(
        case_id=f"IND-CORP-DUTY-{20000+i}",
        facts=f"Director diverts company opportunity worth ₹{5+i} crore to personal company without disclosure to board. Company discovers diversion and sues director.",
        issues="- Is fiduciary duty breached?\n- Is disclosure required?\n- What remedies available?",
        principles="- Director's fiduciary duty: Act in company's interest\n- Corporate opportunity doctrine\n- Disclosure requirement for conflicts",
        role_binding="DUTY_HOLDER: Director\nRIGHT_HOLDER: Company\nBENEFITED_PARTY: Director's personal company\nINJURED_PARTY: Company",
        doctrine_routing="PRIMARY_DOCTRINE: Fiduciary Duty Breach\nBEST_FRAMEWORK: Corporate Opportunity Doctrine\nREASON_FOR_SELECTION: Director diverted company opportunity.",
        fact_findings="FIDUCIARY_RELATIONSHIP: Yes (director-company)\nCORPORATE_OPPORTUNITY: Yes\nDISCLOSURE_MADE: No\nPERSONAL_BENEFIT: Yes\nDUTY_BREACH: Yes\nREMEDY_AVAILABLE: Yes (disgorgement)",
        legal_effect="Because FIDUCIARY_RELATIONSHIP = Yes and CORPORATE_OPPORTUNITY = Yes, duty to disclose arises.\nBecause DISCLOSURE_MADE = No and PERSONAL_BENEFIT = Yes, duty is breached.\nBecause DUTY_BREACH = Yes, company can claim disgorgement of profits.",
        final_answer="Fiduciary duty breached. Disgorgement of profits available.",
        category="director_duty",
        difficulty=2
    ))

# Piercing Corporate Veil (15 samples)
print("  - Piercing Corporate Veil (15 samples)")
for i in range(15):
    samples.append(make_sample(
        case_id=f"IND-CORP-VEIL-{21000+i}",
        facts=f"Company incorporated solely to evade personal liability. Director transfers personal assets to company, then declares personal bankruptcy. Creditors seek to pierce veil to reach company assets for ₹{20+i*2} lakh personal debt.",
        issues="- Can corporate veil be pierced?\n- Is company a sham?\n- Are directors personally liable?",
        principles="- Separate legal entity: Salomon principle\n- Piercing veil: Fraud, sham, evasion\n- Lifting veil exceptions",
        role_binding="COMPANY: Incorporated entity\nDIRECTOR: Individual\nCREDITORS: Claimants\nBENEFITED_PARTY: Director",
        doctrine_routing="PRIMARY_DOCTRINE: Piercing Corporate Veil\nBEST_FRAMEWORK: Piercing Veil\nREASON_FOR_SELECTION: Company used as sham to evade liability.\nREJECTED_DOCTRINE: Absolute Separate Entity\nREASON_REJECTED: Fraud and evasion justify piercing veil.",
        fact_findings="SEPARATE_ENTITY: Yes (incorporated)\nSHAM_PURPOSE: Yes (evade liability)\nFRAUD_OR_EVASION: Yes\nASSET_TRANSFER: Yes (personal to company)\nVEIL_PIERCING_JUSTIFIED: Yes\nDIRECTOR_PERSONALLY_LIABLE: Yes",
        legal_effect="Because SHAM_PURPOSE = Yes and FRAUD_OR_EVASION = Yes, veil piercing is justified.\nBecause VEIL_PIERCING_JUSTIFIED = Yes, separate entity doctrine does not protect.\nBecause DIRECTOR_PERSONALLY_LIABLE = Yes, creditors can reach company assets.",
        final_answer="Corporate veil pierced. Director personally liable.",
        category="piercing_veil",
        difficulty=2
    ))

print(f"  ✓ Corporate Law complete: {len([s for s in samples if 'corp' in s['metadata']['case_id'].lower()])} samples")

# EVIDENCE & PROCEDURE (20 samples)
print("\n[5/5] Evidence & Procedure (20 samples)")

# Burden of Proof (10 samples: 5 criminal, 5 civil)
print("  - Burden of Proof (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-EVID-BURDEN-CRIM-{22000+i}",
        facts=f"A charged with theft. Prosecution presents circumstantial evidence. Defense argues prosecution failed to prove guilt beyond reasonable doubt.",
        issues="- Who bears burden of proof?\n- What is the standard?\n- Has burden been discharged?",
        principles="- Criminal: Prosecution bears burden\n- Standard: Beyond reasonable doubt\n- Presumption of innocence",
        role_binding="PROSECUTION: State\nACCUSED: A\nBURDEN_HOLDER: Prosecution",
        doctrine_routing="PRIMARY_DOCTRINE: Burden of Proof (Criminal)\nBEST_FRAMEWORK: Prosecution burden\nREASON_FOR_SELECTION: Criminal case requires prosecution to prove guilt.",
        fact_findings="CRIMINAL_CASE: Yes\nBURDEN_ON_PROSECUTION: Yes\nSTANDARD: Beyond reasonable doubt\nCIRCUMSTANTIAL_EVIDENCE: Yes\nBURDEN_DISCHARGED: Fact-dependent\nPRESUMPTION_OF_INNOCENCE: Yes",
        legal_effect="Because CRIMINAL_CASE = Yes, burden is on prosecution.\nBecause STANDARD = Beyond reasonable doubt, high threshold applies.\nBecause PRESUMPTION_OF_INNOCENCE = Yes, accused need not prove innocence.",
        final_answer="Burden on prosecution. Standard: beyond reasonable doubt.",
        category="burden_criminal",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-EVID-BURDEN-CIVIL-{23000+i}",
        facts=f"Plaintiff sues for breach of contract. Defendant denies contract existence. Plaintiff presents written agreement. Defendant claims forgery.",
        issues="- Who bears burden of proof?\n- What is the standard?\n- Does burden shift?",
        principles="- Civil: Plaintiff bears initial burden\n- Standard: Balance of probabilities\n- Burden may shift on specific issues",
        role_binding="PLAINTIFF: Claimant\nDEFENDANT: Respondent\nINITIAL_BURDEN_HOLDER: Plaintiff",
        doctrine_routing="PRIMARY_DOCTRINE: Burden of Proof (Civil)\nBEST_FRAMEWORK: Plaintiff burden with shifting\nREASON_FOR_SELECTION: Civil case with affirmative defense.",
        fact_findings="CIVIL_CASE: Yes\nINITIAL_BURDEN_ON_PLAINTIFF: Yes\nSTANDARD: Balance of probabilities\nCONTRACT_PRESENTED: Yes\nFORGERY_CLAIMED: Yes\nBURDEN_SHIFTS_TO_DEFENDANT: Yes (on forgery)",
        legal_effect="Because CIVIL_CASE = Yes, initial burden is on plaintiff.\nBecause CONTRACT_PRESENTED = Yes, plaintiff discharges initial burden.\nBecause FORGERY_CLAIMED = Yes, burden shifts to defendant to prove forgery.",
        final_answer="Initial burden on plaintiff. Burden shifts to defendant on forgery claim.",
        category="burden_civil",
        difficulty=2
    ))

# Hearsay (10 samples: 5 inadmissible, 5 exception)
print("  - Hearsay Evidence (10 samples)")
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-EVID-HEARSAY-{24000+i}",
        facts=f"Witness testifies that friend told him accused confessed to crime. Friend not called as witness. Prosecution relies on this testimony.",
        issues="- Is hearsay evidence admissible?\n- Does exception apply?\n- Can testimony be relied upon?",
        principles="- Hearsay: Out-of-court statement offered for truth\n- General rule: Hearsay inadmissible\n- Exceptions: Dying declaration, res gestae, etc.",
        role_binding="WITNESS: Testifying person\nDECLARANT: Friend (not testifying)\nRELYING_PARTY: Prosecution",
        doctrine_routing="PRIMARY_DOCTRINE: Hearsay (Inadmissible)\nBEST_FRAMEWORK: Hearsay exclusion\nREASON_FOR_SELECTION: Out-of-court statement without declarant testimony.",
        fact_findings="OUT_OF_COURT_STATEMENT: Yes\nOFFERED_FOR_TRUTH: Yes\nDECLARANT_TESTIFYING: No\nHEARSAY: Yes\nEXCEPTION_APPLIES: No\nADMISSIBLE: No",
        legal_effect="Because OUT_OF_COURT_STATEMENT = Yes and OFFERED_FOR_TRUTH = Yes, hearsay rule applies.\nBecause DECLARANT_TESTIFYING = No and EXCEPTION_APPLIES = No, evidence is inadmissible.",
        final_answer="Hearsay evidence. Inadmissible.",
        category="hearsay_inadmissible",
        difficulty=2
    ))
    
    samples.append(make_sample(
        case_id=f"IND-EVID-DYING-DECL-{25000+i}",
        facts=f"Victim makes statement identifying attacker before death. Doctor records statement. Victim dies. Doctor testifies about victim's statement in trial.",
        issues="- Is dying declaration admissible?\n- Is this hearsay?\n- Does exception apply?",
        principles="- Dying Declaration: Statement by person expecting death\n- Exception to hearsay rule\n- Section 32 Evidence Act: Statements by deceased",
        role_binding="DECLARANT: Victim (deceased)\nWITNESS: Doctor\nRELYING_PARTY: Prosecution",
        doctrine_routing="PRIMARY_DOCTRINE: Dying Declaration (Hearsay Exception)\nBEST_FRAMEWORK: Dying Declaration\nREASON_FOR_SELECTION: Statement made in expectation of death.\nREJECTED_DOCTRINE: Hearsay Exclusion\nREASON_REJECTED: Dying declaration is recognized exception.",
        fact_findings="OUT_OF_COURT_STATEMENT: Yes\nDECLARANT_DECEASED: Yes\nEXPECTATION_OF_DEATH: Yes\nHEARSAY: Yes\nEXCEPTION_APPLIES: Yes (dying declaration)\nADMISSIBLE: Yes",
        legal_effect="Because EXPECTATION_OF_DEATH = Yes and DECLARANT_DECEASED = Yes, dying declaration exception applies.\nBecause EXCEPTION_APPLIES = Yes, hearsay rule does not exclude.\nBecause ADMISSIBLE = Yes, doctor's testimony can be relied upon.",
        final_answer="Dying declaration exception applies. Admissible.",
        category="dying_declaration",
        difficulty=2
    ))

print(f"  ✓ Evidence & Procedure complete: {len([s for s in samples if 'evid' in s['metadata']['case_id'].lower()])} samples")

# Save final dataset
with open('legal_reasoning_200_complete.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✓ DATASET COMPLETE: {len(samples)} samples")
print(f"✓ Saved to: legal_reasoning_200_complete.json")
print("\nDistribution by category:")
categories = {}
for s in samples:
    cat = s['metadata']['category']
    categories[cat] = categories.get(cat, 0) + 1
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
