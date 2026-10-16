# campus-green-space-analysis
Python analysis of campus green-space perceptions, engagement, and student well-being.

## Project Overview
This project uses Python to investigate the relationship between campus green-space perceptions, engagement with green spaces, and student well-being. The goal was to test the hypothesis: "Students who perceive campus green spaces as providing a greater sense of being away will report higher well-being, with green-space engagement potentially mediating this relationship"

## Research Questions

Are perceptions of campus green spaces associated with student well-being?
Is green-space engagement associated with student well-being?
Does student well-being vary across age groups and campus environments?
Does green-space engagement help explain the relationship between perceived being away and well-being?

## Tools
Tools: Python, pandas, Matplotlib, Seaborn, SciPy, and statsmodels

## Analysis
Data cleaning
Descriptive statistics and correlation analysis
Regression analysis
Group comparisons using t-tests and ANOVA
Mediation analysis with bootstrap confidence intervals
Data visualization

## Key Findings

Green-space engagement was positively correlated with student well-being (r = 0.382, p = 0.0004). Students reporting greater engagement also tended to report higher well-being. This association does not establish causation.

### Mediation analysis

The estimated indirect effect of perceived being away on well-being through green-space engagement was 0.227. The 95% bootstrap confidence interval ranged from -0.016 to 0.527, including zero. Therefore, the analysis did not find statistically significant evidence of mediation at the 5% significance level.

### Limitations
The data are observational, so the results cannot establish cause and effect. Missing responses and the available sample may also limit how broadly the findings can be generalized.

### Visualizations
This repository includes visualizations of the relationships between green-space engagement, student well-being, correlations among study variables, demographic group comparisons, and the mediation model.

### Green-Engagement and Student Well-being











