import pandas as pd
import numpy as np

## Data Cleaning


# header = 0, skip row 1 because it contains survey response options instead of
df = pd.read_csv("Campus Green Space.csv", header=0, skiprows=[1])

# shape
# print(df.shape)
# # count location
# print(df["City where your college or university is located"].value_counts(dropna=False))


# # count location
# print(df["City where your college or university is located"].value_counts(dropna=False))

# location clean
df["location_clean"] = df["City where your college or university is located"].str.lower().str.strip()

# print(print(df["location_clean"].value_counts(dropna=False)))

# non midwest
non_midwest = ["los angeles", "san francisco", "new york", "ny", "texas"]

# remove values that are not midwest
df = df[~df["location_clean"].isin(non_midwest)]

print(df.head())
print(df["location_clean"].value_counts(dropna=False))

print(len(df["location_clean"]))

# look at columns
print(df.columns.tolist())

# WHO-5
# WHO-5 columns
who5_cols = df.columns[156:186]

import numpy as np

who5_cols = df.columns[156:186]

for i in range(5):
    question_cols = who5_cols[i * 6:(i + 1) * 6]

    # Find which answer-choice column was selected
    answered = df[question_cols].notna().sum(axis=1)

    scores = df[question_cols].notna().values.argmax(axis=1)
    scores = (5 - scores).astype(float)

    scores[answered == 0] = np.nan
    scores[answered > 1] = np.nan

    df[f"WHO5_{i + 1}"] = scores

# Total only when all 5 WHO-5 questions were answered
df["WHO5_total"] = df[[f"WHO5_{i}" for i in range(1, 6)]].sum(
    axis=1, min_count=5
) * 4


# checking usable who-5 scores
print("Missing WHO-5:", df["WHO5_total"].isna().sum())
print("Usable WHO-5:", df["WHO5_total"].notna().sum())


# PRS subscale scores
df["PRS_BeingAway"] = df.iloc[:, 141:146].sum(axis=1, min_count=5)
df["PRS_Fascination"] = df.iloc[:, 146:151].sum(axis=1, min_count=5)
df["PRS_Compatibility"] = df.iloc[:, 151:156].sum(axis=1, min_count=5)



# check
print(df[["PRS_BeingAway", "PRS_Fascination", "PRS_Compatibility"]].head(20))

# how many have all 3 subscales
print("Complete PRS:", df[[
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]].notna().all(axis=1).sum())

# green engagement score



outdoor = df.iloc[:, 64:69].bfill(axis=1).iloc[:, 0]

outdoor_scores = {
    "Frequently": 4,
    "Sometimes": 3,
    "Not very much": 2,
    "Rarely": 1,
    "Not applicable / No outdoor green space available": 0
}

df["Outdoor_score"] = outdoor.map(outdoor_scores)
print(df["Outdoor_score"].head())

activity_scores = {
    "1-3 times daily": 5,
    "1-3 times weekly": 4,
    "1-3 times monthly": 3,
    "Rarely": 2,
    "Never": 1,
    "Not applicable / no outdoor green spaces available": 0
}

for start in range(69, 123, 6):
    activity = df.iloc[:, start:start+6].bfill(axis=1).iloc[:, 0]
    df[f"score_{start}"] = activity.map(activity_scores)

print(df.iloc[:, -10:].head(10))

for col in df.columns[-10:]:
    print(col, df[col].unique())


# final green score calculation
score_cols = [col for col in df.columns if col.startswith("score_")]

df[score_cols] = df[score_cols].fillna(0)
df["Outdoor_score"] = df["Outdoor_score"].fillna(0)

df["Green_Engagement_Score"] = (
    df["Outdoor_score"] + df[score_cols].sum(axis=1)
)

print(df["Green_Engagement_Score"].describe())


# checking missingness
analysis_vars = [
    "Green_Engagement_Score",
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]

print(df[analysis_vars].isna().sum())
print(df[analysis_vars].isna().mean() * 100)

# complete cases
complete_cases = df[
    df[
        [
            "Green_Engagement_Score",
            "WHO5_total",
            "PRS_BeingAway",
            "PRS_Fascination",
            "PRS_Compatibility"
        ]
    ].notna().all(axis=1)
]

print("Complete cases:", len(complete_cases))
# so 67 full cases

# now check for partial missingness
analysis_vars = [
    "Green_Engagement_Score",
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]

missing_count = df[analysis_vars].isna().sum(axis=1)

print(missing_count.value_counts().sort_index())

# checking green engagement
green_cols = df.columns[64:123]

green_missing = df[green_cols].isna().all(axis=1)

print("Completely blank green-space section:", green_missing.sum())

print(df.loc[green_missing, green_cols].head())

# modifying green space score
green_cols = df.columns[64:123]

green_blank = df[green_cols].isna().all(axis=1)

df.loc[green_blank, "Green_Engagement_Score"] = np.nan

print(df["Green_Engagement_Score"].isna().sum())
print(df["Green_Engagement_Score"].describe())

# recalculating missingness
analysis_vars = [
    "Green_Engagement_Score",
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]

missing_count = df[analysis_vars].isna().sum(axis=1)

print(missing_count.value_counts().sort_index())

# Checking the 8 cases missing 1 variable
eight_cases = df.loc[missing_count == 1, analysis_vars]

print(eight_cases.isna())

print(
    df.loc[
        missing_count == 1,
        [
            "PRS_BeingAway",
            "PRS_Fascination",
            "PRS_Compatibility"
        ]
    ]
)

print(df[
    ["PRS_BeingAway", "PRS_Fascination", "PRS_Compatibility"]
].mean())

missing_prs = (
    df["PRS_BeingAway"].isna() |
    df["PRS_Fascination"].isna() |
    df["PRS_Compatibility"].isna()
)

print(df.loc[
    missing_prs,
    df.columns[141:156]
])


# fill 8 cases with mean
df["PRS_BeingAway"] = df["PRS_BeingAway"].fillna(df["PRS_BeingAway"].mean())
df["PRS_Fascination"] = df["PRS_Fascination"].fillna(df["PRS_Fascination"].mean())
df["PRS_Compatibility"] = df["PRS_Compatibility"].fillna(df["PRS_Compatibility"].mean())

analysis_vars = [
    "Green_Engagement_Score",
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]

print(df[analysis_vars].notna().all(axis=1).sum())

# select 81 good cases
analysis_vars = [
    "Green_Engagement_Score",
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility"
]

complete_81 = df[analysis_vars].notna().all(axis=1)

df_81 = df.loc[complete_81].copy()

print(df_81.shape)

# save as new csv
df_81.to_csv("Campus_Green_Space_Clean.csv", index=False)


## Demographic Data
# Gender Frequency Table
gender_cols = ["Gender:", "Unnamed: 24", "Unnamed: 25", "Unnamed: 26", "Unnamed: 27"]

gender = df_81[gender_cols].replace(r"^\s*$", pd.NA, regex=True).bfill(axis=1).iloc[:, 0].dropna()

gender_counts = gender.value_counts()

gender_table = pd.DataFrame({
    "Frequency": gender_counts,
    "Percentage": (gender_counts / gender_counts.sum() * 100).round(1)
})

print(gender_table)

# Age Frequency Table
age_bins = [17, 20, 23, 26, 30]
# Create age ranges
age_labels = ["18–20", "21–23", "24–26", "27–30"]

age_ranges = pd.cut(
    df_81["Age"],
    bins=age_bins,
    labels=age_labels
)

age_counts = age_ranges.value_counts().sort_index()

age_table = pd.DataFrame({
    "Frequency": age_counts,
    "Percentage": (age_counts / age_counts.sum() * 100).round(1)
})

print(age_table)

# Urban vs Suburban Frequency Table
print(df_81.columns.tolist())
location_cols = [
    "Is your college in an urban or suburban environment?",
    "Unnamed: 19"
]

location = (
    df_81[location_cols]
    .replace(r"^\s*$", pd.NA, regex=True)
    .bfill(axis=1)
    .iloc[:, 0]
    .dropna()
)

location_counts = location.value_counts()

location_table = pd.DataFrame({
    "Frequency": location_counts,
    "Percentage": (location_counts / location_counts.sum() * 100).round(1)
})

print(location_table)

# Race Frequency Table
race_cols = [
    "Race/ethnicity (Please select all that apply)",
    "Unnamed: 29", "Unnamed: 30", "Unnamed: 31",
    "Unnamed: 32", "Unnamed: 33", "Unnamed: 34",
    "Unnamed: 35", "Unnamed: 36"
]

race_data = df_81[race_cols].replace(r"^\s*$", pd.NA, regex=True)

race_counts = race_data.stack().value_counts()

race_table = pd.DataFrame({
    "Frequency": race_counts,
    "Percentage": (race_counts / len(df_81) * 100).round(1)
})

print(race_table)

# Socioeconomic Status Frequency Table
ses_cols = [
    "Socioeconomic status (self-perceived):",
    "Unnamed: 38",
    "Unnamed: 39",
    "Unnamed: 40",
    "Unnamed: 41"
]

ses = (
    df_81[ses_cols]
    .replace(r"^\s*$", pd.NA, regex=True)
    .bfill(axis=1)
    .iloc[:, 0]
    .dropna()
)

ses_counts = ses.value_counts()

ses_table = pd.DataFrame({
    "Frequency": ses_counts,
    "Percentage": (ses_counts / ses_counts.sum() * 100).round(1)
})

print(ses_table)

# Statistical Analysis
# Pearson Correlation
from scipy.stats import pearsonr

predictors = [
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility",
    "Green_Engagement_Score"
]

outcome = "WHO5_total"

for predictor in predictors:
    r, p = pearsonr(df_81[predictor], df_81[outcome])
    print(f"{predictor}: r = {r:.3f}, p = {p:.4f}")

# Multilinear Regression
import statsmodels.api as sm

X = df_81[predictors]
y = df_81[outcome]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())


# Gender t-test
from scipy.stats import ttest_ind
test_data = pd.DataFrame({
    "Gender": gender,
    "WHO5_total": df_81["WHO5_total"]
}).dropna()

male = df_81.loc[gender == "Male", "WHO5_total"].dropna()
female = df_81.loc[gender == "Female", "WHO5_total"].dropna()
# Descriptive statistics
print("Male: n =", len(male), "| Mean =", round(male.mean(), 2),
      "| SD =", round(male.std(), 2))
print("Female: n =", len(female), "| Mean =", round(female.mean(), 2),
      "| SD =", round(female.std(), 2))

# Welch's independent-samples t-test
t_stat, p_value = ttest_ind(male, female, equal_var=False)

print("t =", round(t_stat, 3))
print("p =", round(p_value, 4))

# Urban vs Suburban t-test
campus_col = "Is your college in an urban or suburban environment?"
suburban_col = "Unnamed: 19"

urban = df_81.loc[
    df_81[campus_col] == "Urban", "WHO5_total"
].dropna()

suburban = df_81.loc[
    df_81[suburban_col] == "Suburban", "WHO5_total"
].dropna()

print("Urban: n =", len(urban),
      "| Mean =", round(urban.mean(), 2),
      "| SD =", round(urban.std(), 2))

print("Suburban: n =", len(suburban),
      "| Mean =", round(suburban.mean(), 2),
      "| SD =", round(suburban.std(), 2))

t_stat, p_value = ttest_ind(urban, suburban, equal_var=False)

print("t =", round(t_stat, 3))
print("p =", round(p_value, 4))

# ANOVA of age range
from scipy.stats import f_oneway

age_bins = [17, 20, 23, 30]
# new grouping
age_labels = ["18–20", "21–23", "24–30"]

age_ranges = pd.cut(
    df_81["Age"],
    bins=age_bins,
    labels=age_labels
)

groups = [
    df_81.loc[age_ranges == age_group, "WHO5_total"].dropna()
    for age_group in age_labels
]

for age_group, scores in zip(age_labels, groups):
    print(age_group, "n =", len(scores), "| Mean =", round(scores.mean(), 2))

f_stat, p_value = f_oneway(*groups)

print("F =", round(f_stat, 3))
print("p =", round(p_value, 4))

# Mediation Analysis

# Select the three variables
data = df_81[[
    "PRS_BeingAway",
    "Green_Engagement_Score",
    "WHO5_total"
]].dropna()

# Path a: Does Being Away predict Green Engagement?
model_a = sm.OLS(
    data["Green_Engagement_Score"],
    sm.add_constant(data[["PRS_BeingAway"]])
).fit()

# Paths b and c': Does Green Engagement predict well-being, while accounting for Being Away?
model_b = sm.OLS(
    data["WHO5_total"],
    sm.add_constant(data[["PRS_BeingAway", "Green_Engagement_Score"]])
).fit()

# Calculate the indirect effect
indirect_effect = (
    model_a.params["PRS_BeingAway"]
    * model_b.params["Green_Engagement_Score"]
)

print("Path a:", model_a.params["PRS_BeingAway"])
print("Path b:", model_b.params["Green_Engagement_Score"])
print("Indirect effect:", indirect_effect)

# bootstrap
indirect_effects = []

for i in range(5000):
    sample = data.sample(n=len(data), replace=True)

    model_a = sm.OLS(
        sample["Green_Engagement_Score"],
        sm.add_constant(sample[["PRS_BeingAway"]])
    ).fit()

    model_b = sm.OLS(
        sample["WHO5_total"],
        sm.add_constant(sample[["PRS_BeingAway", "Green_Engagement_Score"]])
    ).fit()

    a = model_a.params["PRS_BeingAway"]
    b = model_b.params["Green_Engagement_Score"]

    indirect_effects.append(a * b)

lower = np.percentile(indirect_effects, 2.5)
upper = np.percentile(indirect_effects, 97.5)

print("95% confidence interval:", round(lower, 3), "to", round(upper, 3))

# Visualizations
# scatterplot

import matplotlib.pyplot as plt

# Remove rows missing either variable
plot_data = df_81[
    ["Green_Engagement_Score", "WHO5_total"]
].dropna()

# Create the scatter plot
plt.scatter(
    plot_data["Green_Engagement_Score"],
    plot_data["WHO5_total"]
)

# Add a trendline
x = plot_data["Green_Engagement_Score"]
y = plot_data["WHO5_total"]

slope, intercept = np.polyfit(x, y, 1)

plt.plot(x, slope * x + intercept, label="Trendline")

equation = f"y = {slope:.2f}x + {intercept:.2f}"
plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes,
         verticalalignment="top")

plt.legend()

# Label the chart
plt.xlabel("Green Engagement Score")
plt.ylabel("Well-Being Score (WHO-5)")
plt.title("Green Engagement and Student Well-Being")

plt.tight_layout()
plt.show()

# Correlation heat map
import seaborn as sns
import matplotlib.pyplot as plt

variables = [
    "WHO5_total",
    "PRS_BeingAway",
    "PRS_Fascination",
    "PRS_Compatibility",
    "Green_Engagement_Score"
]

correlations = df_81[variables].corr()

sns.heatmap(
    correlations,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    fmt=".2f"
)

plt.title("Correlations Between Green Space Perceptions and Well-Being")
plt.tight_layout()
plt.show()

# Well-being across demographic groups
campus_col = "Is your college in an urban or suburban environment?"
suburban_col = "Unnamed: 19"

plot_data = df_81.copy()

plot_data["Campus"] = (
    plot_data[campus_col]
    .fillna(plot_data[suburban_col])
)

sns.boxplot(
    data=plot_data,
    x="Campus",
    y="WHO5_total"
)

plt.title("Student Well-Being by Campus Environment")
plt.xlabel("Campus Environment")
plt.ylabel("WHO-5 Well-Being Score")

plt.tight_layout()
plt.show()

# Well-being age ranges ANOVA
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Group ages
age_bins = [17, 20, 23, 30]
age_labels = ["18–20", "21–23", "24–30"]

plot_data = df_81.copy()

plot_data["Age_Group"] = pd.cut(
    plot_data["Age"],
    bins=age_bins,
    labels=age_labels
)

# Create box plot
sns.boxplot(
    data=plot_data,
    x="Age_Group",
    y="WHO5_total"
)

plt.title("Student Well-Being by Age Group")
plt.xlabel("Age Group")
plt.ylabel("WHO-5 Well-Being Score")

plt.tight_layout()
plt.show()

# Mediation diagram
import matplotlib.pyplot as plt

# Create the diagram
plt.figure(figsize=(10, 5))

# Draw the three boxes
plt.text(0.15, 0.6, "Perceived Being Away",
         ha="center",
         bbox=dict(boxstyle="round", facecolor="lightblue"))

plt.text(0.5, 0.6, "Green-Space Engagement",
         ha="center",
         bbox=dict(boxstyle="round", facecolor="lightgreen"))

plt.text(0.85, 0.6, "Student Well-Being",
         ha="center",
         bbox=dict(boxstyle="round", facecolor="lightblue"))

# Draw arrows between the boxes
plt.annotate("", xy=(0.39, 0.6), xytext=(0.27, 0.6),
             arrowprops=dict(arrowstyle="->"))

plt.annotate("", xy=(0.74, 0.6), xytext=(0.62, 0.6),
             arrowprops=dict(arrowstyle="->"))

# Show the path coefficients
plt.text(0.33, 0.68, "a = 0.309", ha="center")
plt.text(0.68, 0.68, "b = 0.736", ha="center")

# Show the indirect effect and confidence interval
plt.text(0.5, 0.3,
         "Indirect Effect = 0.227\n95% CI: -0.016 to 0.527",
         ha="center")

# Add a title and clean up the diagram
plt.title("Mediation Analysis: Green Space and Well-Being")
plt.xlim(0, 1)
plt.ylim(0.15, 0.85)
plt.axis("off")

plt.show()