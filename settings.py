import os
from dotenv import load_dotenv
load_dotenv()

FROM_ADDRESS = os.getenv("FROM_ADDRESS")
TO_ADDRESS = os.getenv("TO_ADDRESS")
FROM_PWD = os.getenv("FROM_PWD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EXPECTED_FROM = os.getenv("EXPECTED_FROM")
EXPECTED_SUBJECT = os.getenv("EXPECTED_SUBJECT")
