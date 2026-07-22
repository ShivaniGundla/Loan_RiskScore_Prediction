"""

> # Loan Applicant Risk Assessment System Using Machine Learning
  A decision support tool for banks.

# Problem Statement

Banks receive thousands of loan applications every day. Approving loans without assessing the applicant's financial condition can increase the likelihood of loan defaults and financial losses. Traditional risk assessment often relies on manual evaluation, which is time-consuming and may introduce inconsistencies.

The objective of this project is to develop a machine learning model that predicts an applicant's Risk Score using demographic, financial, employment, and credit-related information. The predicted risk score assists bank employees in making informed lending decisions.

# Objective

The objectives of this project are:

- Develop a regression model to predict applicant Risk Score.
- Compare multiple machine learning algorithms.
Identify the most influential factors affecting risk.
- Deploy the trained model using Streamlit.
- Allow bank employees to enter customer details and obtain an instant risk assessment.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(r'C:\Users\shiva\Documents\Downloads\LoanPredictionApp\Loan.csv')

data.columns

data['EmploymentStatus'].unique()

data.shape

data.head()

"""**Observations**
- EmploymentStatus, EducationLevel, MaritalStatus,HomeOwnershipStatus, LoanPurpose are Categorical Data Columns

- NumberOfDependents, NumberOfOpenCreditLines,NumberOfCreditInquiries, BankruptcyHistory, PreviousLoanDefaults, Loan Approval are Discrete Numerical Data Columns.

- Age, AnnualIncome, CreditScore,Experience, LoanAmount, LoanDuration,MonthlyDebtPayments, CreditCardUtilizationRate, DebtToIncomeRatio,PaymentHistory, SavingsAccountBalance, CheckingAccountBalance,TotalAssets, TotalLiability, MonthlyIncome, UtilityBillsPaymentHistory, JobTenure, NetWorth, InterestRate, MonthlyLoanPayment, TotalDebtToIncomeRatio, RiskScore

"""

data = data.drop(columns = ['ApplicationDate'])

data.info()

"""# **Columns Description**

**Applicant Information**
- ApplicationDate
- Age
- MaritalStatus
- NumberOfDependents:  *Number of family members financially dependent on the applicant.*
- EducationLevel: *Highest educational qualification attained by the applicant.*

**Employment Information**
- EmploymentStatus: *Current employment status of the applicant*
- Experience: *Total years of work experience of the applicant*
- AnnualIncome: *Total Annual Income earned by the applicant.*
- monthlyIncome: *Average monthly income earned by the applicant.*
- JobTenure: *Number of years the applicant has worked with the current employer.*

**Loan Information**
- LoanAmount: *Amount of loan requested by applicant*
- LoanDuration: *Repayment period of the loan, usually in months.*
- LoanPurpose: *Purpose for which the loan is requested.*

**Credit Profile**
- CreditScore: *Numerical measure of the applicant's credit worthiness.*
- LengthOfCreditHistory: *Number of years the applicant has maintained credit accounts.*
- NumberOfOpenCreditLines: *Number of active credit accounts held by the applicant.*
- NumberOfCreditInquiries: *Number of recent credit inquiries made by lenders.*
- CreditCardUtilizationRate: *Percentage of available credit card limit currently utilized.*

- PaymentHistory: *Historical record or score of the applicant's loan repayment behaviour.*

**Financial Information**

- SavingsAccountBalance: *Current balance in the applicant's savings account.*

- CheckingAccountBalance: *Current balance in the applicant's checking/current account.*

- TotalAssets: *Total monetary value of assets owned by the applicant.*

- TotalLiabilities: *Total outstanding financial liabilities of the applicant.*

- NetWorth: *Net financial worth of the applicant after considering assets and liabilities.*

- HomeOwnershipStatus: *Ownership status of the applicant's residence.*

**Debt Information**
- MonthlyDebtPayments: *Total monthly payments made towards existing debts.*

- DebtToIncomeRatio: *Ratio of total monthly debt payments to monthly income.*

- TotalDebtToIncomeRatio: *Ratio of total financial obligations (including the new loan) to monthly income.*

**Credit Behaviour/ Financial History**

- BankruptcyHistory: *Indicates whether the applicant has previously declared bankruptcy.(0 - No, 1 = Yes)*

- PreviousLoanDefaults: *Indicates whether the applicant has defaulted on previous loans.(0 = No, 1 = Yes)*

- UtilityBillsPaymentHistory:
*Record or score indicating the applicant's history of paying utility bills on time.*


**Bank Decision Variables**

These variables are generated after the bank evaluates the loan application and therefore should generally not be used as input features for predicting risk before a lending decision.

- BaseInterestRate: *Standard interest rate set by the bank before customer-specific adjustments.*

- InterestRate: *Final interest rate assigned to the applicant based on the bank's assessment.*

- MonthlyLoanPayment: *Estimated monthly repayment amount for the approved loan.*

- LoanApproved: *Final loan approval decision.(0 = Rejected, 1 = Approved)*

**Target Variable**

- RiskScore: *Credit risk score assigned to the applicant, representing the overall lending risk associated with the loan application*

# Detect Missing Values
"""

print(data.isnull().sum().sum())

"""**Observations**
- There are no missing values.

# Detect Duplicates
"""

print(data.duplicated().sum())

"""Observations
- There are no duplicate values

# Feature Engineering

# Remove Unnecessary Columns

- Remove Target Leakage
   - We need to drop LoanAprroved Column.
   - In the dataset, we need to drop InterestRate, BaseInterestRate, MonthlyLoanPayment columns as they are usually defined after risk assessment
- Redundant Columns
   - AnnualIncome and MonthlyIncome give same information, drop AnnualIncome.

- From the dataset, NetWorth ≠ (TotalAssets − TotalLiabilities) , NetWorth is derived from assets and liabilities. Create calculated  networth column with assets and liabilities column
"""

data = data.drop(columns = ['LoanApproved','InterestRate','BaseInterestRate','MonthlyLoanPayment','AnnualIncome'])

data['CalculatedNetWorth'] = data['TotalAssets'] - data['TotalLiabilities']

mismatch = ~np.isclose(
    data["NetWorth"],
    data["CalculatedNetWorth"],
    atol=1e-2  # tolerance of 0.01
)

print("Number of mismatched rows:", mismatch.sum())
print("Percentage:", mismatch.mean() * 100)

networth_corr = data['CalculatedNetWorth'].corr(data['NetWorth'])
print(networth_corr)

"""**Observations**

During feature engineering, the original NetWorth column was validated against the standard financial formula (Total Assets − Total Liabilities) and was found to be inconsistent in approximately 24% of the records. Therefore, the original feature was replaced with a recalculated NetWorth to ensure financial correctness, improve data consistency, and align the model with the calculations performed in the deployed Streamlit application.
- Now, drop TotalAssets and TotalLiabilities and NetWorth column
"""

data = data.drop(columns = ['TotalAssets','TotalLiabilities','NetWorth','TotalDebtToIncomeRatio',])

data.info()

data.head(3)

plt.subplot(1,2,1)
sns.histplot(data, x = 'RiskScore')
plt.title('Histogram of RiskScore')

plt.subplot(1,2,2)
sns.boxplot(data, y = 'RiskScore')
plt.title('Histogram of RiskScore')
plt.tight_layout()

categorical_features = data.select_dtypes(include=['object']).columns.tolist()
binary_features = ['BankruptcyHistory','PreviousLoanDefaults']
discrete_numeric_features = ['PaymentHistory','LengthOfCreditHistory','LoanDuration','JobTenure','NumberOfDependents','NumberOfOpenCreditLines','NumberOfCreditInquiries']
numerical_features = [
    col for col in data.select_dtypes(include=['int64', 'float64']).columns
    if col not in (binary_features + discrete_numeric_features + ['RiskScore'])
]

"""# Categorical Columns Distribution"""

plt.figure(figsize = (20,30))
for i, col in enumerate(categorical_features):
    plt.subplot(5,1,i+1)
    sns.countplot(x=data[col])
    plt.title(col)
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""# Discrete Numerical Columns Distribution"""

for col in discrete_numeric_features:
    print(f"{col}: {data[col].nunique()} unique values")

plt.figure(figsize = (18,12))
for i, col in enumerate(discrete_numeric_features):
     plt.subplot(4,2,i+1)
     sns.countplot(data = data, x = col)
     plt.title(col)
plt.tight_layout()
plt.show()

"""# Binary Numerical Columns Distribution"""

plt.figure(figsize = (10,5))
for i, col in enumerate(binary_features):
    plt.subplot(1,2,i+1)
    ax = sns.countplot(x = data[col])
    for container in ax.containers:
        ax.bar_label(container)
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel("count")
plt.tight_layout()
plt.show()

"""# Numerical Columns Distribution"""

plt.figure(figsize = (20,16))
for i, col in enumerate(numerical_features):
    plt.subplot(7,2,i+1)
    sns.histplot(data[col], kde=True)
    plt.title(col)
plt.tight_layout()
plt.show()

plt.figure(figsize = (20,30))
for i, col in enumerate(numerical_features):
    plt.subplot(7,2,i+1)
    sns.boxplot(data[col])
    plt.title(col)
plt.tight_layout()
plt.show()

data.columns

"""**Observation**
- Numerical data columns have outliers and do not follow normal distribution.

# Split Features and Target
- Target is RiskScore, it is a Regression Problem.
"""

x = data.drop(columns = ['RiskScore'])
y = data['RiskScore']

data.columns

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

x_train.columns

data['EducationLevel'].unique()

# x_train.head()
# x_test.head()

# y_train.head()
# y_test.head()

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler,OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

transformer = ColumnTransformer(transformers = [('t1', RobustScaler(),numerical_features),
                                                ('t2', RobustScaler(),discrete_numeric_features),
                                                ('t3',OrdinalEncoder(),categorical_features),
                                                ('t4','passthrough',binary_features)])

x_train.head()

x_train_trans = transformer.fit_transform(x_train)
# x_train column names are given here because it is the initial dataset
x_train_trans = pd.DataFrame(
    x_train_trans,
    columns=transformer.get_feature_names_out(),
    index=x_train.index
)

x_train_trans.columns

"""# Model Building"""

lr_pipeline = make_pipeline(transformer, LinearRegression())
lr_pipeline.fit(x_train, y_train)
lr_ypred = lr_pipeline.predict(x_test)

knn_pipeline = make_pipeline(transformer, KNeighborsRegressor())
knn_pipeline.fit(x_train, y_train)
knn_ypred = knn_pipeline.predict(x_test)

dt_pipeline = make_pipeline(transformer, DecisionTreeRegressor())
dt_pipeline.fit(x_train, y_train)
dt_ypred = dt_pipeline.predict(x_test)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
rf_pipeline = make_pipeline(transformer,RandomForestRegressor(random_state = 42, n_jobs = -1))

rf_pipeline.fit(x_train, y_train)

rf_ypred = rf_pipeline.predict(x_test)

print("R² Score :", r2_score(y_test, rf_ypred))

"""# Compare Models"""

results = pd.DataFrame({
    "Model": ["Linear Regression", "KNN", "Decision Tree","RandomForest"],
    "R2 Score": [
        r2_score(y_test, lr_ypred),
        r2_score(y_test, knn_ypred),
        r2_score(y_test, dt_ypred),
        r2_score(y_test, rf_ypred)
    ]
})

results.sort_values(by="R2 Score", ascending=False)

"""# Hyperparameter Tuning"""

from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'randomforestregressor__n_estimators': [100, 200],
    'randomforestregressor__max_depth': [10,20, None],
    'randomforestregressor__min_samples_split': [2, 5],
    'randomforestregressor__min_samples_leaf': [1, 2],
    'randomforestregressor__max_features': ['sqrt', 'log2', None]
}

random_search = RandomizedSearchCV(
    estimator=rf_pipeline,
    param_distributions=param_dist,
    n_iter=10,
    cv=3,
    scoring='r2',
    random_state=42,
    n_jobs=-1,
    verbose=2
)

random_search.fit(x_train, y_train)

best_rf = random_search.best_estimator_

print("Best Parameters:", random_search.best_params_)
print("Best CV R²:", random_search.best_score_)
y_pred = best_rf.predict(x_test)

print("Test R²:", r2_score(y_test, y_pred))

# # Hyperparameter tuning
# from sklearn.model_selection import GridSearchCV
# param_grid = {
#     'linearregression__fit_intercept': [True, False]
# }

# # Grid Search
# grid_lr = GridSearchCV(
#     estimator=lr_pipeline,
#     param_grid=param_grid,
#     scoring='r2',
#     cv=5,
#     n_jobs=-1,
#     verbose=2
# )

# # Train
# grid_lr.fit(x_train, y_train)

y_pred = best_rf.predict(x_test)

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

print("R2 Score :", r2_score(y_test, y_pred))

import joblib
joblib.dump(rf_pipeline,'Loan_Model.pkl')