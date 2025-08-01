import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

# TODO: Replace with your Firebase project config
firebase_config = {
    "apiKey": "AIzaSyCvKKSZreLB8TLEnxfz9FSfT7KBvkMRm_U",
    "authDomain": "projecttt-f83aa.firebaseapp.com",
    "databaseURL": "",
    "projectId": "projecttt-f83aa",
    "storageBucket": "projecttt-f83aa.firebasestorage.app",
    "messagingSenderId": "208129143693",
    "appId": "1:208129143693:web:e3deb22fe5db6b24f543c4"
}

firebase = pyrebase.initialize_app(firebase_config)

# Firestore admin setup
cred = credentials.Certificate("serviceAccountKey.json")  # Download from Firebase Console
firebase_admin.initialize_app(cred)
db = firestore.client() 