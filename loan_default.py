# Importing the necessary libraries
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# Loading the data
df = pd.read_csv("Loan_default.csv")

print("Data loaded succesfully")
print(f"Shape: {df.shape}")
print(df.head())

# exploring the data
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTarget column distribution:")
print(df['Default'].value_counts())

# cleaning the data
# dropping a column
df = df.drop('LoanID', axis=1)

encoders = {}
categorical_cols = ['Education', 'EmploymentType', 'MaritalStatus','HasMortgage', 'HasDependents', 'LoanPurpose', 'HasCoSigner']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

print("Cleaning done")
print(df.head())


X = df.drop('Default', axis=1)
Y = df['Default']


print(f"Features shape: {X.shape}")
print(f"Target shape: {Y.shape}")

# Train Test Split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape}")
print(f"Testing set size:  {X_test.shape}")


# train the model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

log_model = LogisticRegression(max_iter=1000, class_weight='balanced')
log_model.fit(X_train_scaled, Y_train)

tree_model = DecisionTreeClassifier(random_state=42, class_weight='balanced')
tree_model.fit(X_train, Y_train)

forest_model = RandomForestClassifier(random_state=42, class_weight='balanced')
forest_model.fit(X_train, Y_train)

print("All 3 models trained successfully")


# Evaluating the trained models
log_pred = log_model.predict(X_test_scaled)
print("\n-- LOGISTIC REGRESSION ---")
print(f"Accuracy: {accuracy_score(Y_test, log_pred):.4f}")
print(classification_report(Y_test, log_pred))
print(confusion_matrix(Y_test, log_pred))

# decision tree
tree_pred = tree_model.predict(X_test)
print("\n-- DECISION TREE ---")
print(f"Accuracy: {accuracy_score(Y_test, tree_pred):.4f}")
print(classification_report(Y_test, tree_pred))
print(confusion_matrix(Y_test, tree_pred))

# Random Forest
forest_pred = forest_model.predict(X_test)
print("\n-- RANDOM FOREST ---")
print(f"Accuracy: {accuracy_score(Y_test, forest_pred):.4f}")
print(classification_report(Y_test, forest_pred))
print(confusion_matrix(Y_test, forest_pred))

# comparing models
print("\n--- MODEL COMPARISON ---")
print(f"Logistic Regression - Accuracy: {accuracy_score(Y_test, log_pred):.4f}, Recall (Default=1): {classification_report(Y_test, log_pred, output_dict=True)['1']['recall']:.4f} ")
print(f"Decision Tree        - Accuracy: {accuracy_score(Y_test, tree_pred):.4f}, Recall (Default=1): {classification_report(Y_test, tree_pred, output_dict=True)['1']['recall']:.4f}")
print(f"Random Forest        - Accuracy: {accuracy_score(Y_test, forest_pred):.4f}, Recall (Default=1): {classification_report(Y_test, forest_pred, output_dict=True)['1']['recall']:.4f}")


# # training the production model
production_model = DecisionTreeClassifier(random_state=42)
production_model.fit(X_train, Y_train)

joblib.dump(production_model, 'loan_default_model.pkl')
joblib.dump(encoders, 'encoders.pkl')

print("Production model and encoders saved")

for col in categorical_cols:
    print(f"{col}: {encoders[col].classes_}")

def predict_loan_default(applicant):
    # converting categorical inputs using saved encoders
    for col in categorical_cols:
        applicant[col] = encoders[col].transform([applicant[col]])[0]

    # dataframe for applicant data
    applicant_df = pd.DataFrame([applicant])

    prediction = production_model.predict(applicant_df)[0]
    probability = production_model.predict_proba(applicant_df)[0][1]

    # risk 
    if probability < 0.3:
        risk = "LOW RISK"
    elif probability < 0.6:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"
    
    print("\n--- LOAN DEFAULT PREDICTION ---")
    print(f"Default Prediction : {'YES - WILL DEFAULT' if prediction == 1 else 'NO - WILL Not Default'}")
    print(f"Defualt Probability : {probability:.2%}")
    print(f"Risk Category : {risk}")
    print("----------------------------")


    # Test with example applicants

# Applicant 1 - Low risk profile
applicant1 = {
    'Age': 45,
    'Income': 120000,
    'LoanAmount': 20000,
    'CreditScore': 780,
    'MonthsEmployed': 120,
    'NumCreditLines': 3,
    'InterestRate': 5.5,
    'LoanTerm': 24,
    'DTIRatio': 0.15,
    'Education': "Bachelor's",
    'EmploymentType': 'Full-time',
    'MaritalStatus': 'Married',
    'HasMortgage': 'Yes',
    'HasDependents': 'No',
    'LoanPurpose': 'Home',
    'HasCoSigner': 'No'
}

# Applicant 2 - High risk profile
applicant2 = {
    'Age': 23,
    'Income': 18000,
    'LoanAmount': 150000,
    'CreditScore': 320,
    'MonthsEmployed': 2,
    'NumCreditLines': 1,
    'InterestRate': 22.0,
    'LoanTerm': 60,
    'DTIRatio': 0.85,
    'Education': 'High School',
    'EmploymentType': 'Unemployed',
    'MaritalStatus': 'Single',
    'HasMortgage': 'No',
    'HasDependents': 'Yes',
    'LoanPurpose': 'Other',
    'HasCoSigner': 'No'
}

print(("\nTesting precition tool..."))
predict_loan_default(applicant1)
predict_loan_default(applicant2)

        
