import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:test@localhost:5432/crud')
