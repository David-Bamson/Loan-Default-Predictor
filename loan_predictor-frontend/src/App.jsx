import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    Title: '',
    FirstName: '',
    LastName: '',
    Age: '',
    Income: '',
    LoanAmount: '',
    CreditScore: '',
    MonthsEmployed: '',
    NumCreditLines: '',
    InterestRate: '',
    LoanTerm: '',
    DTIRatio: '',
    Education: '',
    EmploymentType: '',
    MaritalStatus: '',
    HasMortgage: '',
    HasDependents: '',
    LoanPurpose: '',
    HasCoSigner: ''
  })

  const [result, setResult] = useState(null)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const { Title, FirstName, LastName, ...modelFields } = formData

    const payload = {
      ...modelFields,
      Age: parseInt(formData.Age),
      Income: parseInt(formData.Income),
      LoanAmount: parseInt(formData.LoanAmount),
      CreditScore: parseInt(formData.CreditScore),
      MonthsEmployed: parseInt(formData.MonthsEmployed),
      NumCreditLines: parseInt(formData.NumCreditLines),
      InterestRate: parseFloat(formData.InterestRate),
      LoanTerm: parseInt(formData.LoanTerm),
      DTIRatio: parseFloat(formData.DTIRatio)
    }

    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const data = await response.json()
    setResult({ ...data, Title, FirstName, LastName })
  }

  const riskClass = result
    ? result.risk === 'LOW RISK'
      ? 'low'
      : result.risk === 'MEDIUM RISK'
      ? 'medium'
      : 'high'
    : ''

  return (
    <div className="page">
      <div className="dossier">
        <header className="dossier-header">
          <p className="eyebrow">Risk Assessment File</p>
          <h1>Loan Default Predictor</h1>
          <div className="rule" />
        </header>

        <form onSubmit={handleSubmit} className="dossier-form">
          <fieldset className="section">
            <legend>Applicant</legend>
            <div className="grid grid-3">
              <label className="field">
                <span>Title</span>
                <select name="Title" value={formData.Title} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Mr">Mr</option>
                  <option value="Mrs">Mrs</option>
                  <option value="Miss">Miss</option>
                  <option value="Dr">Dr</option>
                </select>
              </label>
              <label className="field">
                <span>First Name</span>
                <input type="text" name="FirstName" placeholder="John" value={formData.FirstName} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Last Name</span>
                <input type="text" name="LastName" placeholder="Doe" value={formData.LastName} onChange={handleChange} />
              </label>
            </div>
          </fieldset>

          <fieldset className="section">
            <legend>Financial Profile</legend>
            <div className="grid grid-3">
              <label className="field">
                <span>Age</span>
                <input type="number" name="Age" placeholder="0" value={formData.Age} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Annual Income</span>
                <input type="number" name="Income" placeholder="0" value={formData.Income} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Credit Score</span>
                <input type="number" name="CreditScore" placeholder="0" value={formData.CreditScore} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Months Employed</span>
                <input type="number" name="MonthsEmployed" placeholder="0" value={formData.MonthsEmployed} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Credit Lines</span>
                <input type="number" name="NumCreditLines" placeholder="0" value={formData.NumCreditLines} onChange={handleChange} />
              </label>
              <label className="field">
                <span>DTI Ratio</span>
                <input type="number" step="0.01" name="DTIRatio" placeholder="0.00" value={formData.DTIRatio} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Education</span>
                <select name="Education" value={formData.Education} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Bachelor's">Bachelor's</option>
                  <option value="High School">High School</option>
                  <option value="Master's">Master's</option>
                  <option value="PhD">PhD</option>
                </select>
              </label>
              <label className="field">
                <span>Employment Type</span>
                <select name="EmploymentType" value={formData.EmploymentType} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Full-time">Full-time</option>
                  <option value="Part-time">Part-time</option>
                  <option value="Self-employed">Self-employed</option>
                  <option value="Unemployed">Unemployed</option>
                </select>
              </label>
              <label className="field">
                <span>Marital Status</span>
                <select name="MaritalStatus" value={formData.MaritalStatus} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Divorced">Divorced</option>
                  <option value="Married">Married</option>
                  <option value="Single">Single</option>
                </select>
              </label>
              <label className="field">
                <span>Dependents</span>
                <select name="HasDependents" value={formData.HasDependents} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </label>
            </div>
          </fieldset>

          <fieldset className="section">
            <legend>Loan Terms</legend>
            <div className="grid grid-3">
              <label className="field">
                <span>Loan Amount</span>
                <input type="number" name="LoanAmount" placeholder="0" value={formData.LoanAmount} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Interest Rate %</span>
                <input type="number" step="0.1" name="InterestRate" placeholder="0.0" value={formData.InterestRate} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Loan Term (months)</span>
                <input type="number" name="LoanTerm" placeholder="0" value={formData.LoanTerm} onChange={handleChange} />
              </label>
              <label className="field">
                <span>Loan Purpose</span>
                <select name="LoanPurpose" value={formData.LoanPurpose} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="Auto">Auto</option>
                  <option value="Business">Business</option>
                  <option value="Education">Education</option>
                  <option value="Home">Home</option>
                  <option value="Other">Other</option>
                </select>
              </label>
              <label className="field">
                <span>Has Mortgage</span>
                <select name="HasMortgage" value={formData.HasMortgage} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </label>
              <label className="field">
                <span>Has Co-Signer</span>
                <select name="HasCoSigner" value={formData.HasCoSigner} onChange={handleChange}>
                  <option value="">Select</option>
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </label>
            </div>
          </fieldset>

          <button type="submit" className="submit-btn">Assess Application</button>
        </form>

        {result && (
          <div className={`verdict verdict-${riskClass}`}>
            <div className="stamp">
              <span>{result.risk}</span>
            </div>
            <p className="verdict-line">
              {result.Title} {result.FirstName} {result.prediction === 1 ? 'will default' : 'will not default'}
            </p>
            <p className="verdict-probability">
              {(result.probability * 100).toFixed(2)}<span>% probability</span>
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App