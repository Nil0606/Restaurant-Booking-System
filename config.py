import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build database config dictionary from environment variables
DATABASE = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "pass"),
    "database": os.getenv("DB_NAME", "production"),
}
