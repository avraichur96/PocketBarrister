"""
Generate section-marked legal reasoning dataset
Format: ROLE_BINDING → DOCTRINE_ROUTING → FACT_FINDINGS → LEGAL_EFFECT → FINAL_ANSWER
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
        "metadata": {
            "case_id": case_id,
            "category": category,
            "difficulty": difficulty,
            "jurisdiction": "India",
            "token_count": len(output_text.split())
        }
    }

samples = []

# ============================================================================
# CONTRACT LAW - Economic Duress vs Undue Influence (40 samples)
# ============================================================================

# Example 1: Economic Duress - Established
samples.append(make_sample(
    case_id="IND-CONTRACT-DURESS-001",
    facts="Company A threatens to breach existing supply contract with Company B unless Company B agrees to reduce contract price by 40%. Company B depends entirely on Company A's supplies and would face bankruptcy if supply stops. Company B agrees under protest and later challenges the modification.",
    issues="- Is economic duress established?\n- Is undue influence the better framework?\n- Is the modification valid?",
    principles="- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent\n- Undue Influence: Dominant relationship + unfair advantage\n- Contract Modification: Requires free consent\n- Competing doctrines: Duress is threat-based; undue influence is relationship-based",
    role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nBENEFITED_PARTY: Company A\nWHOSE_CONSENT_MATTERS: Company B\nIRRELEVANT_CONSENT: Company A",
    doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nSECONDARY_DOCTRINE: Undue Influence\nBEST_FRAMEWORK: Economic Duress\nREASON_FOR_SELECTION: Immediate threat of breach with no practical alternative.\nREJECTED_DOCTRINE: Undue Influence\nREASON_REJECTED: Supplier dependence alone is not relationship-based dominance.",
    fact_findings="IMMEDIATE_THREAT: Yes\nNO_PRACTICAL_ALTERNATIVE: Yes\nBUSINESS_COLLAPSE_RISK: Yes\nRELATIONSHIP_DOMINANCE: No\nFREE_CONSENT: No\nMODIFICATION_VALID: No",
    legal_effect="Because IMMEDIATE_THREAT = Yes and NO_PRACTICAL_ALTERNATIVE = Yes, economic duress is established.\nBecause FREE_CONSENT = No, the modification is not validly enforceable against Company B.\nBecause RELATIONSHIP_DOMINANCE = No, undue influence is not the better framework.",
    final_answer="Company B can avoid the modified contract on economic duress. Undue influence is not the better framework.",
    category="economic_duress",
    difficulty=2
))

# Example 2: Economic Duress - NOT Established (Alternative Available)
samples.append(make_sample(
    case_id="IND-CONTRACT-DURESS-002",
    facts="Company A threatens to breach supply contract with Company B unless Company B accepts 20% price reduction. Company B has three other qualified suppliers available and can switch within 2 weeks. Company B agrees to avoid negotiation hassle. Later challenges modification.",
    issues="- Is economic duress established?\n- Does availability of alternatives matter?\n- Is the modification valid?",
    principles="- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent\n- Practical alternative test: Can victim reasonably avoid pressure?\n- Convenience vs necessity distinction",
    role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nBENEFITED_PARTY: Company A\nWHOSE_CONSENT_MATTERS: Company B\nIRRELEVANT_CONSENT: Company A",
    doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Economic Duress (but not established)\nREASON_FOR_SELECTION: Threat-based pressure scenario.\nREJECTED_DOCTRINE: None (correct framework, but elements not met)",
    fact_findings="IMMEDIATE_THREAT: Yes\nPRACTICAL_ALTERNATIVE_EXISTS: Yes (3 other suppliers, 2 weeks)\nBUSINESS_COLLAPSE_RISK: No\nCONVENIENCE_NOT_NECESSITY: Yes\nFREE_CONSENT: Yes\nMODIFICATION_VALID: Yes",
    legal_effect="Because PRACTICAL_ALTERNATIVE_EXISTS = Yes, the no-alternative element fails.\nBecause CONVENIENCE_NOT_NECESSITY = Yes, Company B's agreement was voluntary.\nBecause FREE_CONSENT = Yes, the modification is validly enforceable.",
    final_answer="Economic duress not established. Practical alternatives existed. Modification is valid.",
    category="economic_duress_negative",
    difficulty=2
))

# Example 3: Undue Influence - Established (Doctor-Patient)
samples.append(make_sample(
    case_id="IND-CONTRACT-INFLUENCE-001",
    facts="Dr. Sharma treats elderly patient Ramesh (78, illiterate) for terminal cancer. During treatment, Dr. Sharma persuades Ramesh to gift him property worth ₹2 crore. No independent advice. Ramesh's family challenges the gift after his death.",
    issues="- Is undue influence established?\n- Is economic duress the better framework?\n- Is the gift valid?",
    principles="- Undue Influence: Dominant position + unfair advantage + no independent advice\n- Fiduciary relationships: Doctor-patient creates presumption\n- Economic Duress: Threat-based, not relationship-based\n- Competing doctrines: Influence is relationship-based; duress is threat-based",
    role_binding="DOMINANT_PARTY: Dr. Sharma\nVULNERABLE_PARTY: Ramesh\nCHALLENGING_PARTY: Ramesh's family\nBENEFITED_PARTY: Dr. Sharma\nWHOSE_CONSENT_MATTERS: Ramesh\nIRRELEVANT_CONSENT: Dr. Sharma",
    doctrine_routing="PRIMARY_DOCTRINE: Undue Influence\nSECONDARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Undue Influence\nREASON_FOR_SELECTION: Doctor-patient fiduciary relationship creates dominance.\nREJECTED_DOCTRINE: Economic Duress\nREASON_REJECTED: No immediate threat. Case turns on relationship exploitation, not coercion.",
    fact_findings="FIDUCIARY_RELATIONSHIP: Yes (doctor-patient)\nDOMINANT_POSITION: Yes\nVULNERABLE_PARTY_STATUS: Yes (elderly, illiterate, terminal illness)\nUNFAIR_ADVANTAGE: Yes (₹2 crore gift)\nINDEPENDENT_ADVICE: No\nFREE_CONSENT: No\nGIFT_VALID: No",
    legal_effect="Because FIDUCIARY_RELATIONSHIP = Yes and DOMINANT_POSITION = Yes, presumption of undue influence arises.\nBecause INDEPENDENT_ADVICE = No and UNFAIR_ADVANTAGE = Yes, presumption is not rebutted.\nBecause FREE_CONSENT = No, the gift is voidable.",
    final_answer="Undue influence established. Economic duress not applicable. Gift is voidable.",
    category="undue_influence",
    difficulty=2
))

# Example 4: Void vs Voidable - Minor's Contract
samples.append(make_sample(
    case_id="IND-CONTRACT-VOID-001",
    facts="Amit (17) purchases goods worth ₹50 lakh using fake ID showing age 22. Seller unaware of minority. After delivery, Amit refuses payment claiming minority. Seller argues contract should be voidable (allowing restitution) not void (no remedy).",
    issues="- Is contract void ab initio or voidable?\n- Does seller's ignorance affect status?\n- Can seller claim restitution?",
    principles="- Section 11: Minor incompetent to contract\n- Mohori Bibee: Minor's contract void ab initio\n- Void vs Voidable: Void = no contract; Voidable = valid until avoided\n- Restitution: Limited equitable recovery may be considered",
    role_binding="INCOMPETENT_PARTY: Amit (minor)\nOTHER_PARTY: Seller\nCHALLENGING_PARTY: Amit\nBENEFITED_PARTY: Amit\nWHOSE_CAPACITY_MATTERS: Amit\nIRRELEVANT_CAPACITY: Seller",
    doctrine_routing="PRIMARY_DOCTRINE: Void ab initio (Section 11)\nSECONDARY_DOCTRINE: Voidable contract\nBEST_FRAMEWORK: Void ab initio\nREASON_FOR_SELECTION: No competent party = no valid contract formed.\nREJECTED_DOCTRINE: Voidable\nREASON_REJECTED: Voidable requires valid contract first. Here no valid contract due to incompetency.",
    fact_findings="MINORITY_ESTABLISHED: Yes (17 years)\nCONTRACTUAL_CAPACITY: No\nVALID_CONTRACT_FORMED: No\nVOIDABLE_FRAMEWORK_APPLIES: No\nVOID_AB_INITIO: Yes\nCONTRACTUAL_REMEDY_AVAILABLE: No\nRESTITUTION_AVAILABLE: Limited/fact-dependent",
    legal_effect="Because CONTRACTUAL_CAPACITY = No, no valid contract was formed.\nBecause VALID_CONTRACT_FORMED = No, voidable doctrine cannot apply.\nBecause VOID_AB_INITIO = Yes, seller cannot enforce payment.\nBecause CONTRACTUAL_REMEDY_AVAILABLE = No, only limited equitable restitution may be considered.",
    final_answer="Contract void ab initio. Voidable framework rejected. Seller cannot enforce payment. Limited equitable restitution may be available.",
    category="void_voidable",
    difficulty=2
))

# Example 5: Fraud vs Misrepresentation
samples.append(make_sample(
    case_id="IND-CONTRACT-FRAUD-001",
    facts="Seller knowingly sells defective machinery to Buyer, actively concealing cracks and providing false inspection reports. Buyer discovers defects after installation. Seller claims innocent misrepresentation, not fraud.",
    issues="- Is fraud established or only misrepresentation?\n- Does intent to deceive matter?\n- What remedies are available?",
    principles="- Fraud (Section 17): False representation + knowledge of falsity + intent to deceive\n- Misrepresentation (Section 18): False representation without intent\n- Remedies: Fraud allows rescission + damages; Misrepresentation allows rescission only\n- Intent distinguishes fraud from misrepresentation",
    role_binding="DECEIVING_PARTY: Seller\nDECEIVED_PARTY: Buyer\nCHALLENGING_PARTY: Buyer\nBENEFITED_PARTY: Seller\nWHOSE_CONSENT_MATTERS: Buyer\nIRRELEVANT_CONSENT: Seller",
    doctrine_routing="PRIMARY_DOCTRINE: Fraud (Section 17)\nSECONDARY_DOCTRINE: Misrepresentation (Section 18)\nBEST_FRAMEWORK: Fraud\nREASON_FOR_SELECTION: Active concealment + false reports = intent to deceive.\nREJECTED_DOCTRINE: Innocent Misrepresentation\nREASON_REJECTED: Knowingly providing false reports negates innocence.",
    fact_findings="FALSE_REPRESENTATION: Yes (false inspection reports)\nKNOWLEDGE_OF_FALSITY: Yes (knowingly concealed cracks)\nINTENT_TO_DECEIVE: Yes (active concealment)\nINNOCENT_MISREPRESENTATION: No\nFRAUD_ESTABLISHED: Yes\nFREE_CONSENT: No\nCONTRACT_VOIDABLE: Yes\nDAMAGES_AVAILABLE: Yes",
    legal_effect="Because KNOWLEDGE_OF_FALSITY = Yes and INTENT_TO_DECEIVE = Yes, fraud is established.\nBecause FRAUD_ESTABLISHED = Yes, innocent misrepresentation is rejected.\nBecause FREE_CONSENT = No, contract is voidable.\nBecause FRAUD_ESTABLISHED = Yes, Buyer can claim both rescission and damages.",
    final_answer="Fraud established. Misrepresentation rejected. Contract voidable. Buyer can claim rescission and damages.",
    category="fraud",
    difficulty=2
))

print("Generating section-marked legal reasoning dataset...")
print(f"Total samples generated: {len(samples)}")

# Save dataset
with open('legal_reasoning_section_marked.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print("✓ Dataset saved to legal_reasoning_section_marked.json")
print("\nSample breakdown:")
print(f"  Contract Law: {len([s for s in samples if 'contract' in s['metadata']['category'].lower()])} samples")
