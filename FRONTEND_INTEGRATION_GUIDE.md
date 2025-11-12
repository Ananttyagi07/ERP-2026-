# 🌐 Frontend Integration Guide - Login & Authentication

## 📋 Table of Contents
1. [Login Flow Overview](#login-flow-overview)
2. [Login Page Implementation](#login-page-implementation)
3. [API Endpoints](#api-endpoints)
4. [Authentication Flow](#authentication-flow)
5. [Code Examples](#code-examples)
6. [Security Best Practices](#security-best-practices)

---

## 🎯 Login Flow Overview

### **What Your Users Will See:**

```
User Journey:
1. User opens website: https://your-erp.com
2. Sees Login Page (first page)
3. Enters email/username + password
4. Clicks "Login"
5. Backend validates credentials
6. If valid: Redirected to their dashboard
7. If invalid: Error message shown
```

### **How Backend Handles It:**

```
Frontend                      Backend                     Database
    |                            |                            |
    |-- POST /api/auth/login/ -->|                            |
    |   {email, password}        |                            |
    |                            |-- Check user in DB ------->|
    |                            |<-- User found --------------|
    |                            |                            |
    |                            |-- Verify password hash --->|
    |                            |<-- Password valid ---------|
    |                            |                            |
    |                            |-- Generate JWT tokens      |
    |                            |-- Create session           |
    |                            |-- Log audit entry -------->|
    |                            |                            |
    |<-- Success + tokens -------|                            |
    |   {user, tokens, redirect} |                            |
    |                            |                            |
    |-- Store tokens in localStorage/cookies                  |
    |-- Redirect to dashboard    |                            |
```

---

## 🔐 Current Login Endpoints

### **You Have 2 Login Options:**

#### **Option 1: Basic Login** (Simpler, faster)
```
POST /api/auth/login/

Features:
- Email + password authentication
- JWT tokens returned
- Role-based redirect URL
- Backward compatible
- No MFA (simpler for basic users)
```

#### **Option 2: Enhanced Login** (More secure, enterprise-grade)
```
POST /api/auth/login/secure/

Features:
- Everything from basic login, PLUS:
- Session tracking (device, location)
- Trust scoring (0-100)
- MFA support (if enabled)
- Audit logging
- Suspicious activity detection
```

**Recommendation:** Use **Option 2** (`/api/auth/login/secure/`) for production!

---

## 🎨 Login Page Implementation

### **What Your Frontend Needs:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>University ERP - Login</title>
</head>
<body>
    <!-- Login Page (First page users see) -->
    <div class="login-container">
        <div class="login-box">
            <img src="/logo.png" alt="University Logo">
            <h1>Welcome to University ERP</h1>

            <form id="loginForm">
                <!-- Email/Username Input -->
                <div class="form-group">
                    <label>Email Address</label>
                    <input
                        type="email"
                        id="email"
                        placeholder="your.email@university.edu"
                        required
                    >
                </div>

                <!-- Password Input -->
                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        id="password"
                        placeholder="Enter your password"
                        required
                    >
                </div>

                <!-- Remember Me -->
                <div class="form-group">
                    <input type="checkbox" id="rememberMe">
                    <label for="rememberMe">Remember me</label>
                </div>

                <!-- Login Button -->
                <button type="submit" id="loginBtn">
                    Login
                </button>

                <!-- Error Message -->
                <div id="errorMessage" class="error" style="display: none;"></div>

                <!-- Links -->
                <div class="links">
                    <a href="/forgot-password">Forgot Password?</a>
                </div>
            </form>
        </div>
    </div>

    <script src="/js/login.js"></script>
</body>
</html>
```

---

## 🔧 JavaScript Implementation

### **Complete Login Logic:**

```javascript
// File: /js/login.js

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';  // Change in production
const LOGIN_ENDPOINT = '/auth/login/secure/';  // Enhanced login

// DOM Elements
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('loginBtn');
const errorMessage = document.getElementById('errorMessage');

// Handle form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable button during request
    loginBtn.disabled = true;
    loginBtn.textContent = 'Logging in...';
    errorMessage.style.display = 'none';

    // Get form data
    const credentials = {
        email: emailInput.value.trim(),
        password: passwordInput.value
    };

    try {
        // Call login API
        const response = await fetch(`${API_BASE_URL}${LOGIN_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials)
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // ✅ LOGIN SUCCESS

            // Check if MFA is required
            if (data.data.mfa_required) {
                // Redirect to MFA verification page
                sessionStorage.setItem('mfa_session_id', data.data.session_id);
                sessionStorage.setItem('mfa_methods', JSON.stringify(data.data.mfa_methods));
                window.location.href = '/mfa-verify.html';
                return;
            }

            // No MFA required - proceed with login
            handleSuccessfulLogin(data.data);

        } else {
            // ❌ LOGIN FAILED
            showError(data.message || 'Invalid email or password');
        }

    } catch (error) {
        console.error('Login error:', error);
        showError('Connection error. Please try again.');
    } finally {
        // Re-enable button
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
    }
});

// Handle successful login
function handleSuccessfulLogin(data) {
    // Store tokens
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);

    // Store user info
    localStorage.setItem('user', JSON.stringify(data.user));

    // Store session ID (for session management)
    if (data.session_id) {
        localStorage.setItem('session_id', data.session_id);
    }

    // Show success message
    showSuccess('Login successful! Redirecting...');

    // Redirect based on role
    setTimeout(() => {
        window.location.href = data.redirect_url || '/dashboard';
    }, 1000);
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.className = 'error';
}

// Show success message
function showSuccess(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.className = 'success';
}
```

---

## 📡 API Request/Response Examples

### **Example 1: Successful Login (No MFA)**

**Request:**
```http
POST /api/auth/login/secure/
Content-Type: application/json

{
  "email": "student@university.edu",
  "password": "student123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1001,
      "email": "student@university.edu",
      "username": "student001",
      "full_name": "John Doe",
      "primary_role": {
        "id": 4,
        "name": "Student",
        "description": "Student account"
      },
      "college_id": 1,
      "college_name": "MIT University"
    },
    "tokens": {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "d3f8a2b4c1e9f7a3d2b5c8e1f4a7d3b9..."
    },
    "session_id": "abc-123-def-456-ghi-789",
    "redirect_url": "/student/dashboard",
    "trust_score": 75
  }
}
```

**What Frontend Should Do:**
1. Store `tokens.access` in localStorage (or httpOnly cookie)
2. Store `tokens.refresh` in localStorage
3. Store `user` object in localStorage
4. Redirect to `redirect_url` (/student/dashboard)

---

### **Example 2: Successful Login (MFA Required)**

**Request:** (Same as above)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "MFA verification required",
  "data": {
    "mfa_required": true,
    "mfa_methods": ["totp", "sms", "email"],
    "session_id": "temp-session-xyz123",
    "trust_score": 45,
    "is_suspicious": false
  }
}
```

**What Frontend Should Do:**
1. Save `session_id` temporarily
2. Show MFA verification page
3. Let user choose method (TOTP/SMS/Email)
4. Call `/api/auth/mfa/verify/` with code

---

### **Example 3: Failed Login**

**Request:** (Same as above)

**Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "errors": {
    "non_field_errors": ["Invalid email or password"]
  }
}
```

**What Frontend Should Do:**
1. Show error message: "Invalid email or password"
2. Keep user on login page
3. Clear password field (security best practice)

---

### **Example 4: Account Locked**

**Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Account is inactive. Please contact administrator."
}
```

---

## 🔐 Making Authenticated Requests

### **After Login, Include Token in All Requests:**

```javascript
// Example: Fetch user dashboard
async function fetchDashboard() {
    const accessToken = localStorage.getItem('access_token');

    const response = await fetch(`${API_BASE_URL}/students/me/dashboard/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`  // ← Include token
        }
    });

    if (response.status === 401) {
        // Token expired - refresh it
        await refreshAccessToken();
        // Retry request
        return fetchDashboard();
    }

    const data = await response.json();
    return data;
}
```

---

## 🔄 Token Refresh Flow

### **Access Token Expires Every 15 Minutes:**

```javascript
// Refresh token when access token expires
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Update tokens
            localStorage.setItem('access_token', data.data.tokens.access);
            localStorage.setItem('refresh_token', data.data.tokens.refresh);
            return true;
        } else {
            // Refresh token invalid - logout user
            logout();
            return false;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
        logout();
        return false;
    }
}

// Logout user
function logout() {
    localStorage.clear();
    window.location.href = '/login.html';
}
```

---

## 🎭 Role-Based Redirects

### **After Login, Redirect Based on Role:**

```javascript
function handleSuccessfulLogin(data) {
    const user = data.user;
    const role = user.primary_role.name;

    // Store tokens and user info
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(user));

    // Redirect based on role
    let dashboardUrl;

    switch(role) {
        case 'Superadmin':
            dashboardUrl = '/superadmin/dashboard.html';
            break;
        case 'Admin':
            dashboardUrl = '/admin/dashboard.html';
            break;
        case 'Teacher':
            dashboardUrl = '/teacher/dashboard.html';
            break;
        case 'Student':
            dashboardUrl = '/student/dashboard.html';
            break;
        default:
            dashboardUrl = '/dashboard.html';
    }

    // Or use the redirect_url from backend
    dashboardUrl = data.redirect_url || dashboardUrl;

    // Redirect
    window.location.href = dashboardUrl;
}
```

---

## 🛡️ Security Best Practices

### **1. Protect Against XSS (Cross-Site Scripting)**

```javascript
// GOOD: Store in httpOnly cookies (backend sets them)
// BETTER: Use httpOnly + secure + sameSite cookies

// If using localStorage (easier for SPA):
// - Never use eval() or innerHTML with user data
// - Sanitize all user inputs
// - Use Content Security Policy (CSP) headers
```

### **2. Protect Against CSRF (Cross-Site Request Forgery)**

```javascript
// Backend already has CSRF protection
// For API calls from frontend, include CSRF token:

// Get CSRF token from cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Include in POST requests
const csrfToken = getCookie('csrftoken');

fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
```

### **3. Implement Auto-Logout on Token Expiry**

```javascript
// Check token expiry on page load
function checkAuthStatus() {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        // Not logged in - redirect to login
        if (window.location.pathname !== '/login.html') {
            window.location.href = '/login.html';
        }
        return;
    }

    // Decode JWT to check expiry (simple example)
    try {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        const expiryTime = payload.exp * 1000; // Convert to milliseconds
        const currentTime = Date.now();

        if (currentTime >= expiryTime) {
            // Token expired - try to refresh
            refreshAccessToken();
        }
    } catch (error) {
        console.error('Token validation error:', error);
        logout();
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', checkAuthStatus);
```

---

## 🔄 Complete Login/Logout Flow

### **Login Flow (Full Code Example):**

```javascript
// login.js - Complete implementation

class AuthService {
    constructor() {
        this.API_BASE = 'http://localhost:8000/api';
    }

    // Login method
    async login(email, password) {
        try {
            const response = await fetch(`${this.API_BASE}/auth/login/secure/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',  // Include cookies
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }

            // Check if MFA required
            if (data.data.mfa_required) {
                return {
                    success: true,
                    mfa_required: true,
                    session_id: data.data.session_id,
                    mfa_methods: data.data.mfa_methods
                };
            }

            // Save tokens
            this.saveTokens(data.data.tokens);
            this.saveUser(data.data.user);
            this.saveSession(data.data.session_id);

            return {
                success: true,
                mfa_required: false,
                redirect_url: data.data.redirect_url,
                user: data.data.user
            };

        } catch (error) {
            console.error('Login error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Logout method
    async logout() {
        const accessToken = this.getAccessToken();
        const refreshToken = this.getRefreshToken();
        const sessionId = this.getSessionId();

        try {
            // Call logout API
            await fetch(`${this.API_BASE}/auth/logout/secure/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    refresh_token: refreshToken,
                    session_id: sessionId
                })
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Clear local storage
            this.clearAuth();
            // Redirect to login
            window.location.href = '/login.html';
        }
    }

    // Save tokens
    saveTokens(tokens) {
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
    }

    // Save user info
    saveUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    }

    // Save session ID
    saveSession(sessionId) {
        localStorage.setItem('session_id', sessionId);
    }

    // Get access token
    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    // Get refresh token
    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    // Get session ID
    getSessionId() {
        return localStorage.getItem('session_id');
    }

    // Get user info
    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    // Check if logged in
    isLoggedIn() {
        return !!this.getAccessToken();
    }

    // Clear auth data
    clearAuth() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('session_id');
    }

    // Refresh access token
    async refreshToken() {
        const refreshToken = this.getRefreshToken();

        try {
            const response = await fetch(`${this.API_BASE}/auth/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.saveTokens(data.data.tokens);
                return true;
            } else {
                this.logout();
                return false;
            }
        } catch (error) {
            console.error('Token refresh error:', error);
            this.logout();
            return false;
        }
    }
}

// Create global instance
const authService = new AuthService();

// Usage in login form
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const result = await authService.login(email, password);

    if (result.success && !result.mfa_required) {
        // Login successful
        window.location.href = result.redirect_url;
    } else if (result.mfa_required) {
        // Redirect to MFA page
        window.location.href = '/mfa-verify.html';
    } else {
        // Show error
        alert(result.error);
    }
});
```

---

## 🎯 Summary

### **✅ Your Login System Supports:**

1. **Email + Password authentication** ✓
2. **Database-stored credentials** ✓
3. **JWT tokens** (access + refresh) ✓
4. **Role-based redirects** ✓
5. **MFA support** (optional) ✓
6. **Session tracking** ✓
7. **Audit logging** ✓

### **📋 Frontend Checklist:**

- [ ] Create login page (first page)
- [ ] Add email + password form
- [ ] Call `/api/auth/login/secure/` on submit
- [ ] Store tokens in localStorage
- [ ] Handle MFA flow (if enabled)
- [ ] Redirect based on role
- [ ] Include token in all API requests
- [ ] Implement token refresh
- [ ] Add logout functionality

### **🔗 Key Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/login/` | POST | Basic login |
| `/api/auth/login/secure/` | POST | Enhanced login (recommended) |
| `/api/auth/logout/` | POST | Logout |
| `/api/auth/refresh/` | POST | Refresh tokens |
| `/api/auth/mfa/verify/` | POST | Verify MFA code |

### **💡 Best Practice:**

Use **`/api/auth/login/secure/`** for production. It gives you:
- Session management ✓
- Device tracking ✓
- Trust scoring ✓
- Audit logging ✓
- MFA support ✓

---

**Your backend is 100% ready for frontend integration!** Just implement the login page following this guide. 🚀
