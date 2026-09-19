# Statistical Inference Core

**Statistical inference** is the process of using data from a **sample** to draw conclusions about a larger **population**, while accounting for uncertainty.

![Image](https://images.openai.com/static-rsc-4/VWsnOGDe8OIaLyXJJRg4K73KQdNBGt8xfCzvwJuG9TvM_Dtx4NC5E4fOItPt4tvDzvP5xvZSBMr88m6s-KI_1hW--ZZq6uga52wCBFssJDTJZxAZNDG2tFWhsatosl-RIOD4PDaeaSQTzIp6MgDezrCNpEFNyo--588lA6TZSmGdf6zHhwnYRY_Zsf_5hYuu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GYM9gCqmnPtv1XjFp1yEF9GlX9nbHYTU-XL-n9ZCQj2mZZ76p_rqxhou0fgYfwJG4FuQQqxgSD4FFjt0lZonzGQUHwbRWEnHQ4Cf0dTFIvy8MZgaPcO61JMWGvK7HgK8SYcH7nLA-j-kvRN1sSk0xlMUGRhdxTzuYlvxORpHowJP0KLNsIbyWG81qksWH5DX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pDTXh2gE4i0bQbvbSqIq7RthNi6xeAAy-7aBuHxOCP_M0RXe14ntppMxksy3xlosMe3q6rP2X4PY1nBU228sARgyoywpdeOdQq3jCrToDQEr0eLa2MorBplGzMrDDkGwDlKVpkPBP3ORRXrLmj7_ZWJwE13QPmXXUYdvKl0dxdIqynujwzQk2Y3iTzo2zHGq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ECHOkCjKELtunuWXs6xjNh2R3QG-W5VqWj2k5enUEo0zQKlPj8AryVdVAOXBqOIiqrBZs6UlnDCDve55Oya7BkeFDWL9w46seEcjKAePMoUwIgp1bHmsybWk1UPXnjSnrxyvwgwAk2JDoNira1vCdMFm4zPorhAHGGTWL1I_q37cIBsacrdLWmQi3tXhNqem?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CjS4fSphHrkOv99p9t0k4NYDK-7_tnpTwGL9LJo9ZbS-tUv7CciMCkEuM7je7tQ4WiVpkIIsTyZ0wF9XjynOu1M-ccvJTMNZOlPfhSH4rF5antCWKy6r0fDyc1G1tmagl_kPkBoLbrxOGNvWGJew3rd3ghXcRxjimPAF3SO4Fh-2v2IrkEnuaF1hCrk3O3g6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/vAjEXio-ga3KuSTsPUnW2bnaFhOjB1VBVOCMuqskwXTW-mGuA3qnfS8_O9-lbgd-2ARFf5bZPmOYAO_DSIQUlFDZayBTm4LYRjpnIHc-irhTSXUmz3UBP31GopUHQ2yqPrJugu71s7U449SoGcJaQSc3sx8H7wu0qTRaXGKEBcg9SUp_ff-NKGYpIxKKor1O?purpose=fullsize)

### 1. Population and Sample

* **Population:** The entire group we want to understand.
* **Sample:** A subset of the population that we actually observe.
* **Parameter:** A numerical characteristic of the population, e.g. population mean \(\mu\).
* **Statistic:** A numerical characteristic calculated from the sample, e.g. sample mean \(\bar{x}\).

Example:

> We want to know the average income of all university students. We survey 500 students.

* Population → all university students
* Sample → 500 surveyed students
* Population mean → \(\mu\)
* Sample mean → \(\bar{x}\)

---

### 2. Sampling

The quality of inference depends heavily on **how the sample was obtained**.

Common sampling methods include:

* Simple random sampling
* Stratified sampling
* Cluster sampling
* Systematic sampling
* Convenience sampling

A **representative random sample** allows us to generalize results more credibly.

---

### 3. Sampling Distribution

A **sampling distribution** describes how a statistic behaves across repeated samples.

For example, imagine repeatedly taking samples of size \(n\) and calculating their means:

$$
\bar X_1,\bar X_2,\bar X_3,\ldots
$$

The distribution of these sample means is the **sampling distribution of \(\bar X\)**.

For a population with mean \(\mu\) and standard deviation \(\sigma\):

$$
E(\bar X)=\mu
$$

and

$$
SE(\bar X)=\frac{\sigma}{\sqrt n}
$$

where \(SE\) is the **standard error**.

---

### 4. Central Limit Theorem

The **Central Limit Theorem (CLT)** is fundamental to statistical inference.

Under appropriate conditions, as sample size becomes sufficiently large, the sampling distribution of the sample mean becomes approximately normal:

$$
\bar X \approx N\left(\mu,\frac{\sigma^2}{n}\right)
$$

This is important because it allows us to make probability statements and construct confidence intervals even when the original population is not normally distributed.

---

### 5. Point Estimation

A **point estimate** is a single number used to estimate an unknown population parameter.

Examples:

$$
\hat{\mu}=\bar{x}
$$

$$
\hat{p}=\frac{x}{n}
$$

where:

* \(\hat{\mu}\) estimates the population mean \(\mu\)
* \(\hat p\) estimates the population proportion \(p\)

Good estimators are often evaluated using properties such as:

* **Unbiasedness**
* **Consistency**
* **Efficiency**
* **Minimum variance**

---

### 6. Confidence Intervals

A **confidence interval (CI)** gives a range of plausible values for a population parameter.

A general form is:

$$
\text{estimate} \pm \text{margin of error}
$$

For example, a 95% CI for a mean might be:

$$
\bar{x}\pm t^*\frac{s}{\sqrt n}
$$

A crucial interpretation:

> A 95% confidence procedure produces intervals that contain the true parameter in approximately 95% of repeated samples.

It is technically incorrect to say that there is a 95% probability that the fixed population parameter is inside a particular calculated interval.

---

### 7. Hypothesis Testing

Hypothesis testing evaluates evidence about a population claim.

We typically specify:

$$
H_0: \text{null hypothesis}
$$

$$
H_A: \text{alternative hypothesis}
$$

Example:

$$
H_0:\mu=50
$$

$$
H_A:\mu\ne50
$$

We then calculate a **test statistic** and determine how compatible the observed data are with \(H_0\).

---

### 8. P-value

The **p-value** is the probability, assuming \(H_0\) is true, of obtaining a result at least as extreme as the observed result.

Small p-value → data are relatively inconsistent with \(H_0\).

For example:

$$
p=0.02
$$

means that, **if the null hypothesis were true**, results at least this extreme would occur with probability 0.02 under the specified testing procedure.

A p-value is **not**:

* the probability that \(H_0\) is true;
* the probability that the result occurred "by chance";
* a measure of the size or practical importance of an effect.

---

### 9. Significance Level

The **significance level**, usually denoted \(\alpha\), is the threshold used for hypothesis testing.

Common choice:

$$
\alpha=0.05
$$

Decision rule:

$$
p<\alpha \Rightarrow \text{reject }H_0
$$

$$
p\ge\alpha \Rightarrow \text{fail to reject }H_0
$$

We generally say **"fail to reject"**, rather than "accept the null hypothesis."

---

### 10. Type I and Type II Errors

Hypothesis testing can produce two major errors:

| Reality       | Decision               | Result            |
| ------------- | ---------------------- | ----------------- |
| \(H_0\) true  | Reject \(H_0\)         | **Type I error**  |
| \(H_0\) false | Fail to reject \(H_0\) | **Type II error** |

#### Type I error

$$
P(\text{Type I error})=\alpha
$$

It is a **false positive**.

#### Type II error

$$
P(\text{Type II error})=\beta
$$

It is a **false negative**.

The **power** of a test is:

$$
\text{Power}=1-\beta
$$

Power is the probability of detecting an effect when a specified effect actually exists.

---

### 11. Statistical vs Practical Significance

These are different concepts.

Suppose a study finds:

$$
p<0.001
$$

This may constitute strong statistical evidence against \(H_0\), but the actual effect might be extremely small.

For example, a treatment could reduce blood pressure by only **0.2 mmHg** in a huge sample. It might be statistically significant but practically unimportant.

Therefore, inference should consider:

**effect size + uncertainty + practical context**, not merely the p-value.

---

### 12. Common Statistical Tests

Different questions require different inferential procedures.

| Question                                   | Common method          |
| ------------------------------------------ | ---------------------- |
| One population mean                        | One-sample \(t\)-test  |
| Two independent means                      | Two-sample \(t\)-test  |
| Paired observations                        | Paired \(t\)-test      |
| One/two proportions                        | Proportion tests       |
| Categorical variables                      | Chi-square test        |
| Several group means                        | ANOVA                  |
| Association between quantitative variables | Correlation/regression |
| Predicting an outcome                      | Regression             |

---

### 13. Regression and Inference

In linear regression:

$$
Y=\beta_0+\beta_1X+\epsilon
$$

we use sample data to estimate the unknown parameters:

$$
\hat\beta_0,\quad\hat\beta_1
$$

Inference can then be performed on these coefficients.

For example:

$$
H_0:\beta_1=0
$$

tests whether there is evidence of a linear association between \(X\) and \(Y\), conditional on the model assumptions.

---

### 14. Assumptions

Statistical inference depends on assumptions. Common ones include:

* Independence
* Random sampling or appropriate study design
* Normality or approximate normality where required
* Homogeneity of variance
* Correct model specification
* Absence of severe outliers

Violating assumptions can make confidence intervals, p-values, and standard errors unreliable.

---

### 15. Bias vs Variability

Two major sources of inferential error are:

**Bias:** Systematic deviation from the true population parameter.

**Variability:** Random differences between samples.

Increasing sample size generally reduces **sampling variability**, because:

$$
SE(\bar X)=\frac{\sigma}{\sqrt n}
$$

But increasing \(n\) **does not automatically eliminate bias**.

This distinction is fundamental: **a very large biased sample can still produce a very precise but wrong estimate.**

---

## The Big Picture

You can organize statistical inference into this sequence:

$$
\boxed{
\text{Population}
\rightarrow
\text{Sample}
\rightarrow
\text{Statistic}
\rightarrow
\text{Sampling Distribution}
\rightarrow
\text{Uncertainty}
\rightarrow
\text{Inference}
}
$$

And the two central branches are:

$$
\boxed{\text{Estimation}}
$$

→ point estimates
→ confidence intervals

and

$$
\boxed{\text{Hypothesis Testing}}
$$

→ null/alternative hypotheses
→ test statistic
→ p-value
→ decision