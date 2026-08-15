"""
Visualize Legal Reasoning Dataset
Generates comprehensive visualizations and statistics
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import re

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

def load_dataset(file_path):
    """Load JSON dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_metadata(samples):
    """Extract metadata from samples"""
    categories = []
    difficulties = []
    input_lengths = []
    output_lengths = []
    
    for sample in samples:
        # Extract category from case_id or analyze content
        input_text = sample['input']
        output_text = sample['output']
        
        # Determine category from case_id
        if 'DURESS' in input_text:
            if 'economic duress not established' in output_text.lower() or 'duress not established' in output_text.lower():
                categories.append('economic_duress_negative')
            elif 'boundary' in input_text.lower() or 'delayed' in input_text.lower():
                categories.append('economic_duress_boundary')
            else:
                categories.append('economic_duress')
        elif 'INFLUENCE' in input_text:
            categories.append('undue_influence')
        elif 'VOID' in input_text:
            categories.append('void_contract')
        elif 'VOIDABLE' in input_text:
            categories.append('voidable_contract')
        elif 'FRAUD' in input_text:
            categories.append('fraud')
        elif 'MISREPRESENTATION' in input_text:
            categories.append('misrepresentation')
        elif 'NEGLIGENCE' in input_text:
            if 'negligence not established' in output_text.lower():
                categories.append('negligence_negative')
            else:
                categories.append('negligence')
        elif 'STRICT' in input_text or 'LIABILITY' in input_text:
            categories.append('strict_liability')
        elif 'VICARIOUS' in input_text:
            categories.append('vicarious_liability')
        elif 'INTENTION' in input_text:
            categories.append('criminal_intention')
        elif 'KNOWLEDGE' in input_text:
            categories.append('criminal_knowledge')
        elif 'ATTEMPT' in input_text:
            categories.append('attempt')
        elif 'PREPARATION' in input_text:
            categories.append('preparation')
        elif 'COMMON INTENTION' in input_text:
            categories.append('common_intention')
        elif 'COMMON OBJECT' in input_text:
            categories.append('common_object')
        elif 'DIRECTOR' in input_text:
            categories.append('director_duty')
        elif 'PIERCING' in input_text or 'VEIL' in input_text:
            categories.append('piercing_veil')
        elif 'BURDEN' in input_text:
            if 'criminal' in input_text.lower():
                categories.append('burden_criminal')
            else:
                categories.append('burden_civil')
        elif 'HEARSAY' in input_text:
            categories.append('hearsay')
        elif 'DYING' in input_text:
            categories.append('dying_declaration')
        else:
            categories.append('other')
        
        # Estimate difficulty (simple heuristic)
        if 'boundary' in input_text.lower() or 'complex' in input_text.lower():
            difficulties.append(3)
        else:
            difficulties.append(2)
        
        # Calculate lengths
        input_lengths.append(len(input_text))
        output_lengths.append(len(output_text))
    
    return categories, difficulties, input_lengths, output_lengths

def count_sections(samples):
    """Count section markers in outputs"""
    section_counts = {
        'ROLE_BINDING': 0,
        'DOCTRINE_ROUTING': 0,
        'FACT_FINDINGS': 0,
        'LEGAL_EFFECT': 0,
        'FINAL_ANSWER': 0,
        'EOS_TOKEN': 0
    }
    
    for sample in samples:
        output = sample['output']
        if '<ROLE_BINDING>' in output:
            section_counts['ROLE_BINDING'] += 1
        if '<DOCTRINE_ROUTING>' in output:
            section_counts['DOCTRINE_ROUTING'] += 1
        if '<FACT_FINDINGS>' in output:
            section_counts['FACT_FINDINGS'] += 1
        if '<LEGAL_EFFECT>' in output:
            section_counts['LEGAL_EFFECT'] += 1
        if '<FINAL_ANSWER>' in output:
            section_counts['FINAL_ANSWER'] += 1
        if '<|end_of_text|>' in output:
            section_counts['EOS_TOKEN'] += 1
    
    return section_counts

def analyze_fact_variables(samples):
    """Analyze fact variables in FACT_FINDINGS sections"""
    all_variables = []
    
    for sample in samples:
        output = sample['output']
        # Extract FACT_FINDINGS section
        if '<FACT_FINDINGS>' in output and '</FACT_FINDINGS>' in output:
            start = output.index('<FACT_FINDINGS>') + len('<FACT_FINDINGS>')
            end = output.index('</FACT_FINDINGS>')
            fact_section = output[start:end]
            
            # Extract variables (format: VARIABLE_NAME: Yes/No)
            variables = re.findall(r'([A-Z_]+):\s*(Yes|No)', fact_section)
            all_variables.extend([v[0] for v in variables])
    
    return Counter(all_variables)

def create_visualizations(file_path):
    """Create all visualizations"""
    print("Loading dataset...")
    samples = load_dataset(file_path)
    print(f"Loaded {len(samples)} samples\n")
    
    # Extract metadata
    print("Extracting metadata...")
    categories, difficulties, input_lengths, output_lengths = extract_metadata(samples)
    
    # Count sections
    print("Counting sections...")
    section_counts = count_sections(samples)
    
    # Analyze fact variables
    print("Analyzing fact variables...")
    fact_variables = analyze_fact_variables(samples)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Category Distribution
    ax1 = plt.subplot(2, 3, 1)
    category_counts = Counter(categories)
    categories_sorted = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    cat_names = [c[0] for c in categories_sorted]
    cat_values = [c[1] for c in categories_sorted]
    
    colors = sns.color_palette("husl", len(cat_names))
    bars = ax1.barh(cat_names, cat_values, color=colors)
    ax1.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax1.set_title('Category Distribution', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, cat_values)):
        ax1.text(val + 0.5, i, str(val), va='center', fontsize=10)
    
    # 2. Difficulty Distribution
    ax2 = plt.subplot(2, 3, 2)
    difficulty_counts = Counter(difficulties)
    diff_labels = [f'Level {k}' for k in sorted(difficulty_counts.keys())]
    diff_values = [difficulty_counts[k] for k in sorted(difficulty_counts.keys())]
    
    colors_diff = ['#2ecc71', '#f39c12', '#e74c3c']
    ax2.pie(diff_values, labels=diff_labels, autopct='%1.1f%%', 
            colors=colors_diff[:len(diff_values)], startangle=90)
    ax2.set_title('Difficulty Distribution', fontsize=14, fontweight='bold')
    
    # 3. Input/Output Length Distribution
    ax3 = plt.subplot(2, 3, 3)
    ax3.hist(input_lengths, bins=30, alpha=0.6, label='Input Length', color='#3498db')
    ax3.hist(output_lengths, bins=30, alpha=0.6, label='Output Length', color='#e74c3c')
    ax3.set_xlabel('Character Count', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax3.set_title('Text Length Distribution', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # 4. Section Marker Coverage
    ax4 = plt.subplot(2, 3, 4)
    section_names = list(section_counts.keys())
    section_values = list(section_counts.values())
    section_percentages = [v/len(samples)*100 for v in section_values]
    
    colors_section = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c']
    bars = ax4.bar(section_names, section_percentages, color=colors_section)
    ax4.set_ylabel('Coverage (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Section Marker Coverage', fontsize=14, fontweight='bold')
    ax4.set_ylim(0, 110)
    ax4.grid(axis='y', alpha=0.3)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add percentage labels
    for bar, pct in zip(bars, section_percentages):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 5. Top Fact Variables
    ax5 = plt.subplot(2, 3, 5)
    top_variables = fact_variables.most_common(15)
    var_names = [v[0] for v in top_variables]
    var_counts = [v[1] for v in top_variables]
    
    colors_var = sns.color_palette("viridis", len(var_names))
    bars = ax5.barh(var_names, var_counts, color=colors_var)
    ax5.set_xlabel('Frequency', fontsize=12, fontweight='bold')
    ax5.set_title('Top 15 Fact Variables', fontsize=14, fontweight='bold')
    ax5.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, var_counts)):
        ax5.text(val + 0.5, i, str(val), va='center', fontsize=9)
    
    # 6. Domain Distribution (Contract, Tort, Criminal, etc.)
    ax6 = plt.subplot(2, 3, 6)
    domain_map = {
        'economic_duress': 'Contract Law',
        'economic_duress_negative': 'Contract Law',
        'economic_duress_boundary': 'Contract Law',
        'undue_influence': 'Contract Law',
        'void_contract': 'Contract Law',
        'voidable_contract': 'Contract Law',
        'fraud': 'Contract Law',
        'misrepresentation': 'Contract Law',
        'negligence': 'Tort Law',
        'negligence_negative': 'Tort Law',
        'strict_liability': 'Tort Law',
        'vicarious_liability': 'Tort Law',
        'criminal_intention': 'Criminal Law',
        'criminal_knowledge': 'Criminal Law',
        'attempt': 'Criminal Law',
        'preparation': 'Criminal Law',
        'common_intention': 'Criminal Law',
        'common_object': 'Criminal Law',
        'director_duty': 'Corporate Law',
        'piercing_veil': 'Corporate Law',
        'burden_criminal': 'Evidence Law',
        'burden_civil': 'Evidence Law',
        'hearsay': 'Evidence Law',
        'dying_declaration': 'Evidence Law',
        'other': 'Other'
    }
    
    domains = [domain_map.get(cat, 'Other') for cat in categories]
    domain_counts = Counter(domains)
    
    domain_labels = list(domain_counts.keys())
    domain_values = list(domain_counts.values())
    
    colors_domain = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6', '#95a5a6']
    explode = [0.05 if v == max(domain_values) else 0 for v in domain_values]
    
    ax6.pie(domain_values, labels=domain_labels, autopct='%1.1f%%',
            colors=colors_domain[:len(domain_values)], startangle=90, explode=explode)
    ax6.set_title('Legal Domain Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('dataset_visualization.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved visualization to: dataset_visualization.png")
    
    # Print statistics
    print("\n" + "="*80)
    print("DATASET STATISTICS")
    print("="*80)
    print(f"\nTotal Samples: {len(samples)}")
    print(f"\nCategories: {len(category_counts)}")
    for cat, count in categories_sorted[:10]:
        print(f"  {cat}: {count}")
    if len(categories_sorted) > 10:
        print(f"  ... and {len(categories_sorted) - 10} more")
    
    print(f"\nDifficulty Levels:")
    for level in sorted(difficulty_counts.keys()):
        print(f"  Level {level}: {difficulty_counts[level]} ({difficulty_counts[level]/len(samples)*100:.1f}%)")
    
    print(f"\nText Length Statistics:")
    print(f"  Input - Mean: {np.mean(input_lengths):.0f}, Median: {np.median(input_lengths):.0f}, Max: {max(input_lengths)}")
    print(f"  Output - Mean: {np.mean(output_lengths):.0f}, Median: {np.median(output_lengths):.0f}, Max: {max(output_lengths)}")
    
    print(f"\nSection Coverage:")
    for section, count in section_counts.items():
        print(f"  {section}: {count}/{len(samples)} ({count/len(samples)*100:.1f}%)")
    
    print(f"\nDomain Distribution:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {count} ({count/len(samples)*100:.1f}%)")
    
    print(f"\nTop 10 Fact Variables:")
    for var, count in fact_variables.most_common(10):
        print(f"  {var}: {count}")
    
    print("\n" + "="*80)
    
    plt.show()

if __name__ == "__main__":
    print("="*80)
    print("LEGAL REASONING DATASET VISUALIZATION")
    print("="*80)
    
    # Visualize both datasets
    print("\n[1] Analyzing legal_reasoning_200_alpaca.json...")
    create_visualizations('legal_reasoning_200_alpaca.json')
    
    print("\n" + "="*80)
    print("\n[2] Analyzing legal_reasoning_600_alpaca.json...")
    try:
        create_visualizations('legal_reasoning_600_alpaca.json')
    except FileNotFoundError:
        print("  File not found, skipping...")
    
    print("\n✓ Visualization complete!")
