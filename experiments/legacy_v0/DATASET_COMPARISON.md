# Legal Reasoning Dataset - Comparison & Improvements

## 📊 **Old Dataset vs New Dataset**

### **Old Dataset (`legal_training_1000.json`)**
- **Samples:** 491
- **Format:** `[STATUTE] → [CASE LAW] → [SCENARIO] → [QUESTION] → [ANALYSIS] → [OUTCOME]`
- **Approach:** Template-based legal information

**Problems:**
❌ Formulaic structure (every sample identical)  
❌ No doctrine competition (single clear answer)  
❌ Missing "WHY ALTERNATIVES FAIL" section  
❌ Too easy (mostly Level 1 - clear application)  
❌ Shallow reasoning (doesn't show thought process)  
❌ No ambiguity (facts always point to one answer)  
❌ Teaches WHAT law exists, not HOW to reason

**Result:** Model learned format but hallucinated new scenarios

---

### **New Dataset (`legal_reasoning_dataset.json`)**
- **Samples:** 120 (quality over quantity)
- **Format:** `CASE_ID → FACTS → ISSUES → PRINCIPLES → REASONING → CONCLUSION → WHY ALTERNATIVES FAIL`
- **Approach:** Reasoning-focused legal analysis

**Improvements:**
✅ **Doctrine Competition** - Forces choice between competing legal frameworks  
✅ **Explicit Reasoning Steps** - Shows lawyer's thought process  
✅ **WHY ALTERNATIVES FAIL** - Teaches boundary formation  
✅ **Difficulty Distribution:**
   - Level 1 (Clear): 20 samples (16.7%)
   - Level 2 (Competing): 60 samples (50.0%)
   - Level 3 (Ambiguous): 30 samples (25.0%)
   - Level 4 (Edge Cases): 10 samples (8.3%)

✅ **Teaches HOW lawyers think**, not WHAT law exists

---

## 🎯 **Key Improvements Based on Master Prompt**

### **1. Doctrine Competition (CRITICAL)**

**Old Approach:**
```
Section 10 applies → Minor's contract void → Done
```

**New Approach:**
```
Two competing frameworks:
(a) Void ab initio (Mohori Bibee) → no contract
(b) Voidable contract (Section 19) → contract exists until avoided

Must analyze which applies and WHY the other fails
```

---

### **2. WHY ALTERNATIVES FAIL Section**

**Old:** Missing entirely

**New:** Every sample includes:
```
WHY ALTERNATIVES FAIL:
- Voidable contract doctrine → REJECTED: Reason X
- Estoppel against minor → REJECTED: Reason Y
- Seller's ignorance defense → REJECTED: Reason Z
```

This teaches **boundary formation** between doctrines.

---

### **3. Reasoning Geometry**

**Old:** Linear explanation
```
1. Law says X
2. Facts show Y
3. Therefore Z
```

**New:** Multi-step analysis
```
Step 1 — Doctrine Selection: Identify competing frameworks
Step 2 — Fact-to-Rule Mapping: Map facts to elements
Step 3 — Applying Test: Apply legal test
Step 4 — Rejecting Alternatives: Eliminate wrong doctrines
Step 5 — Resolution: Justify final application
```

---

### **4. Ambiguity & Edge Cases**

**Old:** Every case has clear answer

**New:** 
- **Level 3 (30%):** Ambiguous cases with incomplete/conflicting facts
- **Level 4 (10%):** Edge cases requiring deep analysis
- Forces conditional reasoning: "If X, then Y; but if Z, then W"

---

## 📈 **Expected Training Improvements**

### **Old Dataset Results:**
- ❌ Learned format, lost reasoning
- ❌ Hallucinated new scenarios
- ❌ Weaker than baseline model
- ❌ No clear conclusion

### **New Dataset Expected Results:**
- ✅ Learn legal reasoning process
- ✅ Distinguish competing doctrines
- ✅ Stop at EOS token (no hallucination)
- ✅ Provide justified conclusions
- ✅ Explain why alternatives fail

---

## 🔧 **Sample Comparison**

### **Old Format:**
```
[STATUTE]
Section 10: Minor incompetent to contract

[CASE LAW]
Mohori Bibee: Minor's contract void

[SCENARIO]
Raj, 16, borrows money...

[ANALYSIS]
1. Raj is minor
2. Contract void
3. Cannot enforce

[OUTCOME]
NO - Cannot enforce
```

**Problem:** Memorization, not reasoning

---

### **New Format:**
```
CASE_ID: IND-CONTRACT-1000

FACTS:
Rahul, 16, enters contract. Seller unaware of age.
Seller argues voidable (restitution) vs void (no remedy).

ISSUES:
- Void ab initio or voidable?
- Does ignorance affect status?
- Can seller claim restitution?

APPLICABLE PRINCIPLES:
- Mohori Bibee: Void ab initio
- Section 19: Voidable contracts
- Section 65: Restitution

REASONING:
Step 1 — Doctrine Selection:
Two competing frameworks:
(a) Void ab initio → no contract
(b) Voidable → contract exists until avoided

Step 2 — Fact-to-Rule Mapping:
- Rahul is 16 → minor
- No fraud
- Seller ignorant
- Goods delivered

Step 3 — Applying Mohori Bibee:
Void ab initio regardless of:
- Minor's fraud
- Seller's knowledge
- Benefit to minor

Step 4 — Rejecting Voidable Framework:
Voidable applies when:
- Valid contract formed BUT
- Consent vitiated
Here: No valid contract (incompetent party)

Step 5 — Restitution Analysis:
Section 65 allows restitution BUT:
- Limited to benefits
- Doesn't validate contract

CONCLUSION:
Void ab initio. Seller cannot enforce.
Restitution under Section 65 only.

WHY ALTERNATIVES FAIL:
- Voidable doctrine → No valid contract formed
- Estoppel → Mohori Bibee bars it
- Ignorance defense → Competency objective
- Quantum meruit → Unavailable for incompetency
```

**Benefit:** Teaches reasoning process, not just outcome

---

## 🎓 **Training Recommendations**

### **For 120-Sample Dataset:**

**Training Parameters:**
- **Epochs:** 5-7 (more epochs needed for reasoning)
- **Batch Size:** 2-4
- **Learning Rate:** 1e-5 (lower for reasoning stability)
- **LoRA Rank:** 32 (higher for complex reasoning)
- **LoRA Alpha:** 64

**Expected Training Time (A100):**
- ~3-5 minutes total

**Evaluation:**
Test on cases requiring:
1. Doctrine selection
2. Alternative rejection
3. Ambiguous fact patterns

---

## 📁 **Files**

- `legal_training_1000.json` - Old format (491 samples)
- `legal_reasoning_dataset.json` - New format (120 samples)
- `create_real_dataset.py` - Old generator
- `create_reasoning_dataset.py` - New generator

---

## ✅ **Next Steps**

1. **Upload** `legal_reasoning_dataset.json` to Colab
2. **Train** with new parameters (5-7 epochs, rank 32)
3. **Test** on ambiguous cases
4. **Compare** with old dataset results
5. **Iterate** based on performance

---

## 🎯 **Success Criteria**

Model should:
- ✅ Identify competing doctrines
- ✅ Explain why alternatives fail
- ✅ Show step-by-step reasoning
- ✅ Stop at conclusion (no hallucination)
- ✅ Handle ambiguous cases
- ✅ Provide justified conclusions

**The goal:** Teach the model to **think like a lawyer**, not memorize law.
