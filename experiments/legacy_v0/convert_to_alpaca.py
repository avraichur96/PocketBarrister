"""
Convert legal reasoning dataset to Alpaca format
Alpaca format: {"instruction": "", "input": "", "output": ""}
"""
import json

def convert_to_alpaca(input_file, output_file):
    """
    Convert legal reasoning dataset to Alpaca format
    
    Original format:
    {
        "input": "CASE_ID: ...\n\nFACTS:\n...\n\nISSUES:\n...\n\nAPPLICABLE PRINCIPLES:\n...",
        "output": "<ROLE_BINDING>...",
        "metadata": {...}
    }
    
    Alpaca format:
    {
        "instruction": "Analyze the following legal case and provide structured reasoning...",
        "input": "CASE_ID: ...\n\nFACTS:\n...",
        "output": "<ROLE_BINDING>..."
    }
    """
    
    # Load original dataset
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    print(f"Loaded {len(original_data)} samples from {input_file}")
    
    # Convert to Alpaca format
    alpaca_data = []
    
    instruction_template = """Analyze the following legal case and provide structured legal reasoning using the specified format.

Your response must follow this exact structure:
1. <ROLE_BINDING>: Identify all parties and whose consent/capacity matters
2. <DOCTRINE_ROUTING>: Select the primary legal doctrine, explain why it's the best framework, and reject alternative doctrines with reasoning
3. <FACT_FINDINGS>: Extract relevant facts as state variables (Yes/No format)
4. <LEGAL_EFFECT>: Apply causal reasoning showing how facts lead to legal consequences (use "Because X = Yes/No, Y follows" format)
5. <FINAL_ANSWER>: Provide a concise conclusion

End your response with <|end_of_text|> token."""
    
    for idx, sample in enumerate(original_data):
        alpaca_sample = {
            "instruction": instruction_template,
            "input": sample["input"],
            "output": sample["output"]
        }
        alpaca_data.append(alpaca_sample)
        
        if (idx + 1) % 50 == 0:
            print(f"  Converted {idx + 1}/{len(original_data)} samples...")
    
    # Save Alpaca format
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(alpaca_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Converted {len(alpaca_data)} samples to Alpaca format")
    print(f"✓ Saved to: {output_file}")
    
    # Print sample
    print("\n" + "=" * 80)
    print("SAMPLE ALPACA FORMAT:")
    print("=" * 80)
    print(json.dumps(alpaca_data[0], indent=2, ensure_ascii=False)[:1000] + "...")
    
    return alpaca_data

if __name__ == "__main__":
    # Convert 200 diversified dataset
    print("Converting legal_reasoning_200_diversified.json to Alpaca format...")
    print("=" * 80)
    
    alpaca_200 = convert_to_alpaca(
        'legal_reasoning_200_diversified.json',
        'legal_reasoning_200_alpaca.json'
    )
    
    print("\n" + "=" * 80)
    print("Converting legal_reasoning_600_final.json to Alpaca format...")
    print("=" * 80)
    
    alpaca_600 = convert_to_alpaca(
        'legal_reasoning_600_final.json',
        'legal_reasoning_600_alpaca.json'
    )
    
    print("\n" + "=" * 80)
    print("CONVERSION COMPLETE")
    print("=" * 80)
    print(f"✓ legal_reasoning_200_alpaca.json: {len(alpaca_200)} samples")
    print(f"✓ legal_reasoning_600_alpaca.json: {len(alpaca_600)} samples")
