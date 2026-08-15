"""
Generate 200 section-marked legal reasoning samples
Distribution: Contract 80 | Tort 40 | Criminal 30 | Corporate 30 | Evidence 20
"""
import json
import sys

# Import the existing 5 samples
with open('legal_reasoning_section_marked.json', 'r', encoding='utf-8') as f:
    samples = json.load(f)

print(f"Loaded {len(samples)} existing samples")
print("Generating additional samples to reach 200 total...")
print("=" * 80)

# Helper function from existing script
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

# Track progress
target = 200
current = len(samples)

# CONTRACT LAW - Need 75 more (already have 5)
print(f"\n[1/5] Contract Law - generating {80-current} more samples...")

# Economic Duress - 15 more pairs (30 total)
prices = [100, 80, 120, 90, 110, 95, 105, 85, 115, 75, 125, 88, 92, 108, 78]
reductions = [40, 35, 45, 38, 42, 37, 43, 36, 44, 33, 46, 34, 39, 41, 32]
values = [50, 40, 60, 45, 55, 42, 58, 38, 62, 35, 65, 37, 43, 57, 33]
switching_costs = [8, 6, 10, 7, 9, 6.5, 9.5, 5.5, 10.5, 5, 11, 5.8, 7.2, 9.8, 4.5]
switching_months = [9, 8, 10, 7, 11, 6, 12, 5, 13, 4, 14, 5, 8, 11, 4]

for i in range(5, 20):
    idx = i % len(prices)
    
    samples.append(make_sample(
        case_id=f"IND-DURESS-EST-{1000+i}",
        facts=f"Company A and Company B have existing supply contract for specialized components at ₹{prices[idx]} per unit (total annual value ₹{values[idx]} crore). Mid-contract, Company A threatens to stop all deliveries unless Company B agrees to pay only ₹{prices[idx]-reductions[idx]} per unit ({reductions[idx]}% price reduction). Company B's entire manufacturing depends on these components with no alternative supplier available. Switching would require {switching_months[idx]} months retooling at ₹{switching_costs[idx]} crore cost, during which Company B would face production shutdown and bankruptcy. Company B signs modified contract under protest.",
        issues="- Is economic duress established?\n- Is undue influence the better framework?\n- Is the modification valid?",
        principles="- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent\n- Undue Influence: Dominant relationship + unfair advantage\n- Contract Modification: Requires free consent",
        role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nWHOSE_CONSENT_MATTERS: Company B",
        doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Economic Duress\nREASON_FOR_SELECTION: Immediate threat with no practical alternative.\nREJECTED_DOCTRINE: Undue Influence\nREASON_REJECTED: Supplier dependence is not relationship dominance.",
        fact_findings=f"IMMEDIATE_THREAT: Yes\nNO_PRACTICAL_ALTERNATIVE: Yes\nSWITCHING_COST: ₹{switching_costs[idx]} crore\nSWITCHING_TIME: {switching_months[idx]} months\nBANKRUPTCY_RISK: Yes\nFREE_CONSENT: No\nMODIFICATION_VALID: No",
        legal_effect="Because IMMEDIATE_THREAT = Yes and NO_PRACTICAL_ALTERNATIVE = Yes, economic duress is established.\nBecause FREE_CONSENT = No, modification is voidable.",
        final_answer="Economic duress established. Modification voidable.",
        category="economic_duress",
        difficulty=2
    ))

alt_prices = [50, 60, 55, 65, 52, 58, 62, 54, 56, 64, 51, 59, 53, 61, 57]
alt_reductions = [20, 18, 22, 19, 21, 17, 23, 16, 24, 15, 25, 14, 26, 13, 27]
alt_values = [10, 12, 11, 13, 9, 14, 8, 15, 7, 16, 6, 17, 5, 18, 4]
alt_suppliers = [3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2]
alt_weeks = [2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3]

for i in range(5, 20):
    idx = i % len(alt_prices)
    
    samples.append(make_sample(
        case_id=f"IND-DURESS-NEG-{2000+i}",
        facts=f"Company A and Company B have supply contract for standard components at ₹{alt_prices[idx]} per unit (annual value ₹{alt_values[idx]} crore). Company A threatens to stop deliveries unless Company B accepts reduced price of ₹{alt_prices[idx]-alt_reductions[idx]} per unit ({alt_reductions[idx]}% reduction). Company B has {alt_suppliers[idx]} other qualified suppliers who can provide identical components. Switching requires only updating purchase orders and can be completed within {alt_weeks[idx]} weeks with no retooling cost. Company B agrees to avoid hassle.",
        issues="- Is economic duress established?\n- Does availability of alternatives matter?\n- Is the modification valid?",
        principles="- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent\n- Practical alternative test\n- Convenience vs necessity",
        role_binding="PRESSURING_PARTY: Company A\nVICTIM_PARTY: Company B\nCHALLENGING_PARTY: Company B\nWHOSE_CONSENT_MATTERS: Company B",
        doctrine_routing="PRIMARY_DOCTRINE: Economic Duress\nBEST_FRAMEWORK: Economic Duress (not established)\nREASON_FOR_SELECTION: Threat scenario but elements not met.",
        fact_findings=f"IMMEDIATE_THREAT: Yes\nPRACTICAL_ALTERNATIVE_EXISTS: Yes ({alt_suppliers[idx]} suppliers, {alt_weeks[idx]} weeks)\nCONVENIENCE_NOT_NECESSITY: Yes\nFREE_CONSENT: Yes\nMODIFICATION_VALID: Yes",
        legal_effect="Because PRACTICAL_ALTERNATIVE_EXISTS = Yes, no-alternative element fails.\nBecause CONVENIENCE_NOT_NECESSITY = Yes, agreement was voluntary.\nBecause FREE_CONSENT = Yes, modification is enforceable.",
        final_answer="Economic duress not established. Modification valid.",
        category="economic_duress_negative",
        difficulty=2
    ))

print(f"  Generated economic duress samples. Total: {len(samples)}")

# Continue with script - save periodically
with open('legal_reasoning_200_partial.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)
print(f"  Saved checkpoint: {len(samples)} samples")
