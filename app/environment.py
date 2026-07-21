import os
from load_dotenv import load_dotenv

load_dotenv()

try:
    GEMINI_MODEL = os.environ["GEMINI_MODEL"]
    APP_NAME = os.environ["APP_NAME"]
except Exception as e:
    raise Exception(str(e))