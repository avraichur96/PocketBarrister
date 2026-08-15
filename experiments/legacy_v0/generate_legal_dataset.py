import json
import random

# Load existing 5 samples
with open('legal_training_1000.json', 'r', encoding='utf-8') as f:
    samples = json.load(f)

print(f"Starting with {len(samples)} existing samples")
print("Generating remaining 995 samples...")

# Distribution plan: 1000 total samples
# Formation & Validity: 150 (15%)
# Free Consent: 250 (25%)
# Void Agreements: 150 (15%)
# Performance & Breach: 200 (20%)
# Remedies & Damages: 150 (15%)
# Quasi-Contracts: 50 (5%)
# Contingent/Special: 50 (5%)

# Complexity: 30% straightforward, 50% moderate, 20% complex

def create_sample(section, statute_text, case_name, case_year, case_principle, scenario, question, analysis_steps, outcome, category, complexity):
    """Create a properly formatted training sample"""
    
    input_text = f"""[STATUTE]
{section}, Indian Contract Act, 1872: {statute_text}

[CASE LAW REFERENCE]
{case_name} ({case_year}): {case_principle}

[SCENARIO]
{scenario}

[QUESTION]
{question}"""
    
    output_text = f"""[ANALYSIS]
{analysis_steps}

[OUTCOME]
{outcome}"""
    
    token_estimate = len(input_text.split()) + len(output_text.split())
    
    return {
        "input": input_text,
        "output": output_text,
        "metadata": {
            "section": section,
            "category": category,
            "complexity": complexity,
            "case_law": [f"{case_name} ({case_year})"],
            "jurisdiction": "India",
            "token_count": token_estimate * 1.3  # Rough estimate
        }
    }

# Section 10 - Formation (45 more samples needed)
section_10_samples = [
    create_sample(
        "Section 10",
        "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void",
        "Mohori Bibee v. Dharmodas Ghose",
        "1903",
        "A minor's agreement is absolutely void. A minor cannot ratify the contract upon attaining majority. Estoppel does not apply against a minor",
        "Priya, aged 17, purchases a motorcycle worth ₹1.5 lakh by misrepresenting her age as 21. She provides a forged driving license. After 6 months, she turns 18 and refuses to pay the remaining ₹80,000. The seller sues for payment, arguing Priya should be estopped from denying her age misrepresentation",
        "Can the seller enforce the contract against Priya after she attains majority? Apply Mohori Bibee estoppel principle",
        """1. Applicable Law: Section 10 requires competent parties. Section 11 defines minor as incompetent. Mohori Bibee establishes minor's contract is void ab initio.

2. Case Law Application: Mohori Bibee (1903) held that estoppel cannot validate a void contract. Even fraudulent misrepresentation by minor does not create enforceable obligation. Attaining majority does not ratify void contract.

3. Fact Analysis:
   (a) Age at Contract: 17 years (minor under Section 11)
   (b) Fraudulent Misrepresentation: Forged license showing age 21
   (c) Current Status: Now 18 (attained majority)
   (d) Seller's Argument: Estoppel should prevent denial of age
   (e) Mohori Bibee Test: Can estoppel validate void contract?

4. Legal Reasoning:
   Step 1: Contract formed when Priya was 17 - void ab initio under Section 11
   Step 2: Mohori Bibee principle - void contract remains void despite fraud
   Step 3: Estoppel cannot be invoked to validate void agreement
   Step 4: Attaining majority does not convert void contract to valid contract
   Step 5: No ratification possible for void ab initio contracts
   Step 6: Seller has no contractual remedy despite Priya's fraud

5. Conclusion: Contract void under Section 10/11. Mohori Bibee bars estoppel defense. Attaining majority irrelevant for void ab initio contracts""",
        "NO - Contract cannot be enforced. Mohori Bibee principle: minor's contract is void ab initio and remains void even after attaining majority. Estoppel does not apply to validate void contracts. Seller may have tort remedy for fraud but no contractual remedy",
        "capacity",
        "moderate"
    ),
    
    create_sample(
        "Section 10",
        "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object",
        "Balfour v. Balfour",
        "1919",
        "Social and domestic agreements lack intention to create legal relations and are not enforceable contracts even if other elements of Section 10 are present",
        "Husband promises wife ₹50,000 monthly allowance while he works abroad. Wife agrees to manage household in India. After 2 years, husband stops payments. Wife sues for breach of contract under Section 10, arguing all elements (consent, consideration, lawful object) are present",
        "Is the domestic arrangement between husband and wife an enforceable contract under Section 10?",
        """1. Applicable Law: Section 10 requires free consent, competent parties, lawful consideration, and lawful object. Balfour v. Balfour adds requirement of intention to create legal relations.

2. Case Law Application: Balfour v. Balfour (1919) held that domestic arrangements between spouses lack intention to create legal relations. Such agreements are not contracts despite satisfying technical Section 10 elements.

3. Fact Analysis:
   (a) Parties: Husband and wife (competent under Section 11)
   (b) Consideration: Wife manages household, husband pays allowance (valid consideration)
   (c) Object: Lawful (family support)
   (d) Context: Domestic arrangement between spouses
   (e) Balfour Test: Was there intention to create legal relations?

4. Legal Reasoning:
   Step 1: Technical Section 10 elements satisfied (consent, capacity, consideration, lawful object)
   Step 2: Balfour principle - domestic agreements presumed to lack legal intent
   Step 3: Arrangement made in context of marital relationship
   Step 4: No evidence of intention to create binding legal obligation
   Step 5: Social/domestic agreements excluded from contract law
   Step 6: Section 10 requires not just technical elements but also legal intent

5. Conclusion: Despite satisfying formal Section 10 requirements, agreement lacks intention to create legal relations per Balfour principle. Not an enforceable contract""",
        "NO - Not an enforceable contract. Balfour v. Balfour principle: domestic arrangements between spouses lack intention to create legal relations. Technical compliance with Section 10 elements insufficient without legal intent. Wife cannot sue for breach of contract",
        "formation",
        "moderate"
    ),
]

samples.extend(section_10_samples)

# Section 15 - Coercion (75 more samples)
section_15_samples = [
    create_sample(
        "Section 15",
        "Coercion is the committing, or threatening to commit, any act forbidden by the Indian Penal Code, or the unlawful detaining, or threatening to detain, any property, to the prejudice of any person whatever, with the intention of causing any person to enter into an agreement",
        "Ammiraju v. Seshamma",
        "1918",
        "Threat to prosecute for criminal offense can constitute coercion if the threat is made to induce a contract and the prosecution threat is improper or malicious",
        "Shopkeeper threatens to file false theft complaint against employee unless employee signs promissory note for ₹5 lakh (allegedly stolen goods value). Employee, fearing arrest, signs the note. Later, employee proves no theft occurred and seeks to void the promissory note",
        "Does the threat to file false criminal complaint constitute coercion under Section 15?",
        """1. Applicable Law: Section 15 defines coercion as threat to commit act forbidden by IPC. Filing false complaint violates IPC Section 182 (false information to public servant).

2. Case Law Application: Ammiraju v. Seshamma (1918) held that threat of criminal prosecution can be coercion if threat is improper, malicious, or made to extract unfair advantage.

3. Fact Analysis:
   (a) Threat: File theft complaint (criminal prosecution)
   (b) Nature: False complaint (no actual theft)
   (c) Purpose: Induce signing of ₹5 lakh promissory note
   (d) IPC Violation: False complaint violates IPC Section 182
   (e) Ammiraju Test: Was prosecution threat improper/malicious?

4. Legal Reasoning:
   Step 1: Threat to file criminal complaint is act forbidden by IPC (Section 182 - false information)
   Step 2: Threat made with intention to induce contract (promissory note)
   Step 3: Ammiraju principle - improper prosecution threat constitutes coercion
   Step 4: False complaint threat is malicious and improper
   Step 5: Employee signed under fear of criminal prosecution
   Step 6: All Section 15 elements satisfied

5. Conclusion: Threat to file false criminal complaint constitutes coercion under Section 15. Ammiraju principle applies - improper prosecution threat voids consent""",
        "YES - Coercion under Section 15. Threat to file false criminal complaint is act forbidden by IPC Section 182. Per Ammiraju principle, improper prosecution threat to extract contract is coercion. Promissory note voidable under Section 19",
        "free_consent",
        "moderate"
    ),
    
    create_sample(
        "Section 15",
        "Coercion is the committing, or threatening to commit, any act forbidden by the Indian Penal Code",
        "Chikham Amiraju v. Chikham Seshamma",
        "1918",
        "Threat to take legal action for a legitimate claim does not constitute coercion, even if it induces a settlement agreement",
        "Creditor threatens to file civil suit for ₹10 lakh debt unless debtor agrees to pay ₹12 lakh (including interest). Debtor, wanting to avoid litigation costs, agrees and signs settlement. Later, debtor claims coercion, arguing threat of lawsuit forced the agreement",
        "Does threat of legitimate civil litigation constitute coercion under Section 15?",
        """1. Applicable Law: Section 15 requires threat of act forbidden by IPC. Civil litigation is lawful right, not IPC violation.

2. Case Law Application: Chikham Amiraju (1918) held that threat to exercise legal rights (including filing suit) is not coercion, even if it pressures other party into agreement.

3. Fact Analysis:
   (a) Threat: File civil suit for debt recovery
   (b) Underlying Claim: ₹10 lakh legitimate debt
   (c) Settlement Terms: ₹12 lakh (debt + interest)
   (d) Legal Right: Creditor has right to sue for debt
   (e) Chikham Test: Is exercising legal right coercion?

4. Legal Reasoning:
   Step 1: Section 15 requires threat of act forbidden by IPC
   Step 2: Filing civil suit is lawful right, not IPC offense
   Step 3: Chikham principle - threat to exercise legal rights not coercion
   Step 4: Creditor entitled to pursue legitimate debt claim
   Step 5: Settlement induced by lawful pressure, not unlawful coercion
   Step 6: No IPC violation, therefore no Section 15 coercion

5. Conclusion: Threat of legitimate litigation not coercion under Section 15. Chikham principle protects right to threaten lawful legal action. Settlement agreement valid""",
        "NO - Not coercion under Section 15. Per Chikham Amiraju, threat to exercise legitimate legal rights (filing suit for valid debt) is not coercion. Civil litigation is lawful, not act forbidden by IPC. Settlement agreement valid and enforceable",
        "free_consent",
        "straightforward"
    ),
]

samples.extend(section_15_samples)

print(f"Generated {len(samples)} samples so far...")

# Save progress
with open('legal_training_1000.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print(f"Saved {len(samples)} samples to legal_training_1000.json")
print("Continuing generation...")
