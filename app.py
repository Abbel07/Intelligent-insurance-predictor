import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import requests
from fpdf import FPDF
from datetime import datetime
import json
import base64
import os
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="Insurance Predict", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Function to load image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return None

# Load background image
img_base64 = get_base64_image("background.jpg")

if img_base64:
    st.markdown(f"""
    <style>
        /* Main app background image */
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* No white overlay */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0);
            z-index: 0;
        }}
        
        /* Target the main content area correctly */
        .stApp > .main {{
            background-color: transparent !important;
        }}
        
        /* Target the block container */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.65) !important;
            border-radius: 15px;
            padding: 2rem 1rem !important;
            margin: 1rem auto !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        /* All text white */
        h1, h2, h3, h4, p, .stMarkdown, label, .stTextInput label, .stNumberInput label, .stSelectbox label {{
            color: white !important;
        }}
        
        /* Slider values */
        .stSlider .stMarkdown {{
            color: white !important;
        }}
        
        /* Number input values */
        .stNumberInput input {{
            color: white !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* Slider thumb */
        .stSlider .stSlider .stThumb {{
            background-color: #57B9FF !important;
        }}
        
        /* Metric text */
        [data-testid="stMetric"] label, [data-testid="stMetric"] .stMarkdown {{
            color: white !important;
        }}
        
        /* Info/Success/Warning text */
        .stAlert {{
            background-color: rgba(0, 0, 0, 0.8) !important;
            color: white !important;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            position: relative;
            z-index: 2;
            background-color: #001f3f !important;
            min-width: 300px !important;
            width: 300px !important;
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdown"],
        [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stExpander,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] .stHeading {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] strong,
        [data-testid="stSidebar"] b {{
            color: #57B9FF !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox select {{
            background-color: #002b4f;
            color: white;
            border: 1px solid #4a6b8f;
        }}
        
        [data-testid="stSidebar"] .stSelectbox option {{
            background-color: #002b4f;
            color: white;
        }}
        
        [data-testid="stSidebar"] hr {{
            border-color: #4a6b8f;
        }}
        
        [data-testid="stSidebar"] .streamlit-expanderHeader {{
            color: white !important;
            background-color: #002b4f;
        }}
        
        [data-testid="stSidebar"] .stButton button {{
            background-color: #57B9FF;
            color: #001f3f;
            font-weight: bold;
        }}
        
        [data-testid="stSidebar"] .stButton button:hover {{
            background-color: #3a9ae0;
            color: white;
        }}
        
        /* Main content margin */
        .main {{
            margin-left: 300px !important;
        }}
        
        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        [data-testid="stToolbar"] {{display: none;}}
        
        [data-testid="stSidebarNav"] {{
            background-color: #001f3f;
        }}
        
        [data-testid="stSidebar"] * {{
            visibility: visible !important;
        }}
        
        /* Input fields */
        input, textarea, .stTextInput input, .stNumberInput input, .stPasswordInput input {{
            background-color: rgba(0, 0, 0, 0.7) !important;
            color: white !important;
            border: 1px solid #57B9FF !important;
            border-radius: 8px !important;
        }}
        
        /* Placeholder text */
        .stTextInput input::placeholder, .stPasswordInput input::placeholder {{
            color: rgba(255, 255, 255, 0.5) !important;
        }}
        
        /* Toggle */
        .stToggle label {{
            color: white !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none;
        }}
        
        .stButton button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
            transition: all 0.2s ease;
        }}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
            color: white !important;
        }}
        
        /* Fix for any remaining dark text */
        .stMarkdown, .stMarkdown p, .stText, div[data-testid="stMarkdownContainer"] p {{
            color: white !important;
        }}
    </style>
    """, unsafe_allow_html=True)

USER_DATA_FILE = "users.json"

EMAIL_ENABLED = True
EMAIL_ADDRESS = "abbelkipkirui@gmail.com"
EMAIL_PASSWORD = "pxtusnhnyytafecj"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_verification_code():
    return str(random.randint(100000, 999999))

def generate_reset_token():
    return hashlib.sha256(str(random.randint(1000000, 9999999)).encode()).hexdigest()[:8]

def send_verification_email(email, code):
    if not EMAIL_ENABLED:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Insurance Predictor - Verify Your Email"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #001f3f;">Welcome to Insurance Predictor!</h2>
                <p>Thank you for registering. Please verify your email address using the code below:</p>
                <p style="font-size: 32px; font-weight: bold; background-color: #f0f0f0; padding: 15px; text-align: center; letter-spacing: 5px;">
                    {code}
                </p>
                <p>Enter this code to complete your registration.</p>
                <p>This code expires in 10 minutes.</p>
                <hr>
                <small>Insurance Predictor - Secure Email Verification</small>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Verification email error details: {e}")
        return False

def send_password_reset_email(email, token):
    if not EMAIL_ENABLED:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Insurance Predictor - Password Reset Code"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #001f3f;">Password Reset Request</h2>
                <p>You requested to reset your password for Insurance Predictor.</p>
                <p style="font-size: 24px; font-weight: bold; background-color: #f0f0f0; padding: 10px; text-align: center; letter-spacing: 5px;">
                    {token}
                </p>
                <p>Enter this code to reset your password.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <hr>
                <small>Insurance Predictor - Secure Password Reset</small>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Password reset email error details: {e}")
        return False

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(c in special_chars for c in password):
        score += 1
    
    if score >= 5:
        strength = "Strong"
        progress = 100
    elif score >= 4:
        strength = "Good"
        progress = 75
    elif score >= 3:
        strength = "Fair"
        progress = 50
    elif score >= 2:
        strength = "Weak"
        progress = 25
    else:
        strength = "Very Weak"
        progress = 10
    
    return {"score": score, "strength": strength, "progress": progress}

def display_password_strength(password):
    if password:
        info = check_password_strength(password)
        st.progress(info['progress'] / 100)
        st.caption(f"Password Strength: {info['strength']} ({info['score']}/5 criteria met)")

def is_admin(email):
    if email == "Guest":
        return False
    users = load_users()
    if email in users:
        return users[email].get("role") == "admin"
    return False

def is_authenticated_user(email):
    return email != "Guest"

def can_make_predictions(email):
    return is_authenticated_user(email)

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "verification_code" not in st.session_state:
    st.session_state.verification_code = None
if "pending_verification_email" not in st.session_state:
    st.session_state.pending_verification_email = None
if "pending_verification_password" not in st.session_state:
    st.session_state.pending_verification_password = None
if "show_reset" not in st.session_state:
    st.session_state.show_reset = False
if "reset_email" not in st.session_state:
    st.session_state.reset_email = None
if "reset_token" not in st.session_state:
    st.session_state.reset_token = None
if "reset_verified" not in st.session_state:
    st.session_state.reset_verified = False
if "code_sent" not in st.session_state:
    st.session_state.code_sent = False
if "language" not in st.session_state:
    st.session_state.language = "English"
if "prediction_made" not in st.session_state:
    st.session_state.prediction_made = False
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "last_input_data" not in st.session_state:
    st.session_state.last_input_data = None
if "last_health_score" not in st.session_state:
    st.session_state.last_health_score = None
if "age" not in st.session_state:
    st.session_state.age = 30
if "bmi" not in st.session_state:
    st.session_state.bmi = 25.0
if "children" not in st.session_state:
    st.session_state.children = 0
if "bloodpressure" not in st.session_state:
    st.session_state.bloodpressure = 120
if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = "USD"
if "gender" not in st.session_state:
    st.session_state.gender = None
if "diabetic" not in st.session_state:
    st.session_state.diabetic = None
if "smoker" not in st.session_state:
    st.session_state.smoker = None
if "region" not in st.session_state:
    st.session_state.region = "southeast"

# Translations
translations = {
    "English": {
        "welcome": "Welcome:",
        "logout": "Logout",
        "about_app": "About This App",
        "model": "Model: Best Model",
        "features": "Features: Age, Body Mass Index (BMI), Blood Pressure (BP), Children, Gender, Diabetic, Smoker, Region",
        "understanding": "Understanding Your Quote",
        "tip1": "- Non-smokers pay 20-30% less",
        "tip2": "- Lower Body Mass Index (BMI) = lower premiums",
        "tip3": "- No diabetes reduces costs by 15-25%",
        "tip4": "- Normal Blood Pressure (BP) helps lower rates",
        "tip5": "- Older age = higher premiums",
        "title": "Health Insurance Prediction",
        "subtitle": "Enter your details to get an insurance estimate",
        "auth_subtitle": "Sign in to access your insurance estimates",
        "tab_prediction": "Prediction",
        "tab_analytics": "Analytics",
        "tab_help": "Help",
        "tab_admin": "Admin",
        "interactive_calc": "Interactive Calculator",
        "age": "Age",
        "bmi": "BMI",
        "smoker": "Smoker",
        "currency": "Currency",
        "region": "Region",
        "select_currency": "Select Currency",
        "real_time_estimate": "Real-time Estimate",
        "predict_button": "Predict Payment",
        "health_score": "Health Score",
        "payment_options": "Payment Options",
        "annual": "Annual",
        "monthly": "Monthly",
        "bi_weekly": "Bi-Weekly",
        "health_tips": "Health Tips",
        "tip_quit_smoking": "Quit smoking to save up to 30%",
        "tip_lose_weight": "Lose weight to save 15-20%",
        "tip_lower_bp": "Lower Blood Pressure (BP) to save up to 10%",
        "tip_manage_diabetes": "Manage diabetes to save 15-25%",
        "tip_great_job": "Great job! You're maintaining healthy habits!",
        "click_predict": "Click Predict Payment to see your estimate",
        "calculating": "Calculating...",
        "estimated_payment": "Estimated Payment",
        "premium_comparison": "Premium Comparison",
        "your_premium": "Your Premium",
        "national_avg": "National Avg",
        "your_age_group": "Your Age Group",
        "above_average": "Your premium is {pct:.1f}% above average for your age group",
        "below_average": "Your premium is {pct:.1f}% below average for your age group",
        "premium_projection": "Premium Projection",
        "provider_comparison": "Provider Comparison",
        "impact_analysis": "Impact Analysis",
        "download_report": "Download Report",
        "download_json": "Download as JSON",
        "download_csv": "Download as CSV",
        "generate_pdf": "Generate PDF Report",
        "prediction_first": "Make a prediction first to see analytics",
        "faq": "Frequently Asked Questions",
        "q1": "How accurate is this prediction?",
        "a1": "This prediction is based on machine learning models trained on real insurance data. Actual quotes may vary by 10-20% depending on the provider and location.",
        "q2": "What factors affect insurance premiums the most?",
        "a2": "The most significant factors are:",
        "factor1": "- Smoking status (20-30% impact)",
        "factor2": "- Age (10-25% impact)",
        "factor3": "- BMI (15-20% impact)",
        "factor4": "- Diabetes status (15-20% impact)",
        "factor5": "- Blood pressure (5-10% impact)",
        "q3": "Can I get insurance with pre-existing conditions?",
        "a3": "Yes, but premiums may be higher. Always disclose all health conditions for accurate quotes.",
        "q4": "How can I reduce my insurance premiums?",
        "a4": "Here are proven ways to lower premiums:",
        "reduce1": "- Quit smoking",
        "reduce2": "- Maintain a healthy BMI through diet and exercise",
        "reduce3": "- Manage chronic conditions like diabetes and hypertension",
        "reduce4": "- Compare quotes from multiple providers",
        "reduce5": "- Consider higher deductibles for lower monthly premiums",
        "q5": "How does the health score work?",
        "a5": "The health score is calculated based on:",
        "score1": "- Smoking status: 25 points deduction",
        "score2": "- Diabetes status: 20 points deduction",
        "score3": "- BMI above 25: 2 points per point above 25",
        "score4": "- Blood pressure above 120: 0.5 points per point above 120",
        "score5": "Higher scores indicate better health and potentially lower premiums.",
        "q6": "Is this app free to use?",
        "a6": "Yes! This is a free educational tool. For actual quotes, please consult licensed insurance professionals.",
        "sign_in": "Sign In",
        "create_account": "Create Account",
        "email": "Email",
        "password": "Password",
        "forgot_password": "Forgot Password",
        "continue_as_guest": "Continue as Guest",
        "confirm_password": "Confirm Password",
        "send_verification_code": "Send Verification Code",
        "verify_email": "Verify Email",
        "enter_6_digit_code": "Enter 6-digit code",
        "verify": "Verify",
        "resend_code": "Resend Code",
        "reset_password": "Reset Password",
        "send_reset_code": "Send Reset Code",
        "enter_reset_code": "Enter Reset Code",
        "verify_code": "Verify Code",
        "new_password": "New Password",
        "cancel": "Cancel",
        "children": "Children",
        "blood_pressure": "Blood Pressure",
        "gender": "Gender",
        "diabetic": "Diabetic",
        "login_required": "Please sign in to make predictions",
        "guest_restricted": "Guest accounts cannot make predictions. Please sign up for a free account.",
        "admin_only": "Admin Access Only",
        "total_users": "Total Users",
        "total_quotes": "Total Quotes",
        "regular_users": "Regular Users",
        "admins": "Admins",
        "all_users": "All Users",
        "role": "Role",
        "created": "Created",
        "quotes_saved": "Quotes Saved",
        "verified": "Verified",
        "delete_user": "Delete User",
        "select_user": "Select user to delete",
        "make_admin": "Make User Admin",
        "select_user_promote": "Select user to promote",
        "all_quotes": "All Quotes (All Users)",
        "clear_all_quotes": "Clear ALL Quotes from ALL Users",
        "access_denied": "Access Denied",
        "admin_warning": "This section is only available to system administrators.",
    },
    "Swahili": {
        "welcome": "Karibu:",
        "logout": "Toka",
        "about_app": "Kuhusu Programu Hii",
        "model": "Modeli: Best Model",
        "features": "Vipengele: Umri, BMI, Shinikizo la Damu, Watoto, Jinsia, Mgonjwa wa Kisukari, Mvutaji sigara, Eneo",
        "understanding": "Kuelewa Nukuu Yako",
        "tip1": "- WasioVuta sigara hulipa 20-30% kidogo",
        "tip2": "- BMI ya chini = malipo ya chini",
        "tip3": "- Kutokuwa na kisukari kunapunguza gharama kwa 15-25%",
        "tip4": "- Shinikizo la kawaida la damu husaidia kupunguza viwango",
        "tip5": "- Umri mkubwa = malipo makubwa",
        "title": "Utabiri wa Bima ya Afya",
        "subtitle": "Weka maelezo yako ili kupata makadirio ya bima",
        "auth_subtitle": "Ingia ili upate makadirio yako ya bima",
        "tab_prediction": "Utabiri",
        "tab_analytics": "Uchambuzi",
        "tab_help": "Usaidizi",
        "tab_admin": "Msimamizi",
        "interactive_calc": "Kikokotoo Maingiliano",
        "age": "Umri",
        "bmi": "BMI",
        "smoker": "Mvutaji Sigara",
        "currency": "Sarafu",
        "region": "Eneo",
        "select_currency": "Chagua Sarafu",
        "real_time_estimate": "Makadirio ya Wakati Halisi",
        "predict_button": "Tabiri Malipo",
        "health_score": "Alama ya Afya",
        "payment_options": "Chaguzi za Malipo",
        "annual": "Kila Mwaka",
        "monthly": "Kila Mwezi",
        "bi_weekly": "Kila Wiki Mbili",
        "health_tips": "Vidokezo vya Afya",
        "tip_quit_smoking": "Acha kuvuta sigara kuokoa hadi 30%",
        "tip_lose_weight": "Punguza uzito kuokoa 15-20%",
        "tip_lower_bp": "Punguza shinikizo la damu kuokoa hadi 10%",
        "tip_manage_diabetes": "Dhibiti kisukari kuokoa 15-25%",
        "tip_great_job": "Kazi nzuri! Unazingatia tabia za kiafya!",
        "click_predict": "Bonyeza Tabiri Malipo kuona makadirio yako",
        "calculating": "Inahesabu...",
        "estimated_payment": "Malipo Yaliyokadiriwa",
        "premium_comparison": "Ulinganisho wa Malipo",
        "your_premium": "Malipo Yako",
        "national_avg": "Wastani wa Taifa",
        "your_age_group": "Kikundi Chako cha Umri",
        "above_average": "Malipo yako ni {pct:.1f}% juu ya wastani kwa kikundi chako cha umri",
        "below_average": "Malipo yako ni {pct:.1f}% chini ya wastani kwa kikundi chako cha umri",
        "premium_projection": "Makadirio ya Malipo",
        "provider_comparison": "Ulinganisho wa Watoa Huduma",
        "impact_analysis": "Uchambuzi wa Athari",
        "download_report": "Pakua Ripoti",
        "download_json": "Pakua kama JSON",
        "download_csv": "Pakua kama CSV",
        "generate_pdf": "Tengeneza Ripoti ya PDF",
        "prediction_first": "Fanya utabiri kwanza ili kuona uchambuzi",
        "faq": "Maswali Yanayoulizwa Sana",
        "q1": "Utabiri huu ni sahihi kiasi gani?",
        "a1": "Utabiri huu unategemea modeli za kujifunza kwa mashine zilizofunzwa kwa data halisi ya bima. Nukuu halisi zinaweza kutofautiana kwa 10-20% kulingana na mtoa huduma na eneo.",
        "sign_in": "Ingia",
        "create_account": "Tengeneza Akaunti",
        "email": "Barua pepe",
        "password": "Nenosiri",
        "forgot_password": "Umesahau Nenosiri",
        "continue_as_guest": "Endelea kama Mgeni",
        "confirm_password": "Thibitisha Nenosiri",
        "send_verification_code": "Tuma Msimbo wa Uthibitishaji",
        "verify_email": "Thibitisha Barua Pepe",
        "enter_6_digit_code": "Weka msimbo wa tarakimu 6",
        "verify": "Thibitisha",
        "resend_code": "Tuma Msimbo Tena",
        "reset_password": "Weka Upya Nenosiri",
        "send_reset_code": "Tuma Msimbo wa Kuweka Upya",
        "enter_reset_code": "Weka Msimbo wa Kuweka Upya",
        "verify_code": "Thibitisha Msimbo",
        "new_password": "Nenosiri Jipya",
        "cancel": "Ghairi",
        "children": "Watoto",
        "blood_pressure": "Shinikizo la Damu",
        "gender": "Jinsia",
        "diabetic": "Mgonjwa wa Kisukari",
        "login_required": "Tafadhali ingia ili kufanya utabiri",
        "guest_restricted": "Wageni hawawezi kufanya utabiri. Tafadhali jisajili kwa akaunti ya bure.",
    }
}

def t(key, **kwargs):
    text = translations[st.session_state.language].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def show_auth_ui():
    # Minimal CSS for login page (gradient is already applied globally)
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h1 class="auth-title" style="color:#001f3f;text-align:center;">{t("title")}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="auth-subtitle" style="color:#57B9FF;text-align:center;">{t("auth_subtitle")}</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([t("sign_in"), t("create_account")])
        
        with tab1:
            email = st.text_input(t("email"), key="login_email")
            password = st.text_input(t("password"), type="password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(t("sign_in"), use_container_width=True):
                    users = load_users()
                    if email in users and users[email]["password"] == hash_password(password):
                        if users[email].get("verified", False):
                            st.session_state.authenticated = True
                            st.session_state.current_user = email
                            st.success(f"Welcome back, {email}!")
                            st.rerun()
                        else:
                            st.error("Please verify your email first.")
                    else:
                        st.error("Invalid email or password")
            
            with col2:
                if st.button(t("forgot_password"), use_container_width=True):
                    st.session_state.show_reset = True
                    st.rerun()
            
            if st.session_state.get("show_reset", False):
                st.markdown("---")
                st.subheader(t("reset_password"))
                
                if not st.session_state.reset_verified:
                    reset_email = st.text_input(t("email"), key="reset_email_input")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(t("send_reset_code"), use_container_width=True):
                            users = load_users()
                            if reset_email in users:
                                token = generate_reset_token()
                                st.session_state.reset_token = token
                                st.session_state.reset_email = reset_email
                                if send_password_reset_email(reset_email, token):
                                    st.success(f"Reset code sent to {reset_email}! Check your email.")
                                    st.session_state.code_sent = True
                                else:
                                    st.error("Failed to send email.")
                            else:
                                st.error("Email not found")
                    with col2:
                        if st.button(t("cancel"), use_container_width=True):
                            st.session_state.show_reset = False
                            st.rerun()
                    
                    if st.session_state.get("code_sent", False) or st.session_state.reset_token:
                        st.markdown("---")
                        st.subheader(t("enter_reset_code"))
                        st.info(f"A reset code was sent to {st.session_state.reset_email}")
                        
                        code = st.text_input(t("enter_reset_code"), key="reset_code")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(t("verify_code"), use_container_width=True):
                                if code and code == st.session_state.reset_token:
                                    st.session_state.reset_verified = True
                                    st.success("Code verified!")
                                    st.rerun()
                                else:
                                    st.error("Invalid code.")
                        with col2:
                            if st.button(t("resend_code"), use_container_width=True):
                                new_token = generate_reset_token()
                                st.session_state.reset_token = new_token
                                send_password_reset_email(st.session_state.reset_email, new_token)
                                st.success("New code sent!")
                
                elif st.session_state.reset_verified:
                    st.success(f"Verified: {st.session_state.reset_email}")
                    new_pass = st.text_input(t("new_password"), type="password", key="reset_new")
                    confirm = st.text_input(t("confirm_password"), type="password", key="reset_confirm")
                    
                    if new_pass:
                        display_password_strength(new_pass)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(t("reset_password"), use_container_width=True):
                            if not new_pass:
                                st.error("Enter new password")
                            elif new_pass != confirm:
                                st.error("Passwords do not match")
                            elif check_password_strength(new_pass)['score'] < 3:
                                st.error("Password too weak")
                            else:
                                users = load_users()
                                users[st.session_state.reset_email]["password"] = hash_password(new_pass)
                                save_users(users)
                                st.success("Password reset successful!")
                                st.session_state.show_reset = False
                                st.session_state.reset_verified = False
                                st.rerun()
                    with col2:
                        if st.button(t("cancel"), use_container_width=True):
                            st.session_state.show_reset = False
                            st.rerun()
        
        with tab2:
            new_email = st.text_input(t("email"), key="reg_email")
            new_pass = st.text_input(t("password"), type="password", key="reg_password")
            confirm = st.text_input(t("confirm_password"), type="password", key="reg_confirm")
            
            if new_pass:
                display_password_strength(new_pass)
            
            st.info("A verification code will be sent to your email.")
            
            if st.button(t("send_verification_code"), use_container_width=True):
                if not new_email or not new_pass:
                    st.error("Fill all fields")
                elif new_pass != confirm:
                    st.error("Passwords do not match")
                elif check_password_strength(new_pass)['score'] < 3:
                    st.error("Password too weak")
                else:
                    users = load_users()
                    if new_email in users:
                        st.error("Email already registered")
                    else:
                        code = generate_verification_code()
                        st.session_state.verification_code = code
                        st.session_state.pending_verification_email = new_email
                        st.session_state.pending_verification_password = hash_password(new_pass)
                        
                        if send_verification_email(new_email, code):
                            st.success(f"Verification code sent to {new_email}!")
                        else:
                            st.error("Failed to send email.")
            
            if st.session_state.pending_verification_email:
                st.markdown("---")
                st.subheader(t("verify_email"))
                st.info(f"A verification code was sent to {st.session_state.pending_verification_email}")
                entered = st.text_input(t("enter_6_digit_code"), max_chars=6, key="verify_code")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(t("verify"), use_container_width=True):
                        if entered == st.session_state.verification_code:
                            users = load_users()
                            users[st.session_state.pending_verification_email] = {
                                "password": st.session_state.pending_verification_password,
                                "verified": True,
                                "role": "user",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            }
                            save_users(users)
                            st.success("Email verified! You can now sign in.")
                            st.session_state.verification_code = None
                            st.session_state.pending_verification_email = None
                            st.rerun()
                        else:
                            st.error("Invalid code")
                with col2:
                    if st.button(t("resend_code"), use_container_width=True):
                        new_code = generate_verification_code()
                        st.session_state.verification_code = new_code
                        send_verification_email(st.session_state.pending_verification_email, new_code)
                        st.success("New code sent!")
        
        if st.button(t("continue_as_guest"), use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.current_user = "Guest"
            st.rerun()
    
    st.stop()

if not st.session_state.authenticated:
    show_auth_ui()

try:
    scaler = joblib.load("scaler.pkl")
    le_diabetic = joblib.load("label_encoder_diabetic.pkl")
    le_gender = joblib.load("label_encoder_gender.pkl")
    le_region = joblib.load("label_encoder_region.pkl")
    le_smoker = joblib.load("label_encoder_smoker.pkl")
    model = joblib.load("best_model.pkl")
    
    smoker_positive = le_smoker.classes_[1] if len(le_smoker.classes_) > 1 else None
    diabetic_positive = le_diabetic.classes_[1] if len(le_diabetic.classes_) > 1 else None

    if st.session_state.gender is None:
        st.session_state.gender = le_gender.classes_[0]
    if st.session_state.diabetic is None:
        st.session_state.diabetic = le_diabetic.classes_[0]
    if st.session_state.smoker is None:
        st.session_state.smoker = le_smoker.classes_[0]
    
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

users = load_users()

@st.cache_data(ttl=3600)
def get_exchange_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        if response.status_code == 200:
            return response.json().get("rates", {})
    except:
        pass
    return {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 148.5, "KES": 130.0, "TZS": 2500.0}

currency_options = {
    "USD": "USD",
    "EUR": "EUR",
    "GBP": "GBP",
    "JPY": "JPY",
    "KES": "KES",
    "TZS": "TZS"
}

with st.sidebar:
    if st.session_state.current_user != "Guest":
        st.write(f"{t('welcome')} {st.session_state.current_user}")
        if is_admin(st.session_state.current_user):
            st.markdown(" **Admin**")
    else:
        st.write(f"{t('welcome')} Guest")
    
    if st.button(t('logout'), use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()
    
    st.markdown("---")
    
    selected_language = st.selectbox(
        "Language", 
        ["English", "Swahili"],
        index=["English", "Swahili"].index(st.session_state.language)
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"### {t('about_app')}")
    st.write(t('model'))
    st.write(t('features'))
    
    st.markdown("---")
    st.markdown(f"### {t('understanding')}")
    st.write(t('tip1'))
    st.write(t('tip2'))
    st.write(t('tip3'))
    st.write(t('tip4'))
    st.write(t('tip5'))

st.title(t('title'))

if is_admin(st.session_state.current_user):
    tab1, tab2, tab3, tab4 = st.tabs([
        t('tab_prediction'), 
        t('tab_analytics'), 
        t('tab_help'),
        t('tab_admin')
    ])
else:
    tab1, tab2, tab3 = st.tabs([
        t('tab_prediction'), 
        t('tab_analytics'), 
        t('tab_help')
    ])

# ==================== TAB 1: PREDICTION ====================
with tab1:
    user_email = st.session_state.current_user
    
    if can_make_predictions(user_email):
        st.write(t('subtitle'))
        st.markdown("---")
        
        st.subheader(t('interactive_calc'))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.age = st.slider(t('age'), 0, 100, st.session_state.age)
        with col2:
            st.session_state.bmi = st.slider(t('bmi'), 15.0, 50.0, st.session_state.bmi, 0.1)
        with col3:
            smoker_val = st.toggle(t('smoker'), value=(st.session_state.smoker == smoker_positive))
            st.session_state.smoker = smoker_positive if smoker_val else le_smoker.classes_[0]
        
        st.markdown("---")
        st.subheader(t('currency'))
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.session_state.selected_currency = st.selectbox(
                t('select_currency'),
                options=list(currency_options.keys()),
                format_func=lambda x: currency_options[x]
            )
        
        exchange_rates = get_exchange_rates()
        
        temp_input = pd.DataFrame({
            "age": [st.session_state.age],
            "gender": [st.session_state.get("gender", le_gender.classes_[0])],
            "bmi": [st.session_state.bmi],
            "bloodpressure": [st.session_state.bloodpressure],
            "diabetic": [st.session_state.get("diabetic", le_diabetic.classes_[0])],
            "children": [st.session_state.children],
            "smoker": [st.session_state.get("smoker", le_smoker.classes_[0])],
            "region": [st.session_state.get("region", "southeast")]
        })
        temp_input["gender"] = le_gender.transform(temp_input["gender"])
        temp_input["diabetic"] = le_diabetic.transform(temp_input["diabetic"])
        temp_input["smoker"] = le_smoker.transform(temp_input["smoker"])
        
        region_encoded_temp = le_region.transform([st.session_state.get("region", "southeast")])[0]
        temp_input["region"] = region_encoded_temp
        
        num_cols = ["age", "bmi", "bloodpressure", "children"]
        temp_input[num_cols] = scaler.transform(temp_input[num_cols])
        
        real_time = model.predict(temp_input)[0]
        rate = exchange_rates.get(st.session_state.selected_currency, 1.0)
        st.info(f"{t('real_time_estimate')}: {st.session_state.selected_currency} {real_time * rate:,.2f} (USD {real_time:,.2f})")
        
        st.markdown("---")
        
        with st.form("input_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input(t('age'), 0, 100, st.session_state.age)
                bmi = st.number_input(t('bmi'), 10.0, 60.0, st.session_state.bmi, 0.1)
                children = st.number_input(t('children'), 0, None, st.session_state.children)
            with col2:
                bp = st.number_input(t('blood_pressure'), 60, 200, st.session_state.bloodpressure)
                gender = st.selectbox(t('gender'), le_gender.classes_, index=list(le_gender.classes_).index(st.session_state.gender))
                diabetic = st.selectbox(t('diabetic'), le_diabetic.classes_, index=list(le_diabetic.classes_).index(st.session_state.diabetic))
                smoker = st.selectbox(t('smoker'), le_smoker.classes_, index=list(le_smoker.classes_).index(st.session_state.smoker))
                region = st.selectbox(t('region'), list(le_region.classes_))
            
            submitted = st.form_submit_button(t('predict_button'), use_container_width=True)
            
            if submitted:
                st.session_state.age = age
                st.session_state.bmi = bmi
                st.session_state.children = children
                st.session_state.bloodpressure = bp
                st.session_state.gender = gender
                st.session_state.diabetic = diabetic
                st.session_state.smoker = smoker
                st.session_state.region = region
        
        if submitted:
            region_encoded = le_region.transform([region])[0]
            
            input_data = pd.DataFrame({
                "age": [age],
                "gender": [gender],
                "bmi": [bmi],
                "bloodpressure": [bp],
                "diabetic": [diabetic],
                "children": [children],
                "smoker": [smoker],
                "region": [region_encoded]
            })
            input_data["gender"] = le_gender.transform(input_data["gender"])
            input_data["diabetic"] = le_diabetic.transform(input_data["diabetic"])
            input_data["smoker"] = le_smoker.transform(input_data["smoker"])
            input_data[num_cols] = scaler.transform(input_data[num_cols])
            
            with st.spinner(t('calculating')):
                prediction = model.predict(input_data)[0]
            
            st.session_state.prediction_made = True
            st.session_state.last_prediction = float(prediction)
            st.session_state.last_input_data = {
                "age": age, "bmi": bmi, "children": children, "bloodpressure": bp,
                "gender": gender, "diabetic": diabetic, "smoker": smoker, "region": region
            }
            
            health_score = 100
            health_score -= (smoker == smoker_positive) * 25
            health_score -= (diabetic == diabetic_positive) * 20
            health_score -= max(0, (bmi - 25)) * 2
            health_score -= max(0, (bp - 120)) * 0.5
            health_score = max(0, min(100, health_score))
            st.session_state.last_health_score = float(health_score)
            
            converted = prediction * rate
            st.success(f"{t('estimated_payment')}: {st.session_state.selected_currency} {converted:,.2f} (USD {prediction:,.2f})")
            
            st.markdown("---")
            st.subheader(f"{t('health_score')}: {health_score:.0f}/100")
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                title={"text": t('health_score'), "font": {"size": 24, "color": "white"}},
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "white", "tickwidth": 2},
                    "bar": {"color": "#57B9FF"},
                    "bgcolor": "rgba(0,0,0,0.3)",
                    "borderwidth": 2,
                    "bordercolor": "#57B9FF",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255, 80, 80, 0.4)"},
                        {"range": [50, 75], "color": "rgba(255, 200, 80, 0.4)"},
                        {"range": [75, 100], "color": "rgba(80, 255, 80, 0.4)"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader(t('payment_options'))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t('annual'), f"{st.session_state.selected_currency} {prediction * rate:,.2f}")
            with col2:
                st.metric(t('monthly'), f"{st.session_state.selected_currency} {prediction * rate / 12:,.2f}")
            with col3:
                st.metric(t('bi_weekly'), f"{st.session_state.selected_currency} {prediction * rate / 26:,.2f}")
            
            st.markdown("---")
            st.subheader(t('health_tips'))
            
            tips = []
            if smoker == smoker_positive:
                tips.append(t('tip_quit_smoking'))
            if bmi > 30:
                tips.append(t('tip_lose_weight'))
            if bp > 140:
                tips.append(t('tip_lower_bp'))
            if diabetic == diabetic_positive:
                tips.append(t('tip_manage_diabetes'))
            
            if tips:
                for tip in tips:
                    st.write(f"- {tip}")
            else:
                st.write(t('tip_great_job'))
        else:
            st.info(t('click_predict'))
    else:
        st.warning(t('guest_restricted'))
        st.info(t('login_required'))
        
        if st.button("Sign In / Create Account", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# ==================== TAB 2: ANALYTICS ====================
with tab2:
    if st.session_state.prediction_made:
        pred = st.session_state.last_prediction
        data = st.session_state.last_input_data
        health = st.session_state.last_health_score
        
        age = data["age"]
        bmi = data["bmi"]
        bp = data["bloodpressure"]
        smoker = data["smoker"]
        diabetic = data["diabetic"]
        region = data.get("region", "southeast")

        region_encoded = le_region.transform([region])[0]
        
        rate = exchange_rates.get(st.session_state.selected_currency, 1.0)
        
        st.subheader(t('premium_comparison'))
        
        avg_by_age = {"18-30": 5000, "31-45": 8000, "46-60": 12000, "60+": 18000}
        age_group = "18-30" if age <= 30 else "31-45" if age <= 45 else "46-60" if age <= 60 else "60+"
        avg = avg_by_age[age_group]
        
        pct = ((pred - avg) / avg) * 100
        if pct > 0:
            st.warning(f" {t('above_average', pct=pct)}")
        else:
            st.success(f" {t('below_average', pct=abs(pct))}")
        
        compare_data = {
            "Category": [t('your_premium'), t('national_avg'), t('your_age_group')],
            "Amount": [pred, 12000, avg]
        }
        df = pd.DataFrame(compare_data)
        
        fig = px.bar(df, x="Category", y="Amount", 
                     title=f"{t('premium_comparison')} - {t('your_premium')}: {st.session_state.selected_currency} {pred * rate:,.0f}",
                     labels={"Category": "", "Amount": f"Premium ({st.session_state.selected_currency})"},
                     color="Category",
                     color_discrete_map={
                         t('your_premium'): '#2E86AB',
                         t('national_avg'): '#A23B72', 
                         t('your_age_group'): '#F18F01'
                     })
        
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        
        fig.add_hline(y=pred, line_dash="dash", line_color="red", 
                      annotation_text=f"Your Premium: {st.session_state.selected_currency} {pred * rate:,.0f}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            difference = pred - avg
            if difference > 0:
                st.metric("vs Your Age Group", f"+{st.session_state.selected_currency} {difference * rate:,.0f}", delta=f"+{pct:.1f}%", delta_color="inverse")
            else:
                st.metric("vs Your Age Group", f"{st.session_state.selected_currency} {difference * rate:,.0f}", delta=f"{pct:.1f}%", delta_color="normal")
            with st.expander(" What does this mean?"):
                st.write(f"Compared to others your age ({age_group}), you pay {st.session_state.selected_currency} {abs(difference * rate):,.0f} {'more' if difference > 0 else 'less'}.")
        
        with col2:
            national_diff = pred - 12000
            if national_diff > 0:
                st.metric("vs National Average", f"+{st.session_state.selected_currency} {national_diff * rate:,.0f}", delta="Above Average", delta_color="inverse")
            else:
                st.metric("vs National Average", f"{st.session_state.selected_currency} {national_diff * rate:,.0f}", delta="Below Average", delta_color="normal")
            with st.expander(" What does this mean?"):
                st.write(f"The national average premium is {st.session_state.selected_currency} {12000 * rate:,.0f}. You pay {st.session_state.selected_currency} {abs(national_diff * rate):,.0f} {'more' if national_diff > 0 else 'less'}.")
        
        with col3:
            if pct > 0:
                st.warning(f"**Potential Savings:** {st.session_state.selected_currency} {(pred - avg) * rate:,.0f}")
            else:
                st.success(f"**You're Saving:** {st.session_state.selected_currency} {(avg - pred) * rate:,.0f}")
            with st.expander(" How to save more?"):
                if pct > 0:
                    st.write("To lower your premium:")
                    if smoker == smoker_positive:
                        st.write("- Quit smoking")
                    if bmi > 25:
                        st.write("- Reduce your BMI")
                    if bp > 120:
                        st.write("- Lower your blood pressure")
                    if diabetic == diabetic_positive:
                        st.write("- Better manage your diabetes")
                else:
                    st.write("Great job! You're already paying less than average. Keep maintaining your healthy habits!")
        
        st.markdown("---")
        st.caption("""
        **Reading the Premium Comparison chart.**
        
        - **Blue bar (Your Premium)** : Your estimated annual premium based on your health profile
        - **Purple bar (National Avg)** : The average premium across all age groups nationally ($12,000)
        - **Orange bar (Your Age Group)** : The average premium for people in your age range
        
        **What the comparisons indicates:**
        
        | Comparison | What it means |
        |------------|---------------|
        | Your Premium vs National Avg | How you compare to everyone regardless of age |
        | Your Premium vs Your Age Group | How you compare to people similar in age to you |
        
        **Why this matters:**
        - If you pay less than your age group average → You have good health habits
        - If you pay more than your age group average → Specific factors (smoking, BMI, etc.) are increasing your premium
        - The age group average is the most fair comparison since age is a major factor in insurance pricing
        """)
        
        st.markdown("---")
        st.subheader(t('premium_projection'))
        
        ages = list(range(age, min(age + 20, 81)))
        proj = []
        for a in ages:
            temp = pd.DataFrame({
                "age": [a], 
                "gender": [data["gender"]], 
                "bmi": [bmi],
                "bloodpressure": [bp], 
                "diabetic": [diabetic],
                "children": [data["children"]], 
                "smoker": [smoker],
                "region": [region_encoded]
            })
            temp["gender"] = le_gender.transform(temp["gender"])
            temp["diabetic"] = le_diabetic.transform(temp["diabetic"])
            temp["smoker"] = le_smoker.transform(temp["smoker"])
            temp[num_cols] = scaler.transform(temp[num_cols])
            proj.append(model.predict(temp)[0])
        
        fig = px.line(x=ages, y=proj, 
                      title=f"{t('premium_projection')} - Next {len(ages)} Years",
                      labels={"x": t('age'), "y": f"Premium ({st.session_state.selected_currency})"},
                      markers=True)
        
        fig.add_hline(y=pred, line_dash="dash", line_color="red", 
                      annotation_text=f"Current: {st.session_state.selected_currency} {pred * rate:,.0f}")
        
        fig.add_vrect(x0=30, x1=45, fillcolor="green", opacity=0.05, 
                      annotation_text="Young Adult", annotation_position="top left")
        fig.add_vrect(x0=45, x1=60, fillcolor="yellow", opacity=0.1, 
                      annotation_text="Middle Age", annotation_position="top left")
        fig.add_vrect(x0=60, x1=80, fillcolor="red", opacity=0.1, 
                      annotation_text="Senior", annotation_position="top left")
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Current Age:** {age}")
            with st.expander("What does this show?"):
                st.write("This is your current age based on the prediction you made.")
        
        with col2:
            premium_change = ((proj[-1] - proj[0]) / proj[0]) * 100 if len(proj) > 1 else 0
            if premium_change > 0:
                st.warning(f"**Expected Increase:** +{premium_change:.1f}% over {len(ages)} years")
            else:
                st.success(f"**Expected Change:** {premium_change:.1f}% over {len(ages)} years")
            with st.expander("What does this mean?"):
                st.write(f"Your premium is projected to {'increase' if premium_change > 0 else 'decrease'} by {abs(premium_change):.1f}% as you age.")
        
        with col3:
            avg_premium = sum(proj) / len(proj)
            st.metric("Average Premium", f"{st.session_state.selected_currency} {avg_premium * rate:,.0f}")
            with st.expander("About this average"):
                st.write(f"This is the average premium you can expect over the next {len(ages)} years.")
        
        st.markdown("---")
        st.caption("""
        **How to read the Premium Projection chart:**
        
        - **X-axis (bottom)**: Your age in years
        - **Y-axis (left)**: Estimated annual insurance premium in your selected currency
        - **Blue line**: Shows how your premium changes as you get older
        - **Red dashed line**: Your current premium for reference
        - **Green/Yellow/Red background**: Different life stages (Young Adult, Middle Age, Senior)
        
        **Why do premiums increase with age?**
        - Older age is associated with higher health risks
        - Insurance companies charge more to cover potential medical costs
        - The rate of increase typically accelerates after age 50-60
        
        **Note:** This projection assumes all your other health factors (BMI, smoking status, etc.) remain the same.
        """)
        
        st.markdown("---")
        st.subheader(t('provider_comparison'))
        
        providers = {
            "Provider A": pred * 0.95,
            "Provider B": pred,
            "Provider C": pred * 1.08,
            "Provider D": pred * 1.15
        }
        for name, amount in providers.items():
            st.write(f"{name}: {st.session_state.selected_currency} {amount * rate:,.2f} (USD {amount:,.2f})")
        
        st.markdown("---")
        st.subheader(t('impact_analysis'))
        
        impacts = []
        
        baseline_data = pd.DataFrame({
            "age": [age],
            "gender": [data["gender"]],
            "bmi": [bmi],
            "bloodpressure": [bp],
            "diabetic": [diabetic],
            "children": [data["children"]],
            "smoker": [smoker],
            "region": [region_encoded]
        })
        baseline_data["gender"] = le_gender.transform(baseline_data["gender"])
        baseline_data["diabetic"] = le_diabetic.transform(baseline_data["diabetic"])
        baseline_data["smoker"] = le_smoker.transform(baseline_data["smoker"])
        baseline_data[num_cols] = scaler.transform(baseline_data[num_cols])
        baseline_pred = model.predict(baseline_data)[0]

        age_data = pd.DataFrame({
            "age": [30],
            "gender": [data["gender"]],
            "bmi": [bmi],
            "bloodpressure": [bp],
            "diabetic": [diabetic],
            "children": [data["children"]],
            "smoker": [smoker],
            "region": [region_encoded]
        })
        age_data["gender"] = le_gender.transform(age_data["gender"])
        age_data["diabetic"] = le_diabetic.transform(age_data["diabetic"])
        age_data["smoker"] = le_smoker.transform(age_data["smoker"])
        age_data[num_cols] = scaler.transform(age_data[num_cols])
        age_pred = model.predict(age_data)[0]
        age_impact = ((baseline_pred - age_pred) / baseline_pred) * 100
        impacts.append(("Age", age_impact))
        
        bmi_data = pd.DataFrame({
            "age": [age],
            "gender": [data["gender"]],
            "bmi": [22],
            "bloodpressure": [bp],
            "diabetic": [diabetic],
            "children": [data["children"]],
            "smoker": [smoker],
            "region": [region_encoded]
        })
        bmi_data["gender"] = le_gender.transform(bmi_data["gender"])
        bmi_data["diabetic"] = le_diabetic.transform(bmi_data["diabetic"])
        bmi_data["smoker"] = le_smoker.transform(bmi_data["smoker"])
        bmi_data[num_cols] = scaler.transform(bmi_data[num_cols])
        bmi_pred = model.predict(bmi_data)[0]
        bmi_impact = ((baseline_pred - bmi_pred) / baseline_pred) * 100
        impacts.append(("BMI", bmi_impact))
        
        bp_data = pd.DataFrame({
            "age": [age],
            "gender": [data["gender"]],
            "bmi": [bmi],
            "bloodpressure": [110],
            "diabetic": [diabetic],
            "children": [data["children"]],
            "smoker": [smoker],
            "region": [region_encoded]
        })
        bp_data["gender"] = le_gender.transform(bp_data["gender"])
        bp_data["diabetic"] = le_diabetic.transform(bp_data["diabetic"])
        bp_data["smoker"] = le_smoker.transform(bp_data["smoker"])
        bp_data[num_cols] = scaler.transform(bp_data[num_cols])
        bp_pred = model.predict(bp_data)[0]
        bp_impact = ((baseline_pred - bp_pred) / baseline_pred) * 100
        impacts.append(("Blood Pressure", bp_impact))

        if smoker == smoker_positive:
            nonsmoker_data = pd.DataFrame({
                "age": [age],
                "gender": [data["gender"]],
                "bmi": [bmi],
                "bloodpressure": [bp],
                "diabetic": [diabetic],
                "children": [data["children"]],
                "smoker": [le_smoker.classes_[0]],
                "region": [region_encoded]
            })
            nonsmoker_data["gender"] = le_gender.transform(nonsmoker_data["gender"])
            nonsmoker_data["diabetic"] = le_diabetic.transform(nonsmoker_data["diabetic"])
            nonsmoker_data["smoker"] = le_smoker.transform(nonsmoker_data["smoker"])
            nonsmoker_data[num_cols] = scaler.transform(nonsmoker_data[num_cols])
            nonsmoker_pred = model.predict(nonsmoker_data)[0]
            smoke_impact = ((baseline_pred - nonsmoker_pred) / baseline_pred) * 100
        else:
            smoker_data = pd.DataFrame({
                "age": [age],
                "gender": [data["gender"]],
                "bmi": [bmi],
                "bloodpressure": [bp],
                "diabetic": [diabetic],
                "children": [data["children"]],
                "smoker": [smoker_positive],
                "region": [region_encoded]
            })
            smoker_data["gender"] = le_gender.transform(smoker_data["gender"])
            smoker_data["diabetic"] = le_diabetic.transform(smoker_data["diabetic"])
            smoker_data["smoker"] = le_smoker.transform(smoker_data["smoker"])
            smoker_data[num_cols] = scaler.transform(smoker_data[num_cols])
            smoker_pred = model.predict(smoker_data)[0]
            smoke_impact = ((baseline_pred - smoker_pred) / baseline_pred) * 100
        impacts.append(("Smoking", smoke_impact))

        if diabetic == diabetic_positive:
            nondiabetic_data = pd.DataFrame({
                "age": [age],
                "gender": [data["gender"]],
                "bmi": [bmi],
                "bloodpressure": [bp],
                "diabetic": [le_diabetic.classes_[0]],
                "children": [data["children"]],
                "smoker": [smoker],
                "region": [region_encoded]
            })
            nondiabetic_data["gender"] = le_gender.transform(nondiabetic_data["gender"])
            nondiabetic_data["diabetic"] = le_diabetic.transform(nondiabetic_data["diabetic"])
            nondiabetic_data["smoker"] = le_smoker.transform(nondiabetic_data["smoker"])
            nondiabetic_data[num_cols] = scaler.transform(nondiabetic_data[num_cols])
            nondiabetic_pred = model.predict(nondiabetic_data)[0]
            diabetic_impact = ((baseline_pred - nondiabetic_pred) / baseline_pred) * 100
        else:
            diabetic_data = pd.DataFrame({
                "age": [age],
                "gender": [data["gender"]],
                "bmi": [bmi],
                "bloodpressure": [bp],
                "diabetic": [diabetic_positive],
                "children": [data["children"]],
                "smoker": [smoker],
                "region": [region_encoded]
            })
            diabetic_data["gender"] = le_gender.transform(diabetic_data["gender"])
            diabetic_data["diabetic"] = le_diabetic.transform(diabetic_data["diabetic"])
            diabetic_data["smoker"] = le_smoker.transform(diabetic_data["smoker"])
            diabetic_data[num_cols] = scaler.transform(diabetic_data[num_cols])
            diabetic_pred = model.predict(diabetic_data)[0]
            diabetic_impact = ((baseline_pred - diabetic_pred) / baseline_pred) * 100
        impacts.append(("Diabetes", diabetic_impact))
        
        impact_df = pd.DataFrame(impacts, columns=["Factor", "Impact (%)"])
        
        fig = px.bar(impact_df, x="Factor", y="Impact (%)",
                     title=t('impact_analysis'),
                     labels={"Factor": "Factor", "Impact (%)": "Impact (%)"},
                     color="Impact (%)",
                     color_continuous_scale=["red", "yellow", "green"])
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("""
        **How to read this chart:**
        - **Positive bars (green)** = Your current health factor is BETTER than average, lowering your premium
        - **Negative bars (red)** = Your current health factor is WORSE than average, raising your premium
        - **Example:** A -15% for Smoking means being a smoker increases your premium by 15%
        """)
        
        st.markdown("---")
        st.subheader(t('download_report'))
        
        if st.button(t('download_json'), use_container_width=True):
            if st.session_state.prediction_made:
                report_data = {
                    "date": datetime.now().isoformat(),
                    "premium": float(pred),
                    "user_data": data,
                    "health_score": float(health)
                }
                json_str = json.dumps(report_data, indent=2)
                st.download_button(
                    label=t('download_json'),
                    data=json_str,
                    file_name=f"insurance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        if st.button(t('download_csv'), use_container_width=True):
            if st.session_state.prediction_made:
                csv_data = pd.DataFrame([{
                    'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Premium (USD)': float(pred),
                    'Age': data.get('age'),
                    'BMI': data.get('bmi'),
                    'Blood Pressure': data.get('bloodpressure'),
                    'Children': data.get('children'),
                    'Gender': data.get('gender'),
                    'Diabetic': data.get('diabetic'),
                    'Smoker': data.get('smoker'),
                    'Region': data.get('region'),
                    'Health Score': float(health)
                }])
                st.download_button(
                    label=t('download_csv'),
                    data=csv_data.to_csv(index=False),
                    file_name=f"insurance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        def create_pdf_report():
            premium_value = float(pred) if pred else 0
            health_score_value = float(health) if health else 0
            
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Insurance Quote Report", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.ln(5)
            
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt=f"Estimated Premium: ${premium_value:,.2f} USD", ln=1)
            pdf.ln(10)
            
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="User Details:", ln=1)
            pdf.set_font("Arial", "", 12)
            
            for key, value in data.items():
                pdf.cell(200, 10, txt=f"  {key.capitalize()}: {value}", ln=1)
            
            pdf.ln(5)
            pdf.cell(200, 10, txt=f"Health Score: {health_score_value:.0f}/100", ln=1)
            
            return pdf.output(dest='S')
        
        if st.button(t('generate_pdf'), use_container_width=True):
            if st.session_state.prediction_made:
                try:
                    pdf_data = create_pdf_report()
                    if isinstance(pdf_data, str):
                        pdf_bytes = pdf_data.encode('latin-1')
                    else:
                        pdf_bytes = bytes(pdf_data)
                    
                    st.download_button(
                        label=t('generate_pdf'),
                        data=pdf_bytes,
                        file_name=f"insurance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"PDF Error: {e}")
    else:
        st.info(t('prediction_first'))

# ==================== TAB 3: HELP ====================
with tab3:
    st.subheader(t('faq'))
    
    with st.expander(t('q1')):
        st.write(t('a1'))
    
    with st.expander(t('q2')):
        st.write(t('a2'))
        st.write(t('factor1'))
        st.write(t('factor2'))
        st.write(t('factor3'))
        st.write(t('factor4'))
        st.write(t('factor5'))
    
    with st.expander(t('q3')):
        st.write(t('a3'))
    
    with st.expander(t('q4')):
        st.write(t('a4'))
        st.write(t('reduce1'))
        st.write(t('reduce2'))
        st.write(t('reduce3'))
        st.write(t('reduce4'))
        st.write(t('reduce5'))
    
    with st.expander(t('q5')):
        st.write(t('a5'))
        st.write(t('score1'))
        st.write(t('score2'))
        st.write(t('score3'))
        st.write(t('score4'))
        st.write(t('score5'))
    
    with st.expander(t('q6')):
        st.write(t('a6'))

# ==================== TAB 4: ADMIN ====================
if is_admin(st.session_state.current_user):
    with tab4:
        st.subheader("Admin Dashboard")
        st.success("Welcome Administrator")
        
        users = load_users()
        total_users = len(users)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t('total_users'), total_users)
        with col2:
            regular_users = len([u for u in users.values() if u.get("role") == "user"])
            st.metric(t('regular_users'), regular_users)
        with col3:
            admins = len([u for u in users.values() if u.get("role") == "admin"])
            st.metric(t('admins'), admins)
        
        st.markdown("---")
        
        st.subheader(t('all_users'))
        user_data = []
        for email, data in users.items():
            user_data.append({
                "Email": email,
                "Role": data.get("role", "user"),
                "Created": data.get("created_at", "Unknown"),
                "Verified": "Yes" if data.get("verified", False) else "No"
            })
        st.dataframe(pd.DataFrame(user_data), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t('delete_user'))
            user_to_delete = st.selectbox(t('select_user'), list(users.keys()))
            if st.button("Delete Selected User", use_container_width=True):
                if user_to_delete == st.session_state.current_user:
                    st.error("You cannot delete yourself!")
                else:
                    del users[user_to_delete]
                    save_users(users)
                    st.success(f"User {user_to_delete} deleted successfully!")
                    st.rerun()
        
        with col2:
            st.subheader(t('make_admin'))
            regular_users_list = [u for u in users.keys() if users[u].get("role") != "admin"]
            if regular_users_list:
                user_to_promote = st.selectbox(t('select_user_promote'), regular_users_list)
                if st.button("Make Admin", use_container_width=True):
                    users[user_to_promote]["role"] = "admin"
                    save_users(users)
                    st.success(f"{user_to_promote} is now an admin!")
                    st.rerun()
            else:
                st.info("No regular users to promote")
