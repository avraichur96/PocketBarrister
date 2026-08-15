"""
Complete 200-sample section-marked legal reasoning dataset generator
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

# Load existing 5 samples
with open('legal_reasoning_section_marked.json', 'r', encoding='utf-8') as f:
    samples = json.load(f)

print(f"Starting with {len(samples)} existing samples")
print("Building to 200 total samples...")
print("=" * 80)

# Import generator modules
import contract_samples
import tort_samples  
import criminal_samples
import corporate_samples
import evidence_samples

# Generate each category
print("\n[1/5] Generating Contract Law samples...")
samples.extend(contract_samples.generate(make_sample, start_idx=len(samples)))

print(f"\n[2/5] Generating Tort Law samples...")
samples.extend(tort_samples.generate(make_sample, start_idx=len(samples)))

print(f"\n[3/5] Generating Criminal Law samples...")
samples.extend(criminal_samples.generate(make_sample, start_idx=len(samples)))

print(f"\n[4/5] Generating Corporate Law samples...")
samples.extend(corporate_samples.generate(make_sample, start_idx=len(samples)))

print(f"\n[5/5] Generating Evidence & Procedure samples...")
samples.extend(evidence_samples.generate(make_sample, start_idx=len(samples)))

# Save final dataset
with open('legal_reasoning_200_complete.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✓ Dataset complete: {len(samples)} samples")
print(f"✓ Saved to: legal_reasoning_200_complete.json")
print("\nDistribution:")
categories = {}
for s in samples:
    cat = s['metadata']['category']
    categories[cat] = categories.get(cat, 0) + 1
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
