# Security Report

## 1. SECRET_KEY hardcoded in main.py
**Where was the problem:**
The secret key for JWT tokens was written directly in the code:

**Details:**
The secret key used to sign JWT tokens was hardcoded directly in the source code. This is a critical security flaw, especially if the code is ever exposed publicly or shared internally without restriction.

**Level Risk:** High
If leaked, an attacker could forge valid tokens and impersonate any user.

**Fix:**
- The hardcoded key was removed.
- A `.env` file was created to store the key.
- The application now loads the key using `python-dotenv`
- Created `.env-example` file as a template for developers
