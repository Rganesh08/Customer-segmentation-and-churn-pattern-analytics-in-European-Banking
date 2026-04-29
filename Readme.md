Churn-Analysis-Dashboard-European-Banking-Sector-Overview
Data Analytics Portfolio Projects

🏦 European Banking Customer Churn Analysis
Project Overview
This project analyzes customer churn behavior across three European banks using a cleaned dataset of 10,000 clients.
The objective is to identify key drivers behind churn and retention — focusing on geography, gender, age group, loyalty level, and satisfaction and propose actionable strategies for improving customer retention.

Dataset Summary
Total customers: 10,000
Churned customers: 2,038
Overall churn rate: 20.38%
Average age: 38.9 years

Main variables analyzed:

Geography (France, Germany, Spain)
Gender
Age, Age group (Young, Middle-aged, Senior)
Tenure (years with the bank)
Fidelity Level (High, Medium, Low)
Satisfaction Score (1–5)
Complain (Yes/No)
Number of Products
Balance, Estimated Salary
Key Insights
Geographic Insights
Germany shows the highest churn rate (≈32.4%), nearly double that of France and Spain.
Indicates potential product, pricing, or service issues specific to the German market.
Gender
Female churn rate: 25.1% ♀
Male churn rate: 16.5% ♂ Suggests communication or service experience gaps by gender.
Age Group
Age Group	Customers	Churn Rate
Senior	1,261	44.6%
Middle-aged	7,098	19.0%
Young	1,641	7.6%
Senior customers are at the highest risk — need tailored retention programs focusing on simpler products, direct assistance and benefits for that key population

💬 Complaints (Critical Variable)
Complain	Customers	Churn Rate
Yes	2,044	99.5%
No	7,956	0.05%
This is the most alarming insight: nearly every customer who filed a complaint churned.
→ Indicates unresolved issues or reactive complaint management.
→ Immediate priority for business intervention.

Satisfaction
Churn rates across satisfaction levels (1–5) remain fairly stable (~19–22%), suggesting that satisfaction alone does not explain churn.
When combined with complaints, however, churn rises sharply.

Fidelity Level
Fidelity Level	Churn Rate
High	20.21%
Medium	19.64%
Low	20.93%
Loyalty level alone does not significantly impact churn — other behavioral or experience variables drive the outcome.

Tenure
Early-tenure clients (0–1 years) show slightly higher churn (~23%), suggesting early dissatisfaction or onboarding expectations.
Business Interpretation
Main causes of churn:

Poor complaint management (near 100% attrition for complainers).
Germany and Senior segments are disproportionately affected.
Female customers show higher churn than males.
Early-tenure churn reveals onboarding gaps.
Main retention opportunities:

Resolve complaint-handling bottlenecks and track satisfaction post-resolution.
Design loyalty or care programs for Senior and German customers.
Improve first-year onboarding and customer education.
Personalize offers based on gender and product portfolio.

https://churn-pattern-analytics.streamlit.app/
