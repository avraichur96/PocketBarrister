"""
Generate 600-sample diversified legal reasoning dataset
Step 1: Diversify existing 185 samples (names, amounts, industries)
Step 2: Generate 415 new samples across all domains
Total: 600 samples with maximum diversity
"""
import json
import random

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

# Name pools for diversification
company_names = ["TechCorp", "InnovateLabs", "GlobalTrade", "PrimeVentures", "ApexSolutions", 
                 "NexGen Industries", "Stellar Enterprises", "Quantum Systems", "Vertex Group",
                 "Horizon Technologies", "Pinnacle Manufacturing", "Zenith Logistics", "Omega Pharma",
                 "Delta Electronics", "Sigma Textiles", "Alpha Chemicals", "Beta Automobiles",
                 "Gamma Retail", "Epsilon Energy", "Zeta Agritech"]

person_names_male = ["Rajesh", "Amit", "Suresh", "Vikram", "Arun", "Karan", "Rohan", "Nikhil",
                     "Sanjay", "Deepak", "Rahul", "Varun", "Arjun", "Ankit", "Mohit", "Ravi"]

person_names_female = ["Priya", "Neha", "Sunita", "Kavita", "Divya", "Asha", "Meera", "Pooja",
                       "Anjali", "Sneha", "Ritu", "Swati", "Nisha", "Rekha", "Geeta", "Suman"]

professional_names = ["Dr. Sharma", "Dr. Patel", "Dr. Gupta", "Dr. Mehta", "Dr. Kumar",
                      "Advocate Singh", "Advocate Verma", "Advocate Desai", "Advocate Roy",
                      "CA Joshi", "CA Pandey", "CA Malhotra", "Guru Anand", "Swami Prakash"]

print("=" * 80)
print("GENERATING 600-SAMPLE DIVERSIFIED LEGAL REASONING DATASET")
print("=" * 80)

# Load existing diversified dataset
with open('legal_reasoning_200_diversified.json', 'r', encoding='utf-8') as f:
    base_samples = json.load(f)

print(f"\nLoaded {len(base_samples)} base samples")

samples = []

# STEP 1: Diversify existing samples with name/amount variations
print("\n[STEP 1] Creating variations of existing samples...")
print("  - Generating 3 variations per base sample (185 × 3 = 555 samples)")

for base_idx, base_sample in enumerate(base_samples):
    # Add original
    samples.append(base_sample)
    
    # Generate 2 variations
    for var_idx in range(2):
        varied = json.loads(json.dumps(base_sample))  # Deep copy
        
        # Vary case_id
        orig_case_id = varied['metadata']['case_id']
        varied['metadata']['case_id'] = f"{orig_case_id}-VAR{var_idx+1}"
        
        # Vary names and amounts in input/output
        input_text = varied['input']
        output_text = varied['output']
        
        # Replace company names
        if "Company A" in input_text:
            company_a = random.choice(company_names)
            company_b = random.choice([c for c in company_names if c != company_a])
            input_text = input_text.replace("Company A", company_a)
            input_text = input_text.replace("Company B", company_b)
            output_text = output_text.replace("Company A", company_a)
            output_text = output_text.replace("Company B", company_b)
        
        # Replace person names
        for old_name in person_names_male + person_names_female:
            if old_name in input_text:
                new_name = random.choice(person_names_male if old_name in person_names_male else person_names_female)
                input_text = input_text.replace(old_name, new_name)
                output_text = output_text.replace(old_name, new_name)
        
        # Vary monetary amounts (±20%)
        import re
        amounts = re.findall(r'₹(\d+(?:\.\d+)?)\s*(lakh|crore)', input_text)
        for amount, unit in amounts:
            old_str = f"₹{amount} {unit}"
            base_val = float(amount)
            new_val = base_val * random.uniform(0.8, 1.2)
            new_str = f"₹{new_val:.1f} {unit}"
            input_text = input_text.replace(old_str, new_str, 1)
        
        # Vary percentages (±5%)
        percentages = re.findall(r'(\d+)%', input_text)
        for pct in percentages:
            old_str = f"{pct}%"
            new_pct = int(pct) + random.randint(-5, 5)
            new_pct = max(10, min(200, new_pct))  # Keep reasonable bounds
            new_str = f"{new_pct}%"
            input_text = input_text.replace(old_str, new_str, 1)
        
        # Vary time periods
        months = re.findall(r'(\d+)\s+months?', input_text)
        for month in months:
            old_str = f"{month} month" if month == "1" else f"{month} months"
            new_month = int(month) + random.randint(-2, 2)
            new_month = max(1, min(24, new_month))
            new_str = f"{new_month} month" if new_month == 1 else f"{new_month} months"
            input_text = input_text.replace(old_str, new_str, 1)
        
        # Update case_id in input
        input_text = re.sub(r'CASE_ID: [^\n]+', f"CASE_ID: {varied['metadata']['case_id']}", input_text)
        
        varied['input'] = input_text
        varied['output'] = output_text
        
        samples.append(varied)
    
    if (base_idx + 1) % 50 == 0:
        print(f"    Processed {base_idx + 1}/{len(base_samples)} base samples...")

print(f"  ✓ Generated {len(samples)} samples from base dataset")

# STEP 2: Generate 45 additional NEW samples to reach 600
print("\n[STEP 2] Generating 45 new diverse samples...")

new_samples_needed = 600 - len(samples)
print(f"  Target: {new_samples_needed} new samples")

# NEW CONTRACT LAW SAMPLES (20 samples)
print("\n  - Contract Law (20 new samples)")

# Mistake (5 samples: unilateral vs mutual)
for i in range(5):
    if i < 3:
        # Unilateral mistake - generally not voidable
        samples.append(make_sample(
            case_id=f"IND-MISTAKE-UNI-{30000+i}",
            facts=f"{random.choice(person_names_male)} purchases antique believing it's worth ₹{random.randint(5,10)} lakh. Actually worth ₹{random.randint(50,100)} thousand. Seller unaware of buyer's mistaken belief. Buyer seeks to void sale claiming unilateral mistake.",
            issues="- Is unilateral mistake grounds for voidability?\n- Does seller's knowledge matter?\n- Is contract voidable?",
            principles="- Unilateral Mistake: Generally not voidable unless induced by other party\n- Mutual Mistake: Both parties mistaken about same fact\n- Mistake must be fundamental to contract",
            role_binding=f"MISTAKEN_PARTY: {random.choice(person_names_male)}\nOTHER_PARTY: Seller\nCHALLENGING_PARTY: {random.choice(person_names_male)}",
            doctrine_routing="PRIMARY_DOCTRINE: Unilateral Mistake\nBEST_FRAMEWORK: Unilateral Mistake (not voidable)\nREASON_FOR_SELECTION: Only buyer mistaken, seller unaware.\nREJECTED_DOCTRINE: Mutual Mistake\nREASON_REJECTED: Seller not mistaken about value.",
            fact_findings="UNILATERAL_MISTAKE: Yes\nSELLER_AWARE_OF_MISTAKE: No\nSELLER_INDUCED_MISTAKE: No\nMUTUAL_MISTAKE: No\nFUNDAMENTAL_TO_CONTRACT: Yes\nVOIDABLE: No",
            legal_effect="Because UNILATERAL_MISTAKE = Yes and SELLER_INDUCED_MISTAKE = No, mistake is not voidable.\nBecause SELLER_AWARE_OF_MISTAKE = No, no duty to correct.\nBecause VOIDABLE = No, contract stands.",
            final_answer="Unilateral mistake. Not voidable. Contract valid.",
            category="unilateral_mistake",
            difficulty=2
        ))
    else:
        # Mutual mistake - voidable
        samples.append(make_sample(
            case_id=f"IND-MISTAKE-MUTUAL-{31000+i}",
            facts=f"Both {random.choice(person_names_male)} and {random.choice(person_names_female)} believe painting is original worth ₹{random.randint(50,80)} lakh. Later discovered to be reproduction worth ₹{random.randint(5,10)} lakh. Both parties mistaken about authenticity.",
            issues="- Is mutual mistake established?\n- Is mistake fundamental?\n- Is contract voidable?",
            principles="- Mutual Mistake: Both parties mistaken about same fundamental fact\n- Mistake must go to root of contract\n- Voidable if fundamental",
            role_binding=f"PARTY_1: {random.choice(person_names_male)}\nPARTY_2: {random.choice(person_names_female)}\nMISTAKEN_PARTIES: Both",
            doctrine_routing="PRIMARY_DOCTRINE: Mutual Mistake\nBEST_FRAMEWORK: Mutual Mistake\nREASON_FOR_SELECTION: Both parties mistaken about fundamental fact.\nREJECTED_DOCTRINE: Unilateral Mistake\nREASON_REJECTED: Both parties shared same mistaken belief.",
            fact_findings="MUTUAL_MISTAKE: Yes\nBOTH_PARTIES_MISTAKEN: Yes\nSAME_FACT: Yes (authenticity)\nFUNDAMENTAL_TO_CONTRACT: Yes\nGOES_TO_ROOT: Yes\nVOIDABLE: Yes",
            legal_effect="Because MUTUAL_MISTAKE = Yes and BOTH_PARTIES_MISTAKEN = Yes, mutual mistake is established.\nBecause FUNDAMENTAL_TO_CONTRACT = Yes, mistake goes to root of contract.\nBecause VOIDABLE = Yes, contract is voidable.",
            final_answer="Mutual mistake established. Contract voidable.",
            category="mutual_mistake",
            difficulty=2
        ))

# Impossibility (5 samples: initial vs supervening)
for i in range(5):
    if i < 3:
        # Initial impossibility - void ab initio
        samples.append(make_sample(
            case_id=f"IND-IMPOSSIBILITY-INITIAL-{32000+i}",
            facts=f"{random.choice(company_names)} agrees to sell specific cargo ship to {random.choice(company_names)} for ₹{random.randint(50,100)} crore. Unknown to both parties, ship had sunk {random.randint(2,5)} days before contract. Contract performance impossible from inception.",
            issues="- Is contract void for initial impossibility?\n- Does knowledge matter?\n- What is contract status?",
            principles="- Initial Impossibility: Performance impossible at contract formation\n- Section 56: Agreement to do impossible act is void\n- Void ab initio if impossible from start",
            role_binding=f"SELLER: {random.choice(company_names)}\nBUYER: {random.choice(company_names)}\nBOTH_PARTIES: Unaware of impossibility",
            doctrine_routing="PRIMARY_DOCTRINE: Initial Impossibility\nBEST_FRAMEWORK: Void ab initio\nREASON_FOR_SELECTION: Performance impossible at contract formation.\nREJECTED_DOCTRINE: Supervening Impossibility\nREASON_REJECTED: Impossibility existed before contract.",
            fact_findings="PERFORMANCE_IMPOSSIBLE: Yes\nIMPOSSIBLE_AT_FORMATION: Yes\nBOTH_PARTIES_UNAWARE: Yes\nINITIAL_IMPOSSIBILITY: Yes\nSUPERVENING_IMPOSSIBILITY: No\nVOID_AB_INITIO: Yes",
            legal_effect="Because IMPOSSIBLE_AT_FORMATION = Yes, contract is void ab initio.\nBecause INITIAL_IMPOSSIBILITY = Yes, Section 56 applies.\nBecause VOID_AB_INITIO = Yes, no contractual obligations arise.",
            final_answer="Initial impossibility. Contract void ab initio.",
            category="initial_impossibility",
            difficulty=2
        ))
    else:
        # Supervening impossibility - contract discharged
        samples.append(make_sample(
            case_id=f"IND-IMPOSSIBILITY-SUPERVENING-{33000+i}",
            facts=f"{random.choice(company_names)} contracts to supply goods to {random.choice(company_names)}. After contract but before performance, government bans export of those goods. Performance becomes illegal and impossible.",
            issues="- Is contract discharged by supervening impossibility?\n- Does illegality matter?\n- What are parties' obligations?",
            principles="- Supervening Impossibility: Performance becomes impossible after contract\n- Section 56: Contract becomes void when performance impossible\n- Frustration of contract",
            role_binding=f"SUPPLIER: {random.choice(company_names)}\nBUYER: {random.choice(company_names)}\nAFFECTED_PARTIES: Both",
            doctrine_routing="PRIMARY_DOCTRINE: Supervening Impossibility\nBEST_FRAMEWORK: Frustration/Discharge\nREASON_FOR_SELECTION: Performance became impossible after contract.\nREJECTED_DOCTRINE: Initial Impossibility\nREASON_REJECTED: Contract was possible at formation.",
            fact_findings="PERFORMANCE_IMPOSSIBLE: Yes\nIMPOSSIBLE_AFTER_CONTRACT: Yes\nGOVERNMENT_INTERVENTION: Yes\nILLEGAL_TO_PERFORM: Yes\nSUPERVENING_IMPOSSIBILITY: Yes\nCONTRACT_DISCHARGED: Yes",
            legal_effect="Because IMPOSSIBLE_AFTER_CONTRACT = Yes, supervening impossibility applies.\nBecause ILLEGAL_TO_PERFORM = Yes, contract is frustrated.\nBecause CONTRACT_DISCHARGED = Yes, parties are released from obligations.",
            final_answer="Supervening impossibility. Contract discharged.",
            category="supervening_impossibility",
            difficulty=2
        ))

# Restraint of Trade (5 samples)
for i in range(5):
    years = random.randint(2, 5)
    radius = random.randint(10, 50)
    reasonable = years <= 3 and radius <= 25
    
    samples.append(make_sample(
        case_id=f"IND-RESTRAINT-{34000+i}",
        facts=f"{random.choice(person_names_male)} sells business to {random.choice(person_names_female)} for ₹{random.randint(2,8)} crore. Contract includes non-compete clause: seller cannot start competing business within {radius} km radius for {years} years. Seller challenges clause as restraint of trade.",
        issues="- Is restraint of trade reasonable?\n- Is clause enforceable?\n- What factors determine reasonableness?",
        principles="- Section 27: Restraint of trade generally void\n- Exception: Reasonable restraint ancillary to sale of goodwill\n- Reasonableness: Duration, geographical scope, legitimate interest",
        role_binding=f"SELLER: {random.choice(person_names_male)}\nBUYER: {random.choice(person_names_female)}\nRESTRAINED_PARTY: {random.choice(person_names_male)}",
        doctrine_routing="PRIMARY_DOCTRINE: Restraint of Trade\nBEST_FRAMEWORK: Reasonableness Test\nREASON_FOR_SELECTION: Non-compete clause ancillary to sale of goodwill.",
        fact_findings=f"RESTRAINT_OF_TRADE: Yes\nANCILLARY_TO_SALE: Yes\nDURATION: {years} years\nGEOGRAPHICAL_SCOPE: {radius} km\nLEGITIMATE_INTEREST: Yes (protect goodwill)\nREASONABLE_DURATION: {'Yes' if years <= 3 else 'No'}\nREASONABLE_SCOPE: {'Yes' if radius <= 25 else 'No'}\nREASONABLE_RESTRAINT: {'Yes' if reasonable else 'No'}\nENFORCEABLE: {'Yes' if reasonable else 'No'}",
        legal_effect=f"Because ANCILLARY_TO_SALE = Yes, exception to Section 27 may apply.\nBecause DURATION = {years} years and GEOGRAPHICAL_SCOPE = {radius} km, reasonableness is {'established' if reasonable else 'not established'}.\nBecause REASONABLE_RESTRAINT = {'Yes' if reasonable else 'No'}, clause is {'enforceable' if reasonable else 'void'}.",
        final_answer=f"{'Reasonable restraint. Enforceable.' if reasonable else 'Unreasonable restraint. Void under Section 27.'}",
        category="restraint_of_trade",
        difficulty=2
    ))

# Wagering Agreements (5 samples)
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-WAGER-{35000+i}",
        facts=f"{random.choice(person_names_male)} and {random.choice(person_names_female)} enter agreement: if stock price of {random.choice(company_names)} rises above ₹{random.randint(500,1000)}, A pays B ₹{random.randint(5,20)} lakh; if falls below, B pays A same amount. Neither party owns stock or has legitimate interest. Pure bet on price movement.",
        issues="- Is this a wagering agreement?\n- Is it enforceable?\n- What is legal status?",
        principles="- Section 30: Wagering agreements are void\n- Wagering: Mutual chance of gain/loss based on uncertain event\n- No legitimate interest in event outcome",
        role_binding=f"PARTY_A: {random.choice(person_names_male)}\nPARTY_B: {random.choice(person_names_female)}\nWAGERING_PARTIES: Both",
        doctrine_routing="PRIMARY_DOCTRINE: Wagering Agreement\nBEST_FRAMEWORK: Void under Section 30\nREASON_FOR_SELECTION: Pure bet with no legitimate interest.",
        fact_findings="MUTUAL_CHANCE_GAIN_LOSS: Yes\nUNCERTAIN_EVENT: Yes (stock price)\nNO_LEGITIMATE_INTEREST: Yes\nNEITHER_OWNS_STOCK: Yes\nWAGERING_AGREEMENT: Yes\nVOID: Yes\nENFORCEABLE: No",
        legal_effect="Because MUTUAL_CHANCE_GAIN_LOSS = Yes and UNCERTAIN_EVENT = Yes, wagering elements present.\nBecause NO_LEGITIMATE_INTEREST = Yes, agreement is pure wager.\nBecause WAGERING_AGREEMENT = Yes, void under Section 30.",
        final_answer="Wagering agreement. Void under Section 30. Not enforceable.",
        category="wagering_agreement",
        difficulty=2
    ))

print(f"  ✓ Contract Law: {len([s for s in samples if s['metadata']['category'] in ['unilateral_mistake', 'mutual_mistake', 'initial_impossibility', 'supervening_impossibility', 'restraint_of_trade', 'wagering_agreement']])} new samples")

# NEW TORT LAW SAMPLES (10 samples)
print("\n  - Tort Law (10 new samples)")

# Defamation (5 samples)
for i in range(5):
    if i < 3:
        # Defamation established
        samples.append(make_sample(
            case_id=f"IND-TORT-DEFAMATION-{40000+i}",
            facts=f"{random.choice(person_names_male)} publishes article in newspaper stating {random.choice(person_names_female)} embezzled ₹{random.randint(10,50)} lakh from company. Statement is false. {random.choice(person_names_female)}'s reputation damaged, loses job and business opportunities.",
            issues="- Is defamation established?\n- Are elements of defamation met?\n- What defenses available?",
            principles="- Defamation: False statement + publication + damage to reputation\n- Libel: Written defamation\n- Defenses: Truth, privilege, fair comment",
            role_binding=f"DEFAMER: {random.choice(person_names_male)}\nDEFAMED: {random.choice(person_names_female)}\nINJURED_PARTY: {random.choice(person_names_female)}",
            doctrine_routing="PRIMARY_DOCTRINE: Defamation (Libel)\nBEST_FRAMEWORK: Defamation\nREASON_FOR_SELECTION: False written statement damaging reputation.",
            fact_findings="FALSE_STATEMENT: Yes\nPUBLICATION: Yes (newspaper)\nDAMAGE_TO_REPUTATION: Yes\nLOSS_OF_JOB: Yes\nBUSINESS_OPPORTUNITIES_LOST: Yes\nTRUTH_DEFENSE: No (statement false)\nDEFAMATION_ESTABLISHED: Yes",
            legal_effect="Because FALSE_STATEMENT = Yes and PUBLICATION = Yes, defamation elements present.\nBecause DAMAGE_TO_REPUTATION = Yes, harm is established.\nBecause TRUTH_DEFENSE = No, no defense available.\nBecause DEFAMATION_ESTABLISHED = Yes, liable for damages.",
            final_answer="Defamation established. Liable for damages.",
            category="defamation",
            difficulty=2
        ))
    else:
        # Defamation not established - truth defense
        samples.append(make_sample(
            case_id=f"IND-TORT-DEFAMATION-NEG-{41000+i}",
            facts=f"{random.choice(person_names_male)} publishes article stating {random.choice(person_names_female)} was convicted of fraud. Statement is true and based on public court records. {random.choice(person_names_female)} sues for defamation.",
            issues="- Is defamation established?\n- Does truth defense apply?\n- Is statement actionable?",
            principles="- Truth is absolute defense to defamation\n- Public interest in truthful reporting\n- No liability for true statements",
            role_binding=f"PUBLISHER: {random.choice(person_names_male)}\nCLAIMANT: {random.choice(person_names_female)}\nALLEGED_DEFAMER: {random.choice(person_names_male)}",
            doctrine_routing="PRIMARY_DOCTRINE: Defamation (Truth Defense)\nBEST_FRAMEWORK: Truth Defense\nREASON_FOR_SELECTION: Statement is true.\nREJECTED_DOCTRINE: Defamation Liability\nREASON_REJECTED: Truth is absolute defense.",
            fact_findings="STATEMENT_MADE: Yes\nPUBLICATION: Yes\nDAMAGE_TO_REPUTATION: Yes\nSTATEMENT_TRUE: Yes\nBASED_ON_PUBLIC_RECORDS: Yes\nTRUTH_DEFENSE: Yes\nDEFAMATION_ESTABLISHED: No",
            legal_effect="Because STATEMENT_TRUE = Yes, truth defense applies.\nBecause TRUTH_DEFENSE = Yes, no liability for defamation.\nBecause DEFAMATION_ESTABLISHED = No, claim fails.",
            final_answer="Truth defense established. No defamation liability.",
            category="defamation_negative",
            difficulty=2
        ))

# Nuisance (5 samples)
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-TORT-NUISANCE-{42000+i}",
        facts=f"Factory operated by {random.choice(company_names)} emits loud noise {random.randint(80,100)} decibels and toxic fumes 24/7. Residential area nearby. {random.choice(person_names_female)} living {random.randint(100,500)} meters away suffers health issues and sleep deprivation. Sues for nuisance.",
        issues="- Is private nuisance established?\n- Is interference unreasonable?\n- What remedies available?",
        principles="- Private Nuisance: Unreasonable interference with use and enjoyment of land\n- Reasonableness: Locality, duration, severity\n- Remedies: Injunction, damages",
        role_binding=f"DEFENDANT: {random.choice(company_names)}\nPLAINTIFF: {random.choice(person_names_female)}\nINJURED_PARTY: {random.choice(person_names_female)}",
        doctrine_routing="PRIMARY_DOCTRINE: Private Nuisance\nBEST_FRAMEWORK: Unreasonable Interference\nREASON_FOR_SELECTION: Interference with use and enjoyment of land.",
        fact_findings=f"INTERFERENCE: Yes (noise and fumes)\nUSE_AND_ENJOYMENT_AFFECTED: Yes\nRESIDENTIAL_LOCALITY: Yes\nDURATION: Continuous (24/7)\nSEVERITY: High (health issues)\nUNREASONABLE_INTERFERENCE: Yes\nNUISANCE_ESTABLISHED: Yes",
        legal_effect="Because INTERFERENCE = Yes and USE_AND_ENJOYMENT_AFFECTED = Yes, interference is established.\nBecause RESIDENTIAL_LOCALITY = Yes and SEVERITY = High, interference is unreasonable.\nBecause NUISANCE_ESTABLISHED = Yes, remedies available.",
        final_answer="Private nuisance established. Injunction and damages available.",
        category="nuisance",
        difficulty=2
    ))

print(f"  ✓ Tort Law: {len([s for s in samples if s['metadata']['category'] in ['defamation', 'defamation_negative', 'nuisance']])} new samples")

# NEW CRIMINAL LAW SAMPLES (10 samples)
print("\n  - Criminal Law (10 new samples)")

# Abetment (5 samples)
for i in range(5):
    samples.append(make_sample(
        case_id=f"IND-CRIM-ABETMENT-{50000+i}",
        facts=f"{random.choice(person_names_male)} instigates {random.choice(person_names_female)} to commit theft of ₹{random.randint(5,20)} lakh from company. Provides inside information, plan, and encouragement. {random.choice(person_names_female)} commits theft. Both arrested.",
        issues="- Is abetment established?\n- What is A's liability?\n- Are both equally liable?",
        principles="- Abetment: Instigation, conspiracy, or intentional aid\n- Section 107-109 IPC: Abetment of offense\n- Abettor liable as if principal offender",
        role_binding=f"ABETTOR: {random.choice(person_names_male)}\nPRINCIPAL_OFFENDER: {random.choice(person_names_female)}\nBOTH_ACCUSED: Both liable",
        doctrine_routing="PRIMARY_DOCTRINE: Abetment\nBEST_FRAMEWORK: Instigation and Aid\nREASON_FOR_SELECTION: Instigated and aided commission of offense.",
        fact_findings="INSTIGATION: Yes\nINFORMATION_PROVIDED: Yes\nENCOURAGEMENT: Yes\nINTENTIONAL_AID: Yes\nOFFENSE_COMMITTED: Yes (theft)\nABETMENT_ESTABLISHED: Yes\nABETTOR_LIABLE: Yes",
        legal_effect="Because INSTIGATION = Yes and INTENTIONAL_AID = Yes, abetment is established.\nBecause OFFENSE_COMMITTED = Yes, abettor liable under Section 109.\nBecause ABETTOR_LIABLE = Yes, both equally liable for theft.",
        final_answer="Abetment established. Both equally liable for theft.",
        category="abetment",
        difficulty=2
    ))

# Self-Defense (5 samples)
for i in range(5):
    if i < 3:
        # Self-defense established
        samples.append(make_sample(
            case_id=f"IND-CRIM-SELF-DEFENSE-{51000+i}",
            facts=f"{random.choice(person_names_male)} attacks {random.choice(person_names_female)} with knife intending to kill. {random.choice(person_names_female)} has no escape route. In self-defense, {random.choice(person_names_female)} strikes attacker with stick causing injury. Charged with assault.",
            issues="- Is self-defense established?\n- Was force reasonable?\n- Is accused liable?",
            principles="- Right of Private Defense: Sections 96-106 IPC\n- Reasonable force to repel attack\n- No liability if within limits",
            role_binding=f"ATTACKER: {random.choice(person_names_male)}\nDEFENDER: {random.choice(person_names_female)}\nACCUSED: {random.choice(person_names_female)}",
            doctrine_routing="PRIMARY_DOCTRINE: Right of Private Defense\nBEST_FRAMEWORK: Self-Defense\nREASON_FOR_SELECTION: Reasonable force to repel imminent attack.",
            fact_findings="IMMINENT_THREAT: Yes (knife attack)\nNO_ESCAPE_ROUTE: Yes\nFORCE_USED: Yes (stick)\nFORCE_REASONABLE: Yes\nEXCESSIVE_FORCE: No\nSELF_DEFENSE_ESTABLISHED: Yes\nLIABLE: No",
            legal_effect="Because IMMINENT_THREAT = Yes and NO_ESCAPE_ROUTE = Yes, right of defense arises.\nBecause FORCE_REASONABLE = Yes and EXCESSIVE_FORCE = No, within limits.\nBecause SELF_DEFENSE_ESTABLISHED = Yes, no liability.",
            final_answer="Self-defense established. Not liable.",
            category="self_defense",
            difficulty=2
        ))
    else:
        # Excessive force - self-defense fails
        samples.append(make_sample(
            case_id=f"IND-CRIM-SELF-DEFENSE-NEG-{52000+i}",
            facts=f"{random.choice(person_names_male)} slaps {random.choice(person_names_female)}. {random.choice(person_names_female)} responds by shooting attacker with gun causing death. Charged with murder. Claims self-defense.",
            issues="- Is self-defense established?\n- Was force excessive?\n- What is liability?",
            principles="- Right of Private Defense: Force must be proportionate\n- Excessive force negates defense\n- Disproportionate response = liability",
            role_binding=f"ATTACKER: {random.choice(person_names_male)}\nDEFENDER: {random.choice(person_names_female)}\nACCUSED: {random.choice(person_names_female)}",
            doctrine_routing="PRIMARY_DOCTRINE: Excessive Force\nBEST_FRAMEWORK: Self-Defense Limits Exceeded\nREASON_FOR_SELECTION: Force disproportionate to threat.\nREJECTED_DOCTRINE: Valid Self-Defense\nREASON_REJECTED: Shooting in response to slap is excessive.",
            fact_findings="THREAT: Yes (slap)\nFORCE_USED: Yes (gunshot)\nFORCE_PROPORTIONATE: No\nEXCESSIVE_FORCE: Yes\nSELF_DEFENSE_ESTABLISHED: No\nLIABLE: Yes (culpable homicide/murder)",
            legal_effect="Because THREAT = Yes but FORCE_PROPORTIONATE = No, defense limits exceeded.\nBecause EXCESSIVE_FORCE = Yes, right of defense does not apply.\nBecause LIABLE = Yes, culpable homicide or murder charge stands.",
            final_answer="Excessive force. Self-defense not established. Liable for culpable homicide.",
            category="self_defense_negative",
            difficulty=2
        ))

print(f"  ✓ Criminal Law: {len([s for s in samples if s['metadata']['category'] in ['abetment', 'self_defense', 'self_defense_negative']])} new samples")

# NEW CORPORATE LAW SAMPLES (3 samples)
print("\n  - Corporate Law (3 new samples)")

# Oppression and Mismanagement (3 samples)
for i in range(3):
    samples.append(make_sample(
        case_id=f"IND-CORP-OPPRESSION-{60000+i}",
        facts=f"Majority shareholders ({random.randint(70,85)}%) of {random.choice(company_names)} consistently exclude minority shareholders from board meetings, deny dividend distribution despite profits of ₹{random.randint(10,50)} crore, and divert company assets to related parties. Minority shareholders file oppression petition.",
        issues="- Is oppression and mismanagement established?\n- Are minority rights violated?\n- What remedies available?",
        principles="- Sections 241-246 Companies Act: Oppression and Mismanagement\n- Oppression: Burdensome, harsh, wrongful conduct\n- Remedies: Buyout, winding up, directions",
        role_binding=f"MAJORITY_SHAREHOLDERS: Controlling group\nMINORITY_SHAREHOLDERS: Petitioners\nCOMPANY: {random.choice(company_names)}",
        doctrine_routing="PRIMARY_DOCTRINE: Oppression and Mismanagement\nBEST_FRAMEWORK: Sections 241-246\nREASON_FOR_SELECTION: Systematic exclusion and asset diversion.",
        fact_findings="EXCLUSION_FROM_MEETINGS: Yes\nDIVIDEND_DENIAL: Yes (despite profits)\nASSET_DIVERSION: Yes\nOPPRESSIVE_CONDUCT: Yes\nMISMANAGEMENT: Yes\nMINORITY_RIGHTS_VIOLATED: Yes\nREMEDIES_AVAILABLE: Yes",
        legal_effect="Because EXCLUSION_FROM_MEETINGS = Yes and DIVIDEND_DENIAL = Yes, oppressive conduct established.\nBecause ASSET_DIVERSION = Yes, mismanagement is proven.\nBecause MINORITY_RIGHTS_VIOLATED = Yes, remedies under Sections 241-246 available.",
        final_answer="Oppression and mismanagement established. Remedies available under Sections 241-246.",
        category="oppression_mismanagement",
        difficulty=2
    ))

print(f"  ✓ Corporate Law: {len([s for s in samples if s['metadata']['category'] == 'oppression_mismanagement'])} new samples")

# NEW EVIDENCE LAW SAMPLES (2 samples)
print("\n  - Evidence Law (2 new samples)")

# Res Gestae (2 samples)
for i in range(2):
    samples.append(make_sample(
        case_id=f"IND-EVID-RES-GESTAE-{70000+i}",
        facts=f"Immediately after being shot, victim shouts '{random.choice(person_names_male)} shot me!' Witness hears statement. Victim dies before trial. Prosecution offers witness testimony of victim's statement. Defense objects as hearsay.",
        issues="- Is res gestae exception applicable?\n- Is statement admissible?\n- Does hearsay rule apply?",
        principles="- Res Gestae: Spontaneous statement contemporaneous with event\n- Exception to hearsay rule\n- Section 6 Evidence Act: Statements forming part of transaction",
        role_binding="DECLARANT: Victim (deceased)\nWITNESS: Person who heard statement\nRELYING_PARTY: Prosecution",
        doctrine_routing="PRIMARY_DOCTRINE: Res Gestae Exception\nBEST_FRAMEWORK: Res Gestae\nREASON_FOR_SELECTION: Spontaneous statement contemporaneous with shooting.\nREJECTED_DOCTRINE: Hearsay Exclusion\nREASON_REJECTED: Res gestae is recognized exception.",
        fact_findings="SPONTANEOUS_STATEMENT: Yes\nCONTEMPORANEOUS_WITH_EVENT: Yes (immediately after)\nNO_TIME_FOR_FABRICATION: Yes\nPART_OF_TRANSACTION: Yes\nHEARSAY: Yes\nRES_GESTAE_EXCEPTION: Yes\nADMISSIBLE: Yes",
        legal_effect="Because SPONTANEOUS_STATEMENT = Yes and CONTEMPORANEOUS_WITH_EVENT = Yes, res gestae applies.\nBecause NO_TIME_FOR_FABRICATION = Yes, reliability is high.\nBecause RES_GESTAE_EXCEPTION = Yes, hearsay rule does not exclude.",
        final_answer="Res gestae exception applies. Statement admissible.",
        category="res_gestae",
        difficulty=2
    ))

print(f"  ✓ Evidence Law: {len([s for s in samples if s['metadata']['category'] == 'res_gestae'])} new samples")

# Save final 600-sample dataset
output_file = 'legal_reasoning_600_final.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✓ FINAL DATASET COMPLETE: {len(samples)} samples")
print(f"✓ Saved to: {output_file}")
print("\n" + "=" * 80)
print("DATASET BREAKDOWN:")
print("=" * 80)

categories = {}
for s in samples:
    cat = s['metadata']['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\nBy Category:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

print(f"\nTotal Categories: {len(categories)}")
print(f"Average samples per category: {len(samples) / len(categories):.1f}")

# Difficulty distribution
difficulties = {}
for s in samples:
    diff = s['metadata']['difficulty']
    difficulties[diff] = difficulties.get(diff, 0) + 1

print("\nBy Difficulty:")
for diff, count in sorted(difficulties.items()):
    print(f"  Level {diff}: {count}")

print("\n" + "=" * 80)
print("KEY FEATURES:")
print("  ✓ Diversified names (20+ company names, 30+ person names)")
print("  ✓ Varied amounts (±20% variation)")
print("  ✓ Varied percentages and time periods")
print("  ✓ 3 variations per base sample")
print("  ✓ 45 new diverse samples across all domains")
print("  ✓ Fixed price direction (suppliers demand MORE)")
print("  ✓ Multiple threat types and factual surfaces")
print("  ✓ Boundary cases and hard negatives")
print("=" * 80)
