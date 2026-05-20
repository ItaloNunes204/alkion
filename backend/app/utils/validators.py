import re


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"

    return True, ""


def validate_cnpj(cnpj: str) -> bool:
    # Remove non-numeric characters
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    # CNPJ must have 14 digits
    if len(cnpj) != 14:
        return False

    # CNPJ cannot have all digits the same
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validate first check digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = 0
    for i in range(12):
        total += int(cnpj[i]) * weights[i]
    remainder = total % 11
    if remainder < 2:
        digit1 = 0
    else:
        digit1 = 11 - remainder

    # Validate second check digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = 0
    for i in range(13):
        total += int(cnpj[i]) * weights[i]
    remainder = total % 11
    if remainder < 2:
        digit2 = 0
    else:
        digit2 = 11 - remainder

    # Check if the calculated digits match the input
    if int(cnpj[12]) != digit1:
        return False

    if int(cnpj[13]) != digit2:
        return False

    return True
