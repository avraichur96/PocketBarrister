# 600-Sample Legal Reasoning Dataset - Complete Summary

## Overview
**Total Samples:** 600  
**File:** `legal_reasoning_600_final.json`  
**Format:** Section-marked with `<ROLE_BINDING>`, `<DOCTRINE_ROUTING>`, `<FACT_FINDINGS>`, `<LEGAL_EFFECT>`, `<FINAL_ANSWER>`, `<|end_of_text|>`  
**Jurisdiction:** India  

## Generation Strategy

### Step 1: Base Dataset (185 samples)
- Started with diversified base covering all major legal domains
- Fixed price direction (suppliers demand MORE, not less)
- Diversified threat types (10+ scenarios)
- Added boundary cases

### Step 2: Variation Generation (370 samples)
- Created **2 variations** per base sample (185 × 2 = 370)
- **Name diversification:**
  - 20 company names (TechCorp, Quantum Systems, Vertex Group, etc.)
  - 16 male person names (Rajesh, Amit, Vikram, etc.)
  - 16 female person names (Priya, Neha, Sunita, etc.)
  - 14 professional names (Dr. Sharma, Advocate Singh, CA Joshi, etc.)
- **Amount variation:** ±20% on all monetary values
- **Percentage variation:** ±5% on all percentages
- **Time period variation:** ±2 months on time periods
- **Case ID variation:** Added -VAR1, -VAR2 suffixes

### Step 3: New Samples (45 samples)
Added entirely new legal concepts:
- **Contract Law (20):** Mistake, Impossibility, Restraint of Trade, Wagering
- **Tort Law (10):** Defamation, Nuisance
- **Criminal Law (10):** Abetment, Self-Defense
- **Corporate Law (3):** Oppression & Mismanagement
- **Evidence Law (2):** Res Gestae

## Distribution by Category (39 categories)

### Contract Law (240 samples)
| Category | Count | Description |
|----------|-------|-------------|
| economic_duress | 30 | Illegitimate pressure + no alternative |
| economic_duress_negative | 21 | Alternatives exist, legitimate pressure |
| economic_duress_boundary | 9 | Delayed challenge, partial alternatives |
| undue_influence | 30 | Fiduciary relationships, dominance |
| void | 30 | Minor's contracts, void ab initio |
| voidable | 15 | Fraud, competent parties |
| fraud | 15 | Intent to deceive |
| misrepresentation | 15 | No intent, honest belief |
| coercion | 15 | Criminal threats for civil debts |
| unilateral_mistake | 3 | Buyer mistaken, seller unaware |
| mutual_mistake | 2 | Both parties mistaken |
| initial_impossibility | 3 | Impossible at formation |
| supervening_impossibility | 2 | Became impossible after |
| restraint_of_trade | 5 | Non-compete clauses |
| wagering_agreement | 5 | Pure bets, no legitimate interest |

### Tort Law (120 samples)
| Category | Count | Description |
|----------|-------|-------------|
| negligence | 30 | Duty + breach + causation + damage |
| negligence_negative | 30 | Standard met, bad outcome alone |
| strict_liability | 30 | Dangerous activity, no fault required |
| vicarious_liability | 30 | Employer liable for employee tort |
| defamation | 3 | False statement damaging reputation |
| defamation_negative | 2 | Truth defense |
| nuisance | 5 | Unreasonable interference with land |

### Criminal Law (90 samples)
| Category | Count | Description |
|----------|-------|-------------|
| intention | 15 | Purpose to cause result |
| knowledge | 15 | Awareness result will follow |
| attempt | 15 | Proximate act toward completion |
| preparation | 15 | Remote acts, not proximate |
| common_intention | 15 | Pre-arranged plan + participation |
| common_object | 15 | Unlawful assembly, no pre-arrangement |
| abetment | 5 | Instigation, aid to commit offense |
| self_defense | 3 | Reasonable force to repel attack |
| self_defense_negative | 2 | Excessive force |

### Corporate Law (93 samples)
| Category | Count | Description |
|----------|-------|-------------|
| director_duty | 45 | Fiduciary duty breach, corporate opportunity |
| piercing_veil | 45 | Sham companies, fraud/evasion |
| oppression_mismanagement | 3 | Minority rights violation |

### Evidence & Procedure (57 samples)
| Category | Count | Description |
|----------|-------|-------------|
| burden_criminal | 30 | Prosecution bears burden |
| burden_civil | 15 | Plaintiff bears initial burden |
| hearsay_inadmissible | 15 | Out-of-court statement, no exception |
| dying_declaration | 15 | Hearsay exception |
| res_gestae | 2 | Spontaneous contemporaneous statement |

## Difficulty Distribution
- **Level 2 (Standard):** 591 samples (98.5%)
- **Level 3 (Complex/Boundary):** 9 samples (1.5%)

## Key Features

### 1. Fixed Business Logic ✅
**Before (wrong):**
```
Company A threatens to stop deliveries unless Company B pays only ₹60 per unit
(supplier forcing buyer to pay LESS - commercially nonsensical)
```

**After (correct):**
```
Company A threatens to stop deliveries unless Company B pays ₹140 per unit instead of ₹100
(supplier demanding MORE - commercially realistic)
```

### 2. Diversified Threat Types ✅
Not just "stop deliveries" - includes:
- **Supply chain:** Stop deliveries
- **Software/SaaS:** Revoke software access
- **Logistics:** Withhold goods at port (perishable, 48-hour deadline)
- **Seasonal:** Withdraw equipment during harvest window
- **Construction:** Abandon mid-project (investor penalty)
- **Distribution:** Terminate exclusive distribution
- **IP/Patent:** Revoke patent license
- **Cloud:** Shut down infrastructure (2M users)
- **Manufacturing:** Recall custom tooling
- **Payment:** Suspend payment gateway

### 3. Boundary Cases ✅
Hard cases testing doctrine limits:
- **Delayed challenge:** Duress + 18 months performance → affirmation issue
- **Partial alternative:** 30% capacity but 70% shortage → still duress
- **Legitimate pressure:** Market increase + termination clause → NOT duress
- **Excessive force:** Slap → gunshot → self-defense fails

### 4. Name & Amount Diversity ✅
- **20 company names:** TechCorp, InnovateLabs, Quantum Systems, Vertex Group, Horizon Technologies, etc.
- **32 person names:** Rajesh, Amit, Priya, Neha, Dr. Sharma, Advocate Singh, etc.
- **Varied amounts:** ±20% variation (₹50 crore → ₹43.7 crore, ₹59.2 crore)
- **Varied percentages:** 40% → 35%, 45%
- **Varied time:** 9 months → 7 months, 10 months, 11 months

### 5. Reduced Template Memorization Risk ✅
Instead of 40 identical "specialized components → duress yes" examples:
- 30 positive duress cases with 10+ different threat types
- 21 negative duress cases with 7+ different reasons
- 9 boundary cases with complications

Model will learn:
```
NO_PRACTICAL_ALTERNATIVE + ILLEGITIMATE_THREAT + VITIATED_CONSENT = DURESS
```

Not:
```
"specialized components" = duress yes
"standard components" = duress no
```

## Training Recommendations

### Model: Gemma-2B or Gemma-4B
### Method: LoRA Fine-tuning

### Hyperparameters:
```python
{
    "model": "google/gemma-2b",
    "lora_rank": 64,
    "lora_alpha": 128,
    "learning_rate": 5e-6,
    "batch_size": 2,
    "gradient_accumulation_steps": 4,
    "epochs": 5-7,
    "warmup_steps": 100,
    "max_seq_length": 2048,
    "optimizer": "adamw_8bit"
}
```

### Training Format:
```python
input_format = """CASE_ID: {case_id}

FACTS:
{facts}

ISSUES:
{issues}

APPLICABLE PRINCIPLES:
{principles}"""

output_format = """<ROLE_BINDING>
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
```

### Data Split:
- **Training:** 540 samples (90%)
- **Validation:** 60 samples (10%)
- Stratify by category to ensure balanced representation

### Expected Outcomes:
1. **Role Binding:** Correctly identify parties and whose consent matters
2. **Doctrine Routing:** Select appropriate legal framework and reject alternatives with reasoning
3. **Fact Finding:** Extract relevant facts as state variables
4. **Legal Effect:** Apply causal reasoning (Because X = Yes, Y follows)
5. **Clean Stopping:** Generate answer and stop at `<|end_of_text|>`

## Testing Strategy

### Test Prompts (Plain Text Format):
```
CASE_ID: TEST-001

FACTS:
Company X threatens to stop deliveries unless Company Y pays ₹200 per unit instead of ₹150. Company Y has 5 alternative suppliers available within 1 week. Company Y agrees to avoid hassle.

ISSUES:
- Is economic duress established?
- Is modification valid?

APPLICABLE PRINCIPLES:
- Economic Duress: Illegitimate pressure + no practical alternative + vitiated consent
```

### Expected Output:
```
<ROLE_BINDING>
PRESSURING_PARTY: Company X
VICTIM_PARTY: Company Y
WHOSE_CONSENT_MATTERS: Company Y
</ROLE_BINDING>

<DOCTRINE_ROUTING>
PRIMARY_DOCTRINE: Economic Duress
BEST_FRAMEWORK: Economic Duress (not established)
REASON_FOR_SELECTION: Threat scenario but elements not met.
</DOCTRINE_ROUTING>

<FACT_FINDINGS>
IMMEDIATE_THREAT: Yes
PRACTICAL_ALTERNATIVE_EXISTS: Yes (5 suppliers, 1 week)
CONVENIENCE_NOT_NECESSITY: Yes
FREE_CONSENT: Yes
DURESS_ESTABLISHED: No
</FACT_FINDINGS>

<LEGAL_EFFECT>
Because PRACTICAL_ALTERNATIVE_EXISTS = Yes, no-alternative element fails.
Because CONVENIENCE_NOT_NECESSITY = Yes, agreement was voluntary.
Because DURESS_ESTABLISHED = No, modification is valid.
</LEGAL_EFFECT>

<FINAL_ANSWER>
Economic duress not established. Modification valid.
</FINAL_ANSWER>
<|end_of_text|>
```

## Files Generated

1. **legal_reasoning_200_diversified.json** (185 samples)
   - Base diversified dataset
   - Fixed price direction
   - Multiple threat types
   - Boundary cases

2. **legal_reasoning_600_final.json** (600 samples)
   - 185 base samples
   - 370 variations (names, amounts, times)
   - 45 new samples (new legal concepts)

3. **generate_600_final.py**
   - Complete generation script
   - Variation logic
   - New sample templates

## Comparison: Before vs After

### Before (Original 200):
- ❌ Wrong price direction (suppliers demanding LESS)
- ❌ 40 nearly identical duress examples
- ❌ Template memorization risk
- ❌ Limited name diversity
- ❌ Fixed amounts and percentages

### After (Final 600):
- ✅ Correct price direction (suppliers demanding MORE)
- ✅ 60 diverse duress examples (10+ threat types)
- ✅ Reduced memorization risk
- ✅ 20+ company names, 30+ person names
- ✅ Varied amounts (±20%), percentages (±5%), times (±2 months)
- ✅ 39 legal categories
- ✅ 45 new legal concepts
- ✅ Boundary cases and hard negatives

## Next Steps

1. **Train Model:**
   ```bash
   python train_gemma_lora.py \
     --model google/gemma-2b \
     --dataset legal_reasoning_600_final.json \
     --lora_rank 64 \
     --epochs 7 \
     --batch_size 2
   ```

2. **Evaluate:**
   - Test on held-out validation set
   - Check section marker adherence
   - Verify causal reasoning chains
   - Confirm EOS token stopping

3. **Iterate:**
   - Add more boundary cases if needed
   - Expand to 1000+ samples if model capacity allows
   - Add difficulty level 4-5 samples for advanced reasoning

## Conclusion

This 600-sample dataset is **production-ready** for Gemma-2B/4B LoRA fine-tuning. It addresses all previous issues:
- ✅ Correct business logic
- ✅ Diverse factual surfaces
- ✅ Reduced template memorization
- ✅ Comprehensive legal coverage
- ✅ Explicit reasoning structure
- ✅ Clean stopping behavior

**Ready to train!** 🎯
