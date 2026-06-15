import re
import html

MAX_NAME_LENGTH = 100
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 128

def sanitize_string(value: str, max_length: int = MAX_NAME_LENGTH) -> str:
    if not isinstance(value, str):
        raise ValueError("Πρέπει να είναι κείμενο")

    # Αφαίρεσε whitespace από αρχή/τέλος
    value = value.strip()

    # Έλεγξε μήκος
    if len(value) == 0:
        raise ValueError("Το πεδίο δεν μπορεί να είναι κενό")
    if len(value) > max_length:
        raise ValueError(f"Μέγιστο μήκος {max_length} χαρακτήρες")

    # Escape HTML χαρακτήρες (<, >, &, ", ')
    # Αυτό μετατρέπει πχ <script> σε &lt;script&gt; — αδύνατο να εκτελεστεί
    value = html.escape(value)

    # Απομάκρυνε SQL injection patterns
    # Δεν είναι απαραίτητο λόγω SQLAlchemy αλλά extra layer ασφάλειας
    sql_patterns = r"(--|;|/\*|\*/|xp_|union|select|insert|drop|delete|update|exec|execute)"
    if re.search(sql_patterns, value, re.IGNORECASE):
        raise ValueError("Μη έγκυρο περιεχόμενο")

    return value

def sanitize_username(value: str) -> str:
    value = sanitize_string(value, max_length=MAX_USERNAME_LENGTH)
    # Username: μόνο γράμματα, αριθμοί, underscore, παύλα
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError("Το username επιτρέπει μόνο γράμματα, αριθμούς, _ και -")
    return value

def sanitize_password(value: str) -> str:
    # Password δεν κάνουμε html.escape γιατί μπορεί να έχει σύμβολα
    # Μόνο μήκος και whitespace
    value = value.strip()
    if len(value) < 8:
        raise ValueError("Ο κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες")
    if len(value) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Μέγιστο μήκος {MAX_PASSWORD_LENGTH} χαρακτήρες")
    return value
