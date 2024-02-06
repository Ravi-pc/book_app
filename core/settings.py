from os import getenv
from dotenv import load_dotenv

load_dotenv()

jwt_secrete_key = getenv('JWT_SECRETE_KEY')
sender = getenv('SENDER')
password = getenv('PASSWORD')
algorithm = getenv('ALGORITHM')
super_key = getenv('SUPER_KEY')
database_path = getenv('DATABASE_PATH')

