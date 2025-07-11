# Cybersecurity\_Test\_01

Welcome to the technical challenge for the **Cybersecurity Engineer** position. In this test, we assess your ability to detect and mitigate vulnerabilities in backend applications developed with Python and FastAPI.

---

## Challenge Overview

You are provided with a pre-built **FastAPI** application intentionally containing several common security vulnerabilities. Your mission is to **analyze, identify, document, and patch** the vulnerabilities in the codebase, ensuring the API meets security best practices.

---

## Project Description

This project simulates a vulnerable backend service that handles user login and profile information. The application is Dockerized and includes endpoints that resemble real-world security pitfalls.

The goal is to demonstrate your ability to:

- Perform code audit and API testing
- Identify and explain common web vulnerabilities
- Apply mitigations using Python best practices
- Deliver clean and secure backend code

---

## API Endpoints

- `POST /login`

- `GET /profile/{user_id}`

- `POST /exec`

- `GET /health`

---

## How to Run the Project Locally

### Requirements

- Docker
- Docker Compose

### Run the Application

```bash
# Clone this project
$ git clone <repo-url> && cd insecure-fastapi

# Build and run
$ docker-compose up --build

# API is now running at:
http://localhost:8000
```

---

## Your Tasks

1. Analyze the code in `main.py` and identify all vulnerabilities.
2. Fix the vulnerabilities by applying secure coding practices.
3. Document the identified issues in a file called `report`.
4. Deliver a `secure_api.py` file or folder with your secure version of the app.

---

## Expected Deliverables

You are expected to deliver:

- A secure version of the codebase in a folder such as `secure_api/`
- A concise and professionally structured report summarizing your findings, reasoning, and remediations

---

## Evaluation Criteria

We will assess your submission based on:

1. Vulnerability detection accuracy
2. Quality and completeness of the fixes
3. Security best practices applied
4. Code readability and structure
5. Clarity of documentation

---

## Security Tip

Please do not use production secrets, real credentials, or copy external code without understanding. This test simulates a real-world environment where **secure-by-design thinking** is essential.

---

We look forward to seeing your secure coding skills in action!

Good luck!
