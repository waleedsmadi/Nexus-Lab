# Nexus Lab - E-commerce Development & Web Security Testing

## Overview
Nexus Lab is a specialized e-commerce project developed with **Python** and the **Django** framework. The primary goal of this repository is to provide a controlled environment for practicing **Web Vulnerability Research** and discovering security flaws in web applications.

The project is focused on the back-end implementation of essential e-commerce features, designed to be tested against common security attack vectors.

## Functional Features
The application currently includes the following core functionalities:
* **User Authentication:** Secure login, registration, and session management.
* **Product Catalog:** Dynamic product listing and detailed view.
* **Shopping Cart:** Add/Remove functionality for authenticated users.
* **Comment System:** User interaction and reviews for products.
* **Wallet System:** Digital balance management for simulated transactions.
* **Current Focus:** Development of secure checkout and purchasing logic.

## Technical Tech Stack
* **Language:** Python 3.x
* **Framework:** Django (MVT Architecture)
* **Database:** MySQL (Relational Schema)
* **Configuration:** Environment variable management using `python-decouple`.
* **Environment:** Developed and tested on **Linux (Ubuntu/Kali)**.

## Security Research & Penetration Testing Goals
This lab environment is used to simulate and mitigate the following vulnerabilities:
* **Insecure Direct Object References (IDOR):** Testing user access control to orders and profiles.
* **Injection Attacks:** Identifying and preventing SQL Injection and Cross-Site Scripting (XSS).
* **Broken Authentication:** Analyzing session handling and password hashing.
* **CSRF Analysis:** Testing Django's built-in Cross-Site Request Forgery protections.

## Installation & Setup
1. Clone the repository.
2. Set up a virtual environment: `python3 -m venv nexus_lab_env`
3. Activate the environment: `source nexus_lab_env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` with your `SECRET_KEY` and MySQL credentials.
6. Migrate and Run: `python manage.py migrate && python manage.py runserver`

---
**Developer:** Waleed Ibrahim Smadi
**Focus:** Backend Development | Web Security Research
