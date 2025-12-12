from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

stored = "$2b$12$wwWBDVubv8wjG70bs2u9..fNzUNLq0shD2GJ9TcoXrbmtlO3K5fUm"  # твой хеш
print(pwd_context.verify("123456", stored))

