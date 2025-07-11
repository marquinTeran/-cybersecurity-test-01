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

## 3. Plaintext password stored for admin user

**Where was the problem:**
The default admin user was created with the password `"admin123"` stored as plain text in the database

**Details:**
Storing passwords without hashing is a serious security issue. Anyone with access to the database could see user passwords directly

**Level Risk:** High
If the database is leaked or accessed by mistake, all passwords would be exposed

**Fix:**
- Installed the `bcrypt` library
- The password is now hashed using `bcrypt.hashpw()` before saving
- Only applies when running in development mode

## 4. Login compared passwords without hashing

**Where was the problem:**
In the `/login` endpoint, the password was compared directly with the stored password in the database.

**Details:**
This worked only when passwords were saved in plain text. After hashing passwords, this method became invalid and insecure.

**Level Risk:** High
Comparing raw passwords with hashed ones doesn't work and breaks the login. It also ignores the need for secure password handling.

**Fix:**
- The login now only selects the user by username.
- Then it checks the password using `bcrypt.checkpw()`, which compares the entered password with the stored hash.

## 5. Command injection vulnerability in /exec

**Where was the problem:**
There was an endpoint (`/exec`) that allowed any command to be executed on the system using `os.system()` and user input.

**Details:**
This is a very dangerous practice. A user could send commands like `rm -rf /` or install malware on the server. The input was not validated or restricted in any way.

**Level Risk:** Critical
Anyone could run any system command just by calling this endpoint.

**Fix:**
- The endpoint was deleted completely, since it had no real purpose and posed a high security risk.

## 6. JWT tokens did not expire

**Where was the problem:**
The `/login` endpoint created JWT tokens without an expiration date.

**Details:**
Tokens without expiration can be used forever. If a token is stolen, an attacker can access the system permanently without re-authentication.

**Level Risk:** High
This is a serious session management issue and a common security problem.

**Fix:**
- Added the `exp` (expiration) field to the JWT payload.
- Tokens now expire 45 minutes after creation.
- If a token is expired, the user must log in again to receive a new one.

## 7. /profile endpoint was not protected

**Where was the problem:**
The `/profile/{user_id}` endpoint could be accessed without a valid token. Anyone could get user data by knowing the ID.

**Details:**
There was no authentication required. This means any user could retrieve data about others without logging in.

**Level Risk:** High
User data exposure is a serious privacy and security issue.

**Fix:**
- Added token validation using `HTTPBearer` and `jwt.decode()`.
- Now the endpoint rejects requests with no or invalid token.
