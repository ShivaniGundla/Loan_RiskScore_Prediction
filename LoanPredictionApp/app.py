# ============================================================
# IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan Risk Assessment System",
    page_icon="🏦",
    layout="wide"
)
st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#F5F7FA;
}

/* Headers */
h1,h2,h3{
    color:#003366;
    font-weight:700;
}

/* Metric Cards */
[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:18px;
    border-left:6px solid #0056B3;
    box-shadow:0px 4px 10px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button{
    background-color:#003366;
    color:white;
    border-radius:8px;
    border:none;
    height:3em;
    font-weight:600;
}

.stButton > button:hover{
    background-color:#0056B3;
    color:white;
}

/* Text Inputs */
.stTextInput input,
.stNumberInput input{
    border-radius:8px;
    border:1px solid #BFC9D1;
}

/* Select Boxes */
.stSelectbox div[data-baseweb="select"]{
    border-radius:8px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#003366;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Success Messages */
[data-testid="stAlert"]{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load("Loan_Model.pkl")

# ============================================================
# EMPLOYEE LOGIN DETAILS
# ============================================================

EMPLOYEES = {
    "manager": "manager123",
    "employee1": "bank123",
    "loanofficer": "loan123"
}

# ============================================================
# PENDING APPLICATION FILE
# ============================================================

PENDING_FILE = "pending_applications.csv"

# Create the file automatically if it doesn't exist

if not os.path.exists(PENDING_FILE):

    pending_columns = [

        "LoanID",
        "Status",

        "Age",
        "CreditScore",
        "EmploymentStatus",
        "EducationLevel",
        "Experience",

        "LoanAmount",
        "LoanDuration",

        "MaritalStatus",
        "NumberOfDependents",

        "HomeOwnershipStatus",

        "MonthlyDebtPayments",
        "CreditCardUtilizationRate",

        "NumberOfOpenCreditLines",
        "NumberOfCreditInquiries",

        "DebtToIncomeRatio",

        "BankruptcyHistory",

        "LoanPurpose",

        "PreviousLoanDefaults",

        "PaymentHistory",

        "LengthOfCreditHistory",

        "SavingsAccountBalance",

        "CheckingAccountBalance",

        "MonthlyIncome",

        "UtilityBillsPaymentHistory",

        "JobTenure",

        "CalculatedNetWorth"

    ]

    pd.DataFrame(columns=pending_columns).to_csv(
        PENDING_FILE,
        index=False
    )

# ============================================================
# LOAN ID GENERATOR
# ============================================================
COMPLETED_FILE = "Completed_Applications.csv"

def generate_loan_id():

    loan_ids = []

    # Read Pending IDs
    if os.path.exists(PENDING_FILE):

        pending = pd.read_csv(PENDING_FILE)

        if not pending.empty:

            loan_ids.extend(
                pending["LoanID"]
                .astype(str)
                .str.replace("L", "", regex=False)
                .astype(int)
                .tolist()
            )

    # Read Completed IDs
    if os.path.exists(COMPLETED_FILE):

        completed = pd.read_csv(COMPLETED_FILE)

        if not completed.empty:

            loan_ids.extend(
                completed["LoanID"]
                .astype(str)
                .str.replace("L", "", regex=False)
                .astype(int)
                .tolist()
            )

    if not loan_ids:
        return "L1"

    return f"L{max(loan_ids)+1}"


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "action" not in st.session_state:
    st.session_state.action = None

if "loan_id" not in st.session_state:
    st.session_state.loan_id = None

if "application_started" not in st.session_state:
    st.session_state.application_started = False

if "form_open" not in st.session_state:
    st.session_state.form_open = False

if "pending_app" not in st.session_state:
    st.session_state.pending_app = None

if "username" not in st.session_state:
    st.session_state.username = None


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <h1 style='text-align:center;color:#003366;'>
        🏦 ABC National Bank
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h3 style='text-align:center;'>
        Loan Risk Assessment System
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    left, centre, right = st.columns([1,2,1])

    with centre:

        st.subheader("Employee Login")

        username = st.text_input(
            "Employee ID"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True,
            type="primary"
        ):

            if (username in EMPLOYEES and EMPLOYEES[username] == password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(
                    "Invalid Employee ID or Password."
                )
        st.info("""
### 🔑 Demo Login Credentials

**Username:** employee1

**Password:** bank123

Use the above credentials to explore the demo loan risk assessment system.
""")

    st.stop()


# ============================================================
# BANK HEADER
# ============================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#003366,#0059b3);
padding:18px;
border-radius:12px;
color:white">

<h1>🏦 ABC National Bank</h1>

<p>Loan Risk Assessment Portal</p>

</div>
""", unsafe_allow_html=True)

st.write(
"""
Enter the applicant's information to estimate the **Risk Score**.
"""
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏦 ABC National Bank")
st.sidebar.success(f"Logged in as: {st.session_state.username}")

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    key="logout_sidebar",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.action = None
    st.session_state.loan_id = None
    st.session_state.form_open = False
    st.session_state.pending_app = None
    st.session_state.application_started = False

    st.rerun()

# ============================================================
# EMPLOYEE DASHBOARD
# ============================================================

st.title("Employee Dashboard")

# ============================================================
# DASHBOARD SUMMARY
# ============================================================

# Pending Applications
if os.path.exists(PENDING_FILE):
    pending_df = pd.read_csv(PENDING_FILE)
    pending_count = len(pending_df)
else:
    pending_count = 0

# Completed Applications
if os.path.exists(COMPLETED_FILE):
    completed_df = pd.read_csv(COMPLETED_FILE)
    completed_count = len(completed_df)
else:
    completed_count = 0

# Total Applications
total_applications = pending_count + completed_count

# Dashboard Metrics
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📂 Pending Applications",
        pending_count
    )

with c2:
    st.metric(
        "✅ Completed Applications",
        completed_count
    )

with c3:
    st.metric(
        "📄 Total Applications",
        total_applications
    )

with c4:
    st.metric(
        "👤 Employee",
        st.session_state.username
    )
st.markdown("---")

st.info("Select an option to continue.")

col1, col2 = st.columns(2)

# ============================================================
# CREATE NEW APPLICATION
# ============================================================

with col1:

    if st.button(
        "🆕 Create New Application",
        use_container_width=True,
        type="primary"
        if st.session_state.action == "new"
        else "secondary"
    ):

        st.session_state.action = "new"

        # Generate Loan ID ONLY if there is no active application
        if not st.session_state.application_started:

            st.session_state.loan_id = generate_loan_id()

            st.session_state.application_started = True

        st.session_state.form_open = False

        st.session_state.pending_app = None

        st.rerun()

# ============================================================
# PENDING APPLICATIONS
# ============================================================

with col2:

    if st.button(
        "📂 Pending Applications",
        use_container_width=True,
        type="primary"
        if st.session_state.action == "pending"
        else "secondary"
    ):

        st.session_state.action = "pending"

        st.session_state.form_open = False

        st.rerun()

st.markdown("---")

# ============================================================
# WAIT UNTIL USER SELECTS
# ============================================================

if st.session_state.action is None:

    st.stop()

# ============================================================
# NEW APPLICATION
# ============================================================

if st.session_state.action == "new":

    st.subheader("🆕 New Loan Application")

    st.success(
        f"Loan ID : {st.session_state.loan_id}"
    )
    st.info(f"""
### Current Application

**Loan ID:** {st.session_state.loan_id}

**Status:** {'Pending' if st.session_state.action=='pending' else 'New Application'}

""")

    app = None

    if not st.session_state.form_open:

        st.info(
            "Click **Open Application Form** to begin entering applicant details."
        )

        if st.button(
            "Open Application Form",
            type="primary",
            use_container_width=True
        ):

            st.session_state.form_open = True

            st.rerun()

        st.stop()

# ============================================================
# PENDING APPLICATION
# ============================================================

elif st.session_state.action == "pending":

    st.subheader("📂 Pending Loan Applications")

    pending_df = pd.read_csv(PENDING_FILE)

    pending_df = pending_df[
        pending_df["Status"] == "Pending"
    ]

    if pending_df.empty:

        st.warning(
            "No pending applications available."
        )

        st.stop()

    loan_id = st.selectbox(

        "Loan ID",

        pending_df["LoanID"],

        index=None,

        placeholder="Select Loan ID"

    )

    if loan_id is None:

        st.stop()

    if st.button(
        "Open Application Form",
        type="primary",
        use_container_width=True
    ):

        app = pending_df[
            pending_df["LoanID"] == loan_id
        ].iloc[0]

        st.session_state.loan_id = loan_id

        st.session_state.pending_app = app.to_dict()

        st.session_state.form_open = True

        st.rerun()

    if not st.session_state.form_open:

        st.stop()

    app = st.session_state.pending_app

    st.success(
        f"{st.session_state.loan_id} loaded successfully."
    )

# ============================================================
# DEFAULT VALUES
# ============================================================

if app is None:

    defaults = {

        "Age": None,
        "CreditScore": None,
        "EmploymentStatus": None,
        "EducationLevel": None,
        "Experience": None,
        "LoanAmount": None,
        "LoanDuration": None,
        "MaritalStatus": None,
        "NumberOfDependents": None,
        "HomeOwnershipStatus": None,
        "MonthlyDebtPayments": None,
        "CreditCardUtilizationRate": None,
        "NumberOfOpenCreditLines": None,
        "NumberOfCreditInquiries": None,
        "DebtToIncomeRatio": None,
        "BankruptcyHistory": None,
        "LoanPurpose": None,
        "PreviousLoanDefaults": None,
        "PaymentHistory": None,
        "LengthOfCreditHistory": None,
        "SavingsAccountBalance": None,
        "CheckingAccountBalance": None,
        "MonthlyIncome": None,
        "UtilityBillsPaymentHistory": None,
        "JobTenure": None,
        "CalculatedNetWorth": None

    }

else:

    defaults = app.copy()

    for key in defaults:

        if pd.isna(defaults[key]):

            defaults[key] = None

st.markdown("---")

# ============================================================
# APPLICATION FORM STARTS HERE
# ============================================================
# ============================================================
# APPLICANT INFORMATION
# ============================================================

st.header("👤 Applicant Information")

col1, col2 = st.columns(2)

education_options = [
    "Associate",
    "Bachelor",
    "Master",
    "Doctorate",
    "High School"
]

marital_options = [
    "Single",
    "Married",
    "Divorced",
    "Widowed"
]

with col1:

    age = st.number_input(
        "Age (Years)",
        min_value=18,
        max_value=100,
        value=None if defaults["Age"] is None else int(defaults["Age"]),
        placeholder="Enter applicant age",
        help="Applicant's current age in completed years."
    )

    education_value = defaults.get("EducationLevel")

    education_index = (
        education_options.index(education_value)
        if education_value in education_options
        else None
    )

    education = st.selectbox(
        "Education Level",
        education_options,
        index=education_index,
        placeholder="Select Education Level"
    )


with col2:

    marital_value = defaults.get("MaritalStatus")

    marital_index = (
        marital_options.index(marital_value)
        if marital_value in marital_options
        else None
    )

    marital = st.selectbox(
        "Marital Status",
        marital_options,
        index=marital_index,
        placeholder="Select Marital Status"
    )

    dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        value=None if defaults["NumberOfDependents"] is None else int(defaults["NumberOfDependents"]),
        placeholder="Enter number of dependents"
    )

st.markdown("---")

# ============================================================
# EMPLOYMENT INFORMATION
# ============================================================

st.header("💼 Employment Information")

employment_options = [
    "Employed",
    "Self-Employed",
    "Unemployed"
]

home_options = [
    "Own",
    "Mortgage",
    "Rent",
    "Other"
]

col1, col2 = st.columns(2)

with col1:

    employment_value = defaults.get("EmploymentStatus")

    employment_index = (
        employment_options.index(employment_value)
        if employment_value in employment_options
        else None
    )

    employment = st.selectbox(
        "Employment Status",
        employment_options,
        index=employment_index,
        placeholder="Select Employment Status"
    )

    experience = st.number_input(
        "Work Experience (Years)",
        min_value=0,
        value=None if defaults["Experience"] is None else int(defaults["Experience"]),
        placeholder="Enter years of experience"
    )


with col2:

    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0.0,
        value=None if defaults["MonthlyIncome"] is None else float(defaults["MonthlyIncome"]),
        placeholder="Enter monthly income"
    )

    job_tenure = st.number_input(
        "Job Tenure (Years)",
        min_value=0,
        value=None if defaults["JobTenure"] is None else int(defaults["JobTenure"]),
        placeholder="Enter years in current job",
        help="Number of years with the current employer."
    )
st.markdown("---")

# ============================================================
# LOAN INFORMATION
# ============================================================

st.header("🏦 Loan Information")

purpose_options = [
    "Home",
    "Auto",
    "Education",
    "Debt Consolidation",
    "Other"
]

col1, col2 = st.columns(2)

with col1:

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=None if defaults["LoanAmount"] is None else float(defaults["LoanAmount"]),
        placeholder="Enter requested loan amount"
    )


    loan_duration_options = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]

    loan_duration = st.selectbox(
    "Loan Duration (Months)",
    loan_duration_options,
    index=loan_duration_options.index(int(defaults["LoanDuration"]))
    if pd.notna(defaults["LoanDuration"]) and int(defaults["LoanDuration"]) in loan_duration_options
    else None,
    placeholder="Select Loan Duration",
    help="Choose the loan repayment period in months."
)   

with col2:

    purpose_value = defaults.get("LoanPurpose")

    purpose_index = (
        purpose_options.index(purpose_value)
        if purpose_value in purpose_options
        else None
    )

    purpose = st.selectbox(
        "Loan Purpose",
        purpose_options,
        index=purpose_index,
        placeholder="Select Loan Purpose"
    )

st.markdown("---")


# ============================================================
# FINANCIAL INFORMATION
# ============================================================

st.header("🏦 Financial Information")

col1, col2 = st.columns(2)

with col1:

    savings = st.number_input(
        "Savings Account Balance",
        min_value=0.0,
        value=None if defaults["SavingsAccountBalance"] is None else float(defaults["SavingsAccountBalance"]),
        placeholder="Enter savings balance",
        help="Current balance available in the applicant's savings account."
    )
    checking = st.number_input(
        "Checking Account Balance",
        min_value=0.0,
        value=None if defaults["CheckingAccountBalance"] is None else float(defaults["CheckingAccountBalance"]),
        placeholder="Current balance available in the applicant's checking/current account."
    )

with col2:

    home_value = defaults.get("HomeOwnershipStatus")

    home_index = (
        home_options.index(home_value)
        if home_value in home_options
        else None
    )

    home = st.selectbox(
        "Home Ownership Status",
        home_options,
        index=home_index,
        placeholder="Select Home Ownership Status"
    )

    networth = st.number_input(
    "Calculated Net Worth",
    value=None if defaults["CalculatedNetWorth"] is None else float(defaults["CalculatedNetWorth"]),
    placeholder="Enter applicant's net worth",
    help="Estimated net worth after considering the applicant's assets and liabilities."
    )

st.markdown("---")

# ============================================================
# EXISTING DEBT & FINANCIAL OBLIGATIONS
# ============================================================

st.header("💳 Existing Debt & Financial Obligations")

col1, col2 = st.columns(2)


with col1:

    monthly_debt = st.number_input(
        "Monthly Debt Payments",
        min_value=0.0,
        value=None if defaults["MonthlyDebtPayments"] is None else float(defaults["MonthlyDebtPayments"]),
        placeholder="Enter total monthly debt payments",
        help="Total monthly payments towards existing loans, EMIs and other debt obligations."
    )
    dti = st.number_input(
        "Debt-to-Income Ratio",
        min_value=0.0,
        max_value=1.0,
        value=None if defaults["DebtToIncomeRatio"] is None else float(defaults["DebtToIncomeRatio"]),
        placeholder="Example: 0.35",
        help="Ratio of Monthly Debt Payments to Monthly Income.Lower values indicate better repayment capacity"

    )

with col2:
    utilization_percent = st.number_input(
    "Credit Card Utilization Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=None if defaults["CreditCardUtilizationRate"] is None else float(defaults["CreditCardUtilizationRate"] * 100),
    step=1.0,
    placeholder="Example: 35",
    help="Percentage of the total available credit currently being used."
)

    # Convert percentage to decimal for the model
    utilization = utilization_percent / 100 if utilization_percent is not None else None
    

st.markdown("---")

# ============================================================
# CREDIT PROFILE
# ============================================================

st.header("📊 Credit Profile")

col1, col2 = st.columns(2)


with col1:

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900,
        value=None if defaults["CreditScore"] is None else int(defaults["CreditScore"]),
        placeholder="Enter credit score",
        help="Credit Score between 300 and 900."
    )
    credit_history = st.number_input(
        "Length of Credit History (Years)",
        min_value=0,
        value=None if defaults["LengthOfCreditHistory"] is None else int(defaults["LengthOfCreditHistory"]),
        placeholder="Enter years of credit history",
        help = 'Total number of years the applicant has maintained credit accounts.'
    )
with col2:

    open_credit = st.number_input(
        "Number of Open Credit Lines",
        min_value=0,
        value=None if defaults["NumberOfOpenCreditLines"] is None else int(defaults["NumberOfOpenCreditLines"]),
        placeholder="Enter open credit lines",
        help="Total number of currently active credit accounts such as credit cards or loans."
    )

    inquiries = st.number_input(
        "Number of Credit Inquiries",
        min_value=0,
        value=None if defaults["NumberOfCreditInquiries"] is None else int(defaults["NumberOfCreditInquiries"]),
        placeholder="Enter recent credit inquiries",
        help="Credit enquiries during the recent assessment period."
    )
st.markdown("---")   

   

# ============================================================
# CREDIT & FINANCIAL HISTORY
# ============================================================

st.header("📅 Credit & Financial History")

col1, col2 = st.columns(2)
# bankruptcy_options = ["No", "Yes"]
# default_options = ["No", "Yes"]
with col1:

    payment_history = st.number_input(
        "Payment History",
        min_value=0,
        value=None if defaults["PaymentHistory"] is None else int(defaults["PaymentHistory"]),
        placeholder="Enter payment history score",
        help="Internal payment history score between 0-100 from previous repayments."
    )

    utility = st.number_input(
        "Utility Bills Payment History",
        min_value=0,
        value=None if defaults["UtilityBillsPaymentHistory"] is None else int(defaults["UtilityBillsPaymentHistory"]),
        placeholder="Enter utility payment score",
        help="Score between 0-100 reflecting the applicant's consistency in paying utility bills such as electricity, water, or gas."
    )

with col2:
    bankruptcy_saved = defaults.get("BankruptcyHistory")

    if pd.notna(bankruptcy_saved):
        bankruptcy_index = int(bankruptcy_saved)
    else:
        bankruptcy_index = None

    bankruptcy = st.selectbox(
        "Bankruptcy History",
        [0, 1],
        index=bankruptcy_index,
        format_func=lambda x: "Yes" if x == 1 else "No",
        placeholder="Select Bankruptcy History",
        help="Indicates whether the applicant has ever declared bankruptcy."
    )

    previous_default_saved = defaults.get("PreviousLoanDefaults")

    if pd.notna(previous_default_saved):
        previous_default_index = int(previous_default_saved)
    else:
        previous_default_index = None

    previous_default = st.selectbox(
        "Previous Loan Defaults",
        [0, 1],
        index=previous_default_index,
        format_func=lambda x: "Yes" if x == 1 else "No",
        placeholder="Select Previous Loan Defaults",
        help="Indicates whether the applicant has defaulted on any previous loan."
    )   

    
    
st.markdown("---")
    

# ============================================================
# ACTION BUTTONS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    save_pending = st.button(
        "💾 Save as Pending",
        use_container_width=True
    )

with col2:

    predict = st.button(
        "Predict Risk Score",
        type="primary",
        use_container_width=True
    )

# ============================================================
# SAVE AS PENDING
# ============================================================

if save_pending:

    if st.session_state.action == "new":

        pending_df = pd.read_csv(PENDING_FILE)

        # Avoid duplicate Loan IDs
        if st.session_state.loan_id in pending_df["LoanID"].values:

            st.warning("This application already exists in Pending.")

        else:

            new_row = pd.DataFrame({

                "LoanID":[st.session_state.loan_id],
                "Status":["Pending"],

                "Age":[age],
                "CreditScore":[credit_score],
                "EmploymentStatus":[employment],
                "EducationLevel":[education],
                "Experience":[experience],

                "LoanAmount":[loan_amount],
                "LoanDuration":[loan_duration],

                "MaritalStatus":[marital],
                "NumberOfDependents":[dependents],

                "HomeOwnershipStatus":[home],

                "MonthlyDebtPayments":[monthly_debt],
                "CreditCardUtilizationRate":[utilization],

                "NumberOfOpenCreditLines":[open_credit],
                "NumberOfCreditInquiries":[inquiries],

                "DebtToIncomeRatio":[dti],

                "BankruptcyHistory":[
                    bankruptcy
                ],

                "LoanPurpose":[purpose],

                "PreviousLoanDefaults":[
                    previous_default
                ],

                "PaymentHistory":[payment_history],

                "LengthOfCreditHistory":[credit_history],

                "SavingsAccountBalance":[savings],

                "CheckingAccountBalance":[checking],

                "MonthlyIncome":[monthly_income],

                "UtilityBillsPaymentHistory":[utility],

                "JobTenure":[job_tenure],

                "CalculatedNetWorth":[networth]

            })

            pending_df = pd.concat(
                [pending_df,new_row],
                ignore_index=True
            )

            pending_df.to_csv(
                PENDING_FILE,
                index=False
            )

            st.success("Application saved successfully.")

    else:

        pending_df = pd.read_csv(PENDING_FILE)

        pending_df.loc[
            pending_df["LoanID"]==st.session_state.loan_id,
            pending_df.columns[2:]
        ]=[

            age,
            credit_score,
            employment,
            education,
            experience,

            loan_amount,
            loan_duration,

            marital,
            dependents,

            home,

            monthly_debt,
            utilization,

            open_credit,
            inquiries,

            dti,

            bankruptcy,

            purpose,

            previous_default,

            payment_history,

            credit_history,

            savings,

            checking,

            monthly_income,

            utility,

            job_tenure,

            networth

        ]

        pending_df.to_csv(
            PENDING_FILE,
            index=False
        )

        st.success("Pending application updated.")

    st.session_state.application_started=False
    st.session_state.form_open=False
    st.session_state.loan_id=None
    st.session_state.pending_app=None
    st.session_state.action=None

    st.rerun()

# ============================================================
# PREDICTION
# ============================================================

if predict:

    required_fields = {
    "Education": education,
    "Employment": employment,
    "Marital Status": marital,
    "Home Ownership": home,
    "Loan Purpose": purpose,
    "Bankruptcy History": bankruptcy,
    "Previous Loan Defaults": previous_default
    }

    missing = [
        name for name, value in required_fields.items()
        if value is None
    ]

    if missing:
        st.error(
            "Please complete the following fields:\n\n• " +
            "\n• ".join(missing)
        )
        st.stop()


    input_df=pd.DataFrame({

        "Age":[age],
        "CreditScore":[credit_score],
        "EmploymentStatus":[employment],
        "EducationLevel":[education],
        "Experience":[experience],

        "LoanAmount":[loan_amount],
        "LoanDuration":[loan_duration],

        "MaritalStatus":[marital],
        "NumberOfDependents":[dependents],

        "HomeOwnershipStatus":[home],

        "MonthlyDebtPayments":[monthly_debt],

        "CreditCardUtilizationRate":[utilization],

        "NumberOfOpenCreditLines":[open_credit],

        "NumberOfCreditInquiries":[inquiries],

        "DebtToIncomeRatio":[dti],

        "BankruptcyHistory":[
            bankruptcy
        ],

        "LoanPurpose":[purpose],

        "PreviousLoanDefaults":[
            previous_default
        ],

        "PaymentHistory":[payment_history],

        "LengthOfCreditHistory":[credit_history],

        "SavingsAccountBalance":[savings],

        "CheckingAccountBalance":[checking],

        "MonthlyIncome":[monthly_income],

        "UtilityBillsPaymentHistory":[utility],

        "JobTenure":[job_tenure],

        "CalculatedNetWorth":[networth]

    })

    prediction=model.predict(input_df)[0]

    st.markdown("---")

    st.subheader("Prediction Result")

    st.metric(
        "Predicted Risk Score",
        f"{prediction:.2f}"
    )

    st.progress(prediction/100)

    if prediction>=65:

        decision="Loan Not Recommended"
        risk = 'High Risk'

        st.error("🔴 High Risk Applicant")

    elif prediction>=35:

        decision="Manual Review Required"
        risk = 'Medium Risk'

        st.warning("🟡 Medium Risk Applicant")

    else:

        decision="Loan Can Be Considered"
        risk = 'Low Risk'

        st.success("🟢 Low Risk Applicant")


    st.info(decision)

    # ------------------------------------
    # Save to Completed.csv
    # ------------------------------------

    completed_record = input_df.copy()

    completed_record.insert(
        0,
        "LoanID",
        st.session_state.loan_id
    )

    completed_record["PredictedRiskScore"] = round(prediction,2)

    completed_record["RiskCategory"] = risk

    completed_record["ProcessedDate"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    completed_record["Employee"] = st.session_state.username


    if os.path.exists(COMPLETED_FILE):

        completed_df = pd.read_csv(COMPLETED_FILE)

    else:

        completed_df = pd.DataFrame()

    completed_df = pd.concat(
        [completed_df, completed_record],
        ignore_index=True
    )

    completed_df.to_csv(
        COMPLETED_FILE,
        index=False)

# ============================================================
# REMOVE COMPLETED APPLICATION
# ============================================================

    if st.session_state.action=="pending":

        pending_df=pd.read_csv(PENDING_FILE)

        pending_df=pending_df[
            pending_df["LoanID"]!=st.session_state.loan_id
        ]

        pending_df.to_csv(
            PENDING_FILE,
            index=False
        )

# ============================================================
# REPORT
# ============================================================

    summary=pd.DataFrame({

        "Field":[

            "Loan ID",
            "Risk Score",
            "Decision"

        ],

        "Value":[

            st.session_state.loan_id,

            round(prediction,2),

            decision

        ]

    })

    st.table(summary)

    csv=summary.to_csv(index=False)

    st.download_button(

        "Download Report",

        csv,

        file_name=f"{st.session_state.loan_id}.csv"

    )

# ============================================================
# RESET APPLICATION
# ============================================================

    st.session_state.application_started=False
    st.session_state.loan_id=None
    st.session_state.form_open=False
    st.session_state.pending_app=None
    st.session_state.action=None

    if st.button("🏠 Back to Dashboard"):

        st.rerun()



# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""

<center>

© 2026 ABC National Bank

Loan Risk Assessment System

Version 1.0

</center>

""",unsafe_allow_html=True)


