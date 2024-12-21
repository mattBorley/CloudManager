import bcrypt

# Password validation criteria (same as frontend)
password_criteria = [
    {"id": 1, "rule": "At least 8 characters", "test": lambda password: len(password) >= 8},
    {"id": 2, "rule": "At least one uppercase letter", "test": lambda password: any(c.isupper() for c in password)},
    {"id": 3, "rule": "At least one lowercase letter", "test": lambda password: any(c.islower() for c in password)},
    {"id": 4, "rule": "At least one number", "test": lambda password: any(c.isdigit() for c in password)},
    {"id": 5, "rule": "At least one special character", "test": lambda password: any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)},
]

def validate_password(password: str) -> tuple[bool, str]:
    for criterion in password_criteria:
        if not criterion["test"](password):
            return False, f"Password must meet criterion: {criterion['rule']}"
    return True, "Password meets criteria"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12) #Set cost to 12
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')