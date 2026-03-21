# 🛡️ Enterprise Identity & Access Management Engine (IAM)

<div align="center">
  <!-- TODO: Add your project banner image below -->
  <img src="images/placeholder-banner.png" alt="Project Banner" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/>
  
  *A high-performance, distributed Role-Based Access Control (RBAC) and Authentication Engine built with Django REST Framework.*
</div>

<br/>

## 📌 Project Overview
This repository contains the **core architecture and backend engine** for a large-scale Enterprise Resource Planning (ERP) system. During my Software Development Internship at Dyota Infotech, I **architected and developed the entire Identity and Access Control Layer from the ground up**. 

To protect the company's intellectual property, the proprietary 40+ business logic modules (accounting, HR, academics, etc.) and the frontend interface have been deliberately excluded. This repository isolates and showcases the **Advanced ACL**, **Custom Auth**, and **RBAC mechanisms** I built.

---

## 🏗️ System Architecture & Design

<div align="center">
  <!-- TODO: Add your main architecture diagram image below -->
  <img src="images/architecture-diagram.png" alt="Architecture Diagram" width="800" style="border-radius: 8px; margin: 20px 0;"/>
</div>

### 🔐 1. Advanced ACL (Access Control) & RBAC Engine
I designed a deeply integrated access control system that goes far beyond Django's basic permission constraints:

*   **Dynamic Permission Matrix:** An architecture to automatically seed over **148+ highly granular permissions** across 37 different system modules.
*   **Hierarchical Role Distribution:** Users can be assigned multiple roles simultaneously (e.g., `Superadmin`, `Teacher`, `Front Office`), and the system dynamically computes their effective "net permission" matrix at runtime.
*   **High-Speed Caching:** To prevent severe database bottlenecks on every incoming TCP/HTTP request, the computed permission matrix for every active user is cached in **Redis**.
*   **Custom Edge Middleware:** I wrote a custom `PermissionMiddleware` that intercepts incoming requests, matches the requested endpoint against the user's cached ACL matrix, and rejects unauthorized traffic before it ever hits the expensive View layer.

### 🔑 2. Enterprise Authentication System

<div align="center">
  <!-- TODO: Add an image explaining the authentication flow (JWT/MFA) -->
  <img src="images/auth-flow.png" alt="Authentication Flow Diagram" width="800" style="border-radius: 8px; margin: 20px 0;"/>
</div>

*   **Stateless JWT with Opaque Refresh:** Implemented a highly secure token rotation strategy (`HS256` / `RS256` compatible) with strict token blacklisting.
*   **Multi-Factor Authentication (MFA):** Integrated OTP capabilities linked directly to a centralized session manager.
*   **Session & Device Fingerprinting:** Every login generates a device fingerprint, allowing security admins (or the users themselves) to monitor active sessions and remotely terminate potentially compromised devices.
*   **Security Audit Logging:** Engineered an asynchronous audit trail. Every single authentication event (login success, failure, suspicious IP, MFA trigger, password reset) is logged strictly for enterprise compliance.

### 🧑‍💻 3. Custom Decoupled User Model
*   Stripped away the default Django username dependency, transitioning the entire system to a strict, secure **Email-First** User model.
*   Designed highly scalable junction tables (`UserRoleAssignment`) that safely detach the user's identity footprint from their modular permissions.

---

## 🛠️ Tech Stack & Tooling

| Category | Technologies Used |
| :--- | :--- |
| **Core Framework** | Python 3.12, Django 5.x, Django REST Framework (DRF) |
| **Database** | PostgreSQL |
| **In-Memory Cache** | Redis (For Permission/Session caching) |
| **Security & Crypto** | PyJWT, Cryptography, Argon2 (Password Hashing) |
| **API Documentation**| DRF Spectacular (OpenAPI 3.0 / Swagger UI) |

---

## 📸 Core Features Showcase

### ❖ Dynamic Role Assignment API
<!-- TODO: Add screenshot of Postman / Swagger testing the Role endpoint -->
![Role Assignment API](images/role-assignment-screenshot.png)

### ❖ Real-time Security Audit Logs
<!-- TODO: Add screenshot of the database tables or JSON response showing audit logs -->
![Security Audit Logs](images/audit-logs-screenshot.png)

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL running on `localhost:5432`
*   Redis Server running on `localhost:6379`

### 2. Setup Guide

```bash
# Clone the repository
git clone https://github.com/yourusername/enterprise-iam-engine.git
cd enterprise-iam-engine

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements/dev.txt

# Configure Environment
cp backend/.env.example backend/.env
# Note: Ensure PostgreSQL and Redis credentials in your .env match your local setup.
# Ensure JWT_ALGORITHM=HS256 for local developmental testing.

# Generate Initial Migrations and Apply them
cd backend
python manage.py makemigrations users roles authentication core
python manage.py migrate

# Run the API Server
python manage.py runserver 0.0.0.0:8001
```

### 3. API Documentation
Once the server is running, the Open API schema is automatically generated. You can explore the IAM endpoints visually:
*   **Swagger UI:** `http://localhost:8001/api/docs/`
*   **ReDoc:** `http://localhost:8001/api/redoc/`

---

<div align="center">
  <b>Architected & Developed by Anant</b><br>
  <i>Software Engineering Intern @ Dyota Infotech (Oct 2025 - Jan 2026)</i>
</div>
