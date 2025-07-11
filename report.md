# Security Report

## 1. SECRET_KEY hardcoded in main.py
**Where was the problem:**
The secret key for JWT tokens was written directly in the code

**Details:**
The secret key used to sign JWT tokens was hardcoded directly in the source code. This is a critical security flaw, especially if the code is ever exposed publicly or shared internally without restriction.

**Level Risk:** High
If leaked, an attacker could forge valid tokens and impersonate any user.

**Fix:**
- The hardcoded key was removed.
- A `.env` file was created to store the key.
- The application now loads the key using `python-dotenv`
- Created `.env-example` file as a template for developers

## 2. Default admin user created on init app
**Where was the problem:**
The app was creating an admin user (`admin` / `admin123`) every time on init.

**Details:**
Every time the application starts, a hardcoded admin user is inserted into the database. This is extremely risky if the application runs in a production environment, since attackers often try common credentials like `admin/admin123`

**Level Risk:** High  
If the application runs in production with this user, anyone can log in with admin access

**Fix:**  
- Introduced an environment variable `ENV`
- The default user is only created when `ENV=dev`
- Prevents the admin user from being inserted automatically in production
