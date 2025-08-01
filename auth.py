import pyrebase
import getpass
from firebase_config import firebase

auth = firebase.auth()

def register():
    print("--- Register New User ---")
    email = input("Enter email: ").strip()
    password = getpass.getpass("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("✔️ Registration successful. Please login.\n")
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            print("❌ This email is already registered. Please login or use another email.")
        elif "WEAK_PASSWORD" in error_str:
            print("❌ Password should be at least 6 characters.")
        elif "INVALID_EMAIL" in error_str:
            print("❌ The email address is badly formatted.")
        else:
            print("❌ Registration failed. Please check your details and try again.\n")

def login():
    print("--- User Login ---")
    email = input("Enter email: ").strip()
    password = getpass.getpass("Enter password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"✔️ Login successful. Welcome, {email.split('@')[0].capitalize()}!")
        return user
    except Exception as e:
        error_str = str(e)
        if "INVALID_PASSWORD" in error_str:
            print("❌ Incorrect password. Please try again.")
        elif "EMAIL_NOT_FOUND" in error_str:
            print("❌ No account found with this email.")
        elif "INVALID_EMAIL" in error_str:
            print("❌ The email address is badly formatted.")
        else:
            print("❌ Login failed. Please check your credentials and try again.")
        return None 