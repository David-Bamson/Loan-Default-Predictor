from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd


model = joblib.load('loan_default_model.pkl')
encoders = joblib.load('encoders.pkl')
categorical_cols = ['Education', 'EmploymentType', 'MaritalStatus','HasMortgage', 'HasDependents', 'LoanPurpose', 'HasCoSigner']

class LoanApplicant(BaseModel):
    Age: int
    Income: int
    LoanAmount: int
    CreditScore: int
    MonthsEmployed: int
    NumCreditLines: int
    InterestRate: float
    LoanTerm: int
    DTIRatio: float
    Education: str
    EmploymentType: str
    MaritalStatus: str
    HasMortgage: str
    HasDependents: str
    LoanPurpose: str
    HasCoSigner: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return{"message": "Hello World"}


@app.post("/predict")
def loanApplicant(data: LoanApplicant):
    df = pd.DataFrame([data.dict()])
    for col in categorical_cols:
        df[col] = encoders[col].transform(df[col])

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    if probability < 0.3:
        risk = "LOW RISK"
    elif probability < 0.6:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"

    return {
        "prediction": prediction, 
        "probability": probability,
        "risk": risk
    }
    
