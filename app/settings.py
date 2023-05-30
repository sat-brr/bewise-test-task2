import os

import dotenv

dotenv.load_dotenv()

APP_PORT = int(os.getenv("APP_PORT"))
DB_URL = os.getenv("DB_URL")
