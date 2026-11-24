# SafeTriage Evaluation Metrics & Research Methodology

This document specifies the mathematical formulations, evaluation denominators, and error handling protocols used in the SafeTriage research laboratory.

---

## 1. Urgency Ordering & Ground Truth Mapping

The triage framework operates across 4 discrete ordinal tiers:

$$\text{Urgency Rank}: \quad \text{Level 1} = 1 < \text{Level 2} = 2 < \text{Level 3} = 3 < \text{Level 4} = 4$$

where rank 1 represents the highest medical urgency and rank 4 represents the lowest medical urgency.

Let $y_i \in \{\text{Level 1}, \text{Level 2}, \text{Level 3}, \text{Level 4}\}$ denote the reference ground-truth category for test case $i$, and $\hat{y}_i$ denote the model's predicted category.

An explicit comparison function is used across the system:

```python
URGENCY_RANK = {
    "Level 1": 1,
    "Level 2": 2,
    "Level 3": 3,
    "Level 4": 4,
}

def is_more_urgent(a: str, b: str) -> bool:
    return URGENCY_RANK[a] < URGENCY_RANK[b]

def is_less_urgent(a: str, b: str) -> bool:
    return URGENCY_RANK[a] > URGENCY_RANK[b]
```

---

## 2. Metric Formulations

### 2.1 Multiclass Accuracy
Fraction of test cases where the predicted category matches the reference category:

$$\text{Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(\hat{y}_i = y_i)$$

where $N$ is the total number of evaluated test cases (including failed and unparseable outputs).

### 2.2 Per-Class Precision, Recall, and F1
For class $c \in \{\text{Level 1}, \text{Level 2}, \text{Level 3}, \text{Level 4}\}$:

$$\text{Precision}_c = \frac{TP_c}{TP_c + FP_c + \epsilon}$$

$$\text{Recall}_c = \text{Sensitivity}_c = \frac{TP_c}{TP_c + FN_c + \epsilon}$$

$$\text{F1}_c = 2 \times \frac{\text{Precision}_c \times \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c + \epsilon}$$

where $\epsilon = 10^{-9}$ prevents division by zero when a class has no predictions or true instances.

### 2.3 Macro and Weighted F1-Scores
- **Macro F1**: Unweighted mean of per-class F1-scores, giving equal importance to rare critical categories:
  $$\text{Macro F1} = \frac{1}{|C|} \sum_{c \in C} \text{F1}_c$$
- **Weighted F1**: Mean of per-class F1-scores weighted by class prevalence $N_c$:
  $$\text{Weighted F1} = \sum_{c \in C} \frac{N_c}{N} \text{F1}_c$$

### 2.4 4x4 Confusion Matrix
A $4 \times 4$ matrix where rows represent reference true categories and columns represent predicted categories:

$$\text{CM}[r, c] = \sum_{i=1}^{N} \mathbb{I}(y_i = r \land \hat{y}_i = c)$$

---

## 3. Patient Safety Metrics: Under-Triage and Over-Triage

In medical triage research, clinical safety is asymmetric: **under-triage** (failing to recognize severe illness) presents severe clinical risk, while **over-triage** (precautionary escalation) primarily incurs healthcare utilization overhead.

### 3.1 Under-Triage Rate
An under-triage occurs when the model predicts a category that is **less urgent** than the ground truth:

$$\text{Under-Triaged Case}: \quad \text{URGENCY\_RANK}[\hat{y}_i] > \text{URGENCY\_RANK}[y_i]$$

The system computes two standard denominators:

1. **Overall Under-Triage Rate**:
   $$\text{Under-Triage Rate}_{\text{overall}} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{URGENCY\_RANK}[\hat{y}_i] > \text{URGENCY\_RANK}[y_i])}{N}$$
   *Denominator*: Total number of evaluated cases $N$.

2. **Eligible-Denominator Under-Triage Rate**:
   Since Level 4 cases cannot be under-triaged (they are already the lowest urgency tier), we also report:
   $$\text{Under-Triage Rate}_{\text{eligible}} = \frac{\sum_{i: y_i \neq \text{Level 4}} \mathbb{I}(\text{URGENCY\_RANK}[\hat{y}_i] > \text{URGENCY\_RANK}[y_i])}{\sum_{i=1}^{N} \mathbb{I}(y_i \neq \text{Level 4})}$$

### 3.2 Over-Triage Rate
An over-triage occurs when the model predicts a category that is **more urgent** than the ground truth:

$$\text{Over-Triaged Case}: \quad \text{URGENCY\_RANK}[\hat{y}_i] < \text{URGENCY\_RANK}[y_i]$$

$$\text{Over-Triage Rate}_{\text{overall}} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{URGENCY\_RANK}[\hat{y}_i] < \text{URGENCY\_RANK}[y_i])}{N}$$

$$\text{Over-Triage Rate}_{\text{eligible}} = \frac{\sum_{i: y_i \neq \text{Level 1}} \mathbb{I}(\text{URGENCY\_RANK}[\hat{y}_i] < \text{URGENCY\_RANK}[y_i])}{\sum_{i=1}^{N} \mathbb{I}(y_i \neq \text{Level 1})}$$

### 3.3 Red-Flag Emergency Sensitivity
Measures the recall specifically on Level 1 (Emergency) cases:

$$\text{Red-Flag Sensitivity} = \frac{\sum_{i: y_i = \text{Level 1}} \mathbb{I}(\hat{y}_i = \text{Level 1})}{\sum_{i=1}^{N} \mathbb{I}(y_i = \text{Level 1})}$$

A safe clinical triage system requires this metric to be near $1.00$ ($100\%$). In SafeTriage, the deterministic safety engine enforces this invariant.

---

## 4. Error Handling and Failed Prediction Accounting

When evaluating external or experimental models (such as an LLM provider):
- **Provider Timeout / Connection Error**: The test case is recorded as `error="Provider timeout"`.
- **Malformed / Unparseable Output**: If a model produces invalid text that cannot be parsed into one of the 4 valid triage levels, it is flagged as `error="Invalid category schema"`.
- **Accounting in Denominators**: Failed predictions are **never** silently discarded or dropped from the denominator. In benchmark reporting, a failed prediction is counted as incorrect ($0$ accuracy) and recorded under the `errors` count to maintain reproducibility and unbiased reporting.
