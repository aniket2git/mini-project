import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    database_url = os.getenv("DATABASE_URL")

    if database_url.startswith("postgres://"):

        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024