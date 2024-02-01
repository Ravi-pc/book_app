import bcrypt


def hash_password(password: str) -> str:
    """
        Description: hash_password function is used to hash the password.
        Parameter: normal password.
        Return: hashed password.
    """
    hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    return hashed_password_str
