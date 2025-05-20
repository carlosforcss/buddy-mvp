from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DEFAULT_BUCKET_NAME = os.getenv("DEFAULT_BUCKET_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
