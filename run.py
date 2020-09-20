from app.readmail import EmailChecker
from settings import SMTP_SERVER, FROM_PWD, FROM_ADDRESS, EXPECTED_FROM, EXPECTED_SUBJECT, TO_ADDRESS


if __name__ == "__main__":
    with EmailChecker(
            from_address=FROM_ADDRESS, pwd=FROM_PWD, server=SMTP_SERVER, to_address=TO_ADDRESS) as casa:
        if not casa.is_ok(EXPECTED_FROM, EXPECTED_SUBJECT):
            casa.send_alert()
