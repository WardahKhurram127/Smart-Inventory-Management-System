# Smart Inventory Management System with Predictive Ordering

## Overview
A console-based inventory management system with Firebase authentication, Firestore storage, and predictive ordering analytics.

## Features
- User registration and login (Firebase Auth)
- Inventory CRUD (Firestore)
- Sales and restocking tracking
- Reports and analytics
- Predictive reordering

## Setup
1. **Clone the repo**
2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Firebase Setup**
   - Create a Firebase project at https://console.firebase.google.com/
   - Enable Email/Password Authentication
   - Create a Firestore database
   - Download your service account key as `serviceAccountKey.json` and place it in the project folder
   - In `firebase_config.py`, fill in your Firebase config details

4. **Run the app**
   ```
   python main.py
   ```

## Notes
- All data is stored in Firestore collections: Products, Sales, Restocks, Users
- Predictive reordering uses simple sales trend analysis
- For production, secure your service account key and restrict database rules 