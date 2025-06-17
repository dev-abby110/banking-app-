import streamlit as st
from Banking.account import SavingsAccount, CurrentAccount
from Banking.transactions import deposit, withdraw
import time

# Initialize session state for accounts if it doesn't exist
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}

# Custom CSS
def local_css():
    st.markdown("""
        <style>
        :root {
            --primary-color: #6C63FF;
            --secondary-color: #4CAF50;
            --accent-color: #FF6B6B;
            --background-color: #F0F2F6;
            --text-color: #2C3E50;
            --light-text: #6B7C93;
        }
        
        .main {
            padding: 0rem 1rem;
            background: linear-gradient(135deg, #ECE9E6 0%, #FFFFFF 100%);
        }
        
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary-color) 0%, #5046E4 100%);
            color: white;
            padding: 0.8rem;
            border-radius: 30px;
            border: none;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(108, 99, 255, 0.2);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
            background: linear-gradient(135deg, #5046E4 0%, #3F3AC1 100%);
        }
        
        .success-message {
            padding: 1.2rem;
            background: linear-gradient(135deg, var(--secondary-color) 0%, #388E3C 100%);
            border: none;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
            animation: slideIn 0.5s ease-out;
        }
        
        .error-message {
            padding: 1.2rem;
            background: linear-gradient(135deg, var(--accent-color) 0%, #E53935 100%);
            border: none;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-10px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .account-card {
            padding: 2rem;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        
        .account-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.2);
            border: 1px solid rgba(108, 99, 255, 0.1);
        }
        
        .balance-display {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color) 0%, #5046E4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 2rem;
            background-color: #FFFFFF;
            border-radius: 20px;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(108, 99, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .balance-display::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, 
                var(--primary-color) 0%, 
                var(--secondary-color) 50%, 
                var(--accent-color) 100%);
        }
        
        .sidebar .css-1d391kg {
            background: linear-gradient(180deg, var(--primary-color) 0%, #5046E4 100%);
            color: white;
        }
        
        h1 {
            background: linear-gradient(135deg, var(--primary-color) 0%, #5046E4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5em;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h2 {
            color: var(--primary-color);
            font-weight: 700;
            margin-bottom: 1rem;
            position: relative;
            display: inline-block;
        }
        
        h2::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, 
                var(--primary-color) 0%, 
                transparent 100%);
            border-radius: 2px;
        }
        
        h3 {
            color: var(--text-color);
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .stTextInput>div>div>input {
            border-radius: 15px;
            border: 2px solid #E0E7FF;
            padding: 1rem;
            font-size: 1.1em;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.2);
            transform: translateY(-1px);
        }
        
        .stSelectbox>div>div>div {
            border-radius: 15px;
            border: 2px solid #E0E7FF;
            background: rgba(255, 255, 255, 0.9);
            transition: all 0.3s ease;
        }
        
        .stSelectbox>div>div>div:hover {
            border-color: var(--primary-color);
            transform: translateY(-1px);
        }
        
        .stNumberInput>div>div>input {
            border-radius: 15px;
            border: 2px solid #E0E7FF;
            background: rgba(255, 255, 255, 0.9);
            transition: all 0.3s ease;
        }
        
        .stNumberInput>div>div>input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.2);
            transform: translateY(-1px);
        }
        
        .tab-content {
            background: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
        }
        
        .css-1y4p8pa {
            max-width: 1200px;
            padding: 2rem;
        }
        
        .banking-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, 
                var(--primary-color) 0%, 
                var(--secondary-color) 50%, 
                var(--accent-color) 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.15);
        }
        
        .feature-card:hover::before {
            transform: scaleX(1);
        }
        
        .feature-card h3 {
            color: var(--primary-color);
            font-size: 1.5em;
            margin-bottom: 1rem;
        }
        
        .feature-card p {
            color: var(--light-text);
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        .stTab {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        
        .stTab:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.15);
        }
        
        footer {
            background: linear-gradient(135deg, var(--primary-color) 0%, #5046E4 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            margin-top: 3rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, 
                rgba(255,255,255,0.1) 0%, 
                rgba(255,255,255,0) 100%);
            pointer-events: none;
        }
        </style>
    """, unsafe_allow_html=True)

def create_account(name, account_type, initial_deposit):
    try:
        initial_deposit = float(initial_deposit)
        if initial_deposit < 0:
            return False, "Initial deposit cannot be negative."
        
        if account_type == "Savings":
            account = SavingsAccount(name, balance=initial_deposit)
        elif account_type == "Current":
            account = CurrentAccount(name, balance=initial_deposit)
        else:
            return False, "Invalid account type. Please choose either 'Savings' or 'Current'."
        
        st.session_state.accounts[account.account_number] = account
        return True, f"Account created successfully! Your account number is: {account.account_number}"
    except ValueError:
        return False, "Please enter a valid number for initial deposit."

def display_success(message):
    st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)

def display_error(message):
    st.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)

def create_account_page():
    st.markdown("""
        <div class="account-card">
            <h2>🎉 Create New Account</h2>
            <p style="color: #666; margin-bottom: 1rem;">Join SIT Bank and experience banking at its finest</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("create_account_form"):
        name = st.text_input("Account Holder's Name", placeholder="Enter your full name")
        account_type = st.selectbox("Account Type", ["Savings", "Current"])
        initial_deposit = st.number_input("Initial Deposit Amount (₹)", min_value=0.0, step=100.0)
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        if submitted:
            if not name:
                display_error("Please enter account holder's name.")
            else:
                success, message = create_account(name, account_type, initial_deposit)
                if success:
                    display_success(message)
                    st.balloons()
                else:
                    display_error(message)

def account_operations_page():
    st.markdown("""
        <div class="account-card">
            <h2>🔐 Account Login</h2>
            <p style="color: #666; margin-bottom: 1rem;">Access your account securely</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for login attempts if not exists
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
        
    with st.form("login_form"):
        account_number = st.number_input("Enter Account Number", min_value=1210001450000, step=1)
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if account_number in st.session_state.accounts:
                st.session_state.login_attempts = 0
                user_account = st.session_state.accounts[account_number]
                st.success("Login successful!")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                display_error("Account not found. Please check your account number or create a new account.")
                if st.session_state.login_attempts >= 3:
                    st.warning("Multiple failed login attempts. Consider creating a new account if you don't have one.")
                    if st.button("Create New Account"):
                        st.session_state.login_attempts = 0
                        st.query_params["page"] = "Create Account"
                        st.rerun()
                return
    
    # Only show account operations if account exists and after successful login
    if account_number in st.session_state.accounts:
        user_account = st.session_state.accounts[account_number]
        
        # Display account information
        st.markdown(f"""
            <div class="account-card">
                <h3>👋 Welcome, {user_account.name}!</h3>
                <p style="font-size: 1.1em; color: #666; margin: 0.5rem 0;">Account Number: {user_account.account_number}</p>
                <p style="font-size: 1.1em; color: #666; margin: 0.5rem 0;">Account Type: {user_account.account_type}</p>
                <div class="balance-display" style="margin-top: 1.5rem;">
                    <p style="font-size: 0.9em; color: #666; margin-bottom: 0.5rem;">Available Balance</p>
                    <p style="font-size: 2.5em; margin: 0;">₹{user_account.get_balance():,.2f}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Add Quick Actions
        st.markdown("""
            <div class="account-card">
                <h3>💫 Quick Actions</h3>
            </div>
        """, unsafe_allow_html=True)

        # Operations tabs
        tabs = ["Deposit", "Withdraw"]
        if isinstance(user_account, SavingsAccount):
            tabs.append("Calculate Interest")
        
        selected_tab = st.tabs(tabs)
        
        # Deposit Tab
        with selected_tab[0]:
            with st.form("deposit_form"):
                deposit_amount = st.number_input("Deposit Amount (₹)", min_value=0.0, step=100.0)
                if st.form_submit_button("Confirm Deposit", use_container_width=True):
                    success, message = deposit(user_account, deposit_amount)
                    if success:
                        display_success(message)
                        time.sleep(0.5)  # Small delay for better UX
                        st.rerun()
                    else:
                        display_error(message)

        # Withdraw Tab
        with selected_tab[1]:
            with st.form("withdraw_form"):
                withdraw_amount = st.number_input("Withdrawal Amount (₹)", min_value=0.0, step=100.0)
                if st.form_submit_button("Confirm Withdrawal", use_container_width=True):
                    success, message = withdraw(user_account, withdraw_amount)
                    if success:
                        display_success(message)
                        time.sleep(0.5)  # Small delay for better UX
                        st.rerun()
                    else:
                        display_error(message)

        # Interest Tab (for Savings Account)
        if isinstance(user_account, SavingsAccount) and len(selected_tab) > 2:
            with selected_tab[2]:
                with st.form("interest_form"):
                    months = st.number_input("Number of Months", min_value=1, step=1)
                    interest_rate = user_account.interest_rate * 100
                    st.write(f"Current Interest Rate: {interest_rate:.1f}%")
                    projected_interest = user_account.get_balance() * user_account.interest_rate * months
                    st.write(f"Projected Interest: ₹{projected_interest:,.2f}")
                    
                    if st.form_submit_button("Apply Interest", use_container_width=True):
                        success, message = deposit(user_account, projected_interest)
                        if success:
                            display_success(f"Interest of ₹{projected_interest:,.2f} applied successfully!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            display_error("Failed to apply interest.")
    else:
        display_error("Account not found. Please create an account first.")

def main():
    st.set_page_config(
        page_title="SIT Bank",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_account' not in st.session_state:
        st.session_state.current_account = None
    
    local_css()
    
    # Header with Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #6C63FF 0%, #5046E4 100%); border-radius: 30px; margin-bottom: 3rem; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQ0MCIgaGVpZ2h0PSI1MDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PGxpbmVhckdyYWRpZW50IHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiIGlkPSJhIj48c3RvcCBzdG9wLWNvbG9yPSIjZmZmIiBzdG9wLW9wYWNpdHk9Ii4xIiBvZmZzZXQ9IjAlIi8+PHN0b3Agc3RvcC1jb2xvcj0iI2ZmZiIgc3RvcC1vcGFjaXR5PSIwIiBvZmZzZXQ9IjEwMCUiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48cGF0aCBkPSJNMCAyNTBjMTQ0IDk1IDI4OCAxNDQgNDMyIDE0NHM0NjAtNDggNzItMTQ0UzE0NCAyMDIgMCAyNTB6IiBmaWxsPSJ1cmwoI2EpIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48L3N2Zz4=') center bottom no-repeat; opacity: 0.1;"></div>
            <h1 style="color: white; font-size: 4em; margin-bottom: 1rem; -webkit-text-fill-color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                🏦 Welcome to SIT Bank
            </h1>
            <p style="font-size: 1.6em; color: rgba(255,255,255,0.95); margin-bottom: 2rem; font-weight: 300; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                Your Trusted Banking Partner for a Secure Future
            </p>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem 2rem; border-radius: 50px; display: inline-block; backdrop-filter: blur(5px);">
                <span style="color: white; font-size: 1.2em;">✨ Experience Modern Banking</span>
            </div>
        </div>
        
        <div class="banking-features">
            <div class="feature-card">
                <h3>🔒 Secure Banking</h3>
                <p>State-of-the-art security for your finances</p>
            </div>
            <div class="feature-card">
                <h3>💰 High Interest</h3>
                <p>Competitive interest rates on savings</p>
            </div>
            <div class="feature-card">
                <h3>📱 24/7 Access</h3>
                <p>Bank anytime, anywhere with our digital services</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2>Navigation Menu</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # If user is logged in, show logout button
        if st.session_state.authenticated and st.session_state.current_account:
            st.write(f"Welcome, {st.session_state.accounts[st.session_state.current_account].name}")
            if st.button("Logout", key="logout"):
                st.session_state.authenticated = False
                st.session_state.current_account = None
                st.rerun()
            page = "Account Operations"
        else:
            page = st.radio("", ["Create Account", "Account Operations"])
        
    if page == "Create Account":
        create_account_page()
    else:
        account_operations_page()
    
    # Footer
    st.markdown("""
        <footer>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: left; margin-bottom: 2rem;">
                <div>
                    <h3 style="color: white; margin-bottom: 1rem;">About SIT Bank</h3>
                    <p>Your trusted banking partner since 2025</p>
                </div>
                <div>
                    <h3 style="color: white; margin-bottom: 1rem;">Contact Us</h3>
                    <p>📧 support@sitbank.com</p>
                    <p>📞 1800-SIT-BANK</p>
                </div>
                <div>
                    <h3 style="color: white; margin-bottom: 1rem;">Quick Links</h3>
                    <p>Privacy Policy</p>
                    <p>Terms of Service</p>
                </div>
            </div>
            <div style="text-align: center; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
                <p>© 2025 SIT Bank. All rights reserved.</p>
            </div>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
