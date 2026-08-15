# Final Legal Reasoning Dataset - 200 Samples

## ✅ **Production Ready: `legal_reasoning_final.json`**

**Total Samples:** 200  
**Format:** FINDINGS → LEGAL_EFFECT → CONCLUSION  
**Optimized for:** Gemma-2B LoRA fine-tuning  
**Purpose:** Teach legal consequence propagation and reasoning

---

## 📊 **Complete Distribution**

### **First 100 Samples (Foundation):**

| Category | Samples | % | Purpose |
|----------|---------|---|---------|
| Void vs Voidable | 20 | 20% | Doctrine competition |
| Coercion vs Undue Influence | 20 | 20% | Consent analysis |
| Economic Duress | 20 | 20% | Commercial pressure |
| Fraud vs Misrepresentation | 15 | 15% | Intent ambiguity |
| Clear Minor Cases | 10 | 10% | Format stabilization |
| Mutual Mistake (Edge) | 15 | 15% | Deep analysis |

### **Next 100 Samples (Extension):**

| Category | Samples | % | Purpose |
|----------|---------|---|---------|
| **Role-Binding Duress** | 30 | 30% | Context-specific pressure |
| **Role-Binding Undue Influence** | 25 | 25% | Fiduciary relationships |
| **Void/Voidable Consequences** | 20 | 20% | Consequence chains |
| **Hard Negatives** | 15 | 15% | Boundary learning |
| **Short Direct EOS** | 10 | 10% | Quick termination |

---

## 🎯 **New Categories Explained**

### **1. Role-Binding Duress (30 samples)**

**Purpose:** Teach context-specific economic duress

**Subcategories:**
- **Employment duress** (10 samples)
  - Termination threats for wage reduction
  - Specialized skills + no alternatives
  - Exploitative use of lawful threats

- **Supplier dependency duress** (10 samples)
  - Mid-contract price increases
  - Breach threats exploiting dependency
  - Retooling costs eliminate alternatives

- **Creditor duress** (10 samples)
  - Criminal complaint threats for civil debt
  - Improper use of legal process
  - Reputational harm pressure

**Key Teaching:**
```
FINDINGS:
- ECONOMIC_DURESS_ESTABLISHED: Yes
- ILLEGITIMATE_PRESSURE: Yes (exploitative)
- EMPLOYMENT_DEPENDENCY: Yes
- PRACTICAL_ALTERNATIVE_EXISTS: No
- FREE_CONSENT: No
- MODIFICATION_VALID: No  ← Consequence!
```

---

### **2. Role-Binding Undue Influence (25 samples)**

**Purpose:** Teach fiduciary relationship exploitation

**Subcategories:**
- **Doctor-patient** (8 samples)
  - Medical dependency creates dominance
  - Terminal illness vulnerability
  - Inche Noriah presumption

- **Lawyer-client** (8 samples)
  - Highest fiduciary duty
  - Elderly + illiterate clients
  - Gross undervaluation

- **Religious advisor-devotee** (9 samples)
  - Spiritual authority dominance
  - False promises exploitation
  - Psychological control

**Key Teaching:**
```
FINDINGS:
- FIDUCIARY_RELATIONSHIP: Yes
- DOMINANT_POSITION: Yes
- UNFAIR_ADVANTAGE: Yes
- INDEPENDENT_ADVICE: No
- FREE_CONSENT: No
- TRANSFER_VALID: No  ← Consequence!
```

---

### **3. Void/Voidable Consequences (20 samples)**

**Purpose:** Teach consequence propagation for void vs voidable

**Subcategories:**
- **Ratification attempts** (5 samples)
  - Void contracts cannot be ratified
  - Voidable contracts can be ratified
  - Effect on subsequent obligations

- **Voidable ratification** (5 samples)
  - Requirements: knowledge + consent + unequivocal act
  - Bars subsequent avoidance
  - Timing matters

- **Partial performance** (5 samples)
  - Doesn't validate void contract
  - Mutual restitution required
  - No estoppel against minor

- **Third party rights** (5 samples)
  - Nemo dat principle
  - Void contract passes no title
  - Bona fide purchaser defense fails

**Key Teaching:**
```
FINDINGS:
- ORIGINAL_CONTRACT_VOID: Yes
- RATIFICATION_POSSIBLE: No
- VALID_CONTRACT_TO_RATIFY: No
- ACKNOWLEDGMENT_CREATES_NEW_CONTRACT: No
- CONTRACTUAL_OBLIGATION: No  ← Consequence chain!
```

---

### **4. Hard Negatives (15 samples)**

**Purpose:** Teach boundary formation - what ISN'T duress/influence/void

**Subcategories:**
- **Looks like duress but isn't** (5 samples)
  - Threat of lawsuit for valid debt = legitimate
  - Financial difficulty ≠ no alternative
  - Valid obligation + legal threat = no duress

- **Looks like undue influence but isn't** (5 samples)
  - Employer-employee not automatic fiduciary
  - Independent advice rebuts presumption
  - Reasonable gift for long service = voluntary

- **Looks like void but is voidable** (5 samples)
  - Intoxication = temporary (voidable)
  - Not permanent like minority (void)
  - Can be ratified upon sobering

**Key Teaching:**
```
FINDINGS:
- ECONOMIC_DURESS_ESTABLISHED: No
- ILLEGITIMATE_PRESSURE: No (legitimate legal threat)
- VALID_UNDERLYING_OBLIGATION: Yes
- FREE_CONSENT: Yes
- PAYMENT_VALID: Yes  ← Opposite consequence!
```

---

### **5. Short Direct EOS (10 samples)**

**Purpose:** Teach quick termination at EOS token

**Format:**
- Ultra-short facts (1-2 sentences)
- Single issue
- Brief reasoning (3 steps)
- Direct conclusion
- Immediate `<|end_of_text|>`

**Example:**
```
FACTS: Raj, aged 15, buys goods worth ₹1 crore. Can seller enforce?

REASONING:
Step 1 — Raj is 15 → minor
Step 2 — Mohori Bibee: void ab initio
Step 3 — Void cannot be enforced

FINDINGS:
- MINORITY: Yes
- CONTRACT_VOID: Yes
- ENFORCEABLE: No

CONCLUSION: NO. Void ab initio.<|end_of_text|>
```

---

## 🔥 **Key Improvements in Extended Dataset**

### **1. Context-Specific Duress**
- Employment, supplier, creditor contexts
- Teaches: lawful threats can be illegitimate if exploitative
- Dependency relationships affect duress analysis

### **2. Fiduciary Relationships**
- Doctor-patient, lawyer-client, religious advisor
- Teaches: different fiduciary duties (medical, legal, spiritual)
- Inche Noriah presumption strength varies

### **3. Consequence Chains**
- Ratification, partial performance, third party rights
- Teaches: void vs voidable has different consequences
- Nemo dat, restitution, title transfer rules

### **4. Boundary Learning**
- Hard negatives teach what ISN'T duress/influence/void
- Prevents over-application of doctrines
- Legitimate vs illegitimate pressure distinction

### **5. Quick Termination**
- Short samples teach when to stop
- Reinforces EOS token behavior
- Prevents over-generation

---

## 📈 **Training Recommendations**

### **Parameters:**
```python
# LoRA Configuration
lora_rank = 64
lora_alpha = 128
lora_dropout = 0.05

# Training
num_epochs = 10-12  # More samples = more epochs
learning_rate = 5e-6
batch_size = 1
gradient_accumulation_steps = 4
warmup_steps = 100

# Memory
fp16 = True
gradient_checkpointing = True
max_grad_norm = 0.3
```

**Expected Time (A100):** 10-15 minutes

---

## 🧪 **Testing Strategy**

### **Test Cases:**

1. **Employment Duress** (covered in training)
   - Should correctly identify exploitative termination threats

2. **Medical Undue Influence** (covered in training)
   - Should apply Inche Noriah to doctor-patient relationships

3. **Ratification** (covered in training)
   - Should distinguish void (cannot ratify) vs voidable (can ratify)

4. **Hard Negative** (covered in training)
   - Should recognize legitimate legal threats ≠ duress

5. **New Context** (NOT in training)
   - Landlord-tenant duress
   - Tests reasoning transfer

---

## ✅ **Success Criteria**

The model should:

1. **State Variables:** Track FINDINGS correctly
2. **Consequence Chains:** Apply LEGAL_EFFECT logic
3. **Context Awareness:** Recognize role-specific rules
4. **Boundary Formation:** Know when doctrines DON'T apply
5. **Quick Termination:** Stop at `<|end_of_text|>` appropriately
6. **No Contradictions:** Maintain logical consistency

---

## 📁 **Files**

- **`legal_reasoning_final.json`** - Production dataset (200 samples)
- **`create_extended_dataset.py`** - Generator for additional 100 samples
- **`create_improved_dataset.py`** - Generator for first 100 samples
- **`FINAL_200_DATASET.md`** - This documentation

---

## 🎯 **What This Dataset Teaches**

### **Not Just Doctrine Explanation:**
```
Old: "Economic duress requires illegitimate pressure..."
```

### **But Consequence Propagation:**
```
FINDINGS:
- ECONOMIC_DURESS_ESTABLISHED: Yes
- FREE_CONSENT: No

LEGAL_EFFECT:
Because FREE_CONSENT = No
→ MODIFICATION_VALID = No

CONCLUSION:
Modification voidable
```

### **The Model Learns:**
- `if duress → no consent → invalid`
- `if fiduciary + unfair → undue influence → voidable`
- `if void → no title → third party cannot acquire`
- `if voidable + ratification → binding`
- `if legitimate threat + valid debt → no duress`

---

## 🚀 **Ready for Production**

This 200-sample dataset is production-ready and addresses:

✅ Logical contradiction problem (FINDINGS + LEGAL_EFFECT)  
✅ Economic duress understanding (30 role-binding samples)  
✅ Fiduciary relationships (25 role-binding samples)  
✅ Void/voidable consequences (20 samples)  
✅ Boundary formation (15 hard negatives)  
✅ Quick termination (10 short EOS samples)  
✅ Precise restitution language (fact-dependent)  
✅ Context-specific reasoning (employment, medical, legal, religious)  

**Upload to Colab and train!** 🎓
