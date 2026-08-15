"""
Add reasoning tags to legal_training_1000.json
Transforms: <REASONING>...[ANALYSIS]...</REASONING>\n\n<CONCLUSION>...[OUTCOME]...</CONCLUSION><|end_of_text|>
"""

import json

print("Loading legal_training_1000.json...")
with open('legal_training_1000.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total samples: {len(data)}")
print("Adding reasoning tags...")

transformed = []
for i, sample in enumerate(data):
    output = sample['output']
    
    # Find [ANALYSIS] and [OUTCOME] positions
    analysis_start = output.find('[ANALYSIS]')
    outcome_start = output.find('[OUTCOME]')
    eos_start = output.find('<|end_of_text|>')
    
    if analysis_start == -1 or outcome_start == -1:
        print(f"Warning: Sample {i} missing ANALYSIS or OUTCOME, skipping transformation")
        transformed.append(sample)
        continue
    
    # Build new output with tags
    # Everything before [ANALYSIS] stays as is
    before_analysis = output[:analysis_start]
    
    # [ANALYSIS] section up to [OUTCOME]
    analysis_section = output[analysis_start:outcome_start]
    
    # [OUTCOME] section up to EOS
    outcome_section = output[outcome_start:eos_start]
    
    # EOS token
    eos_token = output[eos_start:]
    
    # Reconstruct with tags
    new_output = f"""<REASONING>
{analysis_section.strip()}
</REASONING>

<CONCLUSION>
{outcome_section.strip()}
</CONCLUSION>{eos_token}"""
    
    # Create new sample
    new_sample = {
        "input": sample['input'],
        "output": new_output,
        "metadata": sample.get('metadata', {})
    }
    transformed.append(new_sample)
    
    if (i + 1) % 100 == 0:
        print(f"  Processed {i + 1}/{len(data)} samples...")

print(f"\nSaving transformed dataset...")
with open('legal_training_1000_tagged.json', 'w', encoding='utf-8') as f:
    json.dump(transformed, f, indent=2, ensure_ascii=False)

print("✓ Complete! Saved to legal_training_1000_tagged.json")
print(f"\nVerifying first sample...")
print("=" * 80)
print(transformed[0]['output'][:500])
print("...")
print(transformed[0]['output'][-200:])
print("=" * 80)
