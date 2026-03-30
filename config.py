import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
