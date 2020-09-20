import smtplib
import time
import imaplib
import email
import time
import pytz
from email.mime.text import MIMEText
from datetime import datetime
from .logger import logger

########## CONSTANTS ##########
DELAY_MINS = 12
ROUTER_TIMEZONE = "Europe/Madrid"
###############################


class EmailChecker:
    """ Checks email """

    def __init__(self, from_address, pwd, server, to_address, port=993):
        self.__from_address = from_address
        self.__to_address = to_address
        self.__pwd = pwd
        self.__server = server
        self.__port = port
        self.mailbox = None
        self.is_logged_in = self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Expunging...")
        self.mailbox.expunge()
        logger.debug("Closing...")
        self.mailbox.close()
        logger.debug("Mailbox closed")
        self.mailbox.logout()
        logger.debug("Mailbox logged out")

    def login(self):
        try:
            logger.debug("Logging in...")
            self.mailbox = imaplib.IMAP4_SSL(self.__server)
            self.mailbox.login(self.__from_address, self.__pwd)
            self.mailbox.select('inbox')
            logger.debug("Logged in...")
            return True
        except Exception, e:
            logger.critical(str(e))
            return False

    def get_unseen_router_mail(self, expected_from, expected_subject):
        """ Retrieves mail from mailbox """
        mail = []
        self.mailbox.recent()
        typ, data = self.mailbox.search(None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()

        for i in reversed(id_list):
            typ, data = self.mailbox.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    date = msg['date']
                    date_struct = email.utils.parsedate(date)
                    date_time = datetime.fromtimestamp(
                        time.mktime(date_struct))
                    tz = pytz.timezone(ROUTER_TIMEZONE)
                    datetime_utc = toUTC(date_time, tz=tz)
                    timestamp = time.mktime(datetime_utc.timetuple())

                    if email_subject != expected_subject:
                        logger.debug('Ignoring...')
                        logger.debug('\tFrom : ' + email_from)
                        continue
                    if email_from != expected_from:
                        logger.debug('Ignoring...' + '\n')
                        logger.debug('\tSubject : ' + email_subject)
                        continue

                    logger.debug('From : ' + email_from)
                    logger.debug('Subject : ' + email_subject)
                    logger.debug(datetime_utc)

                    mail.append(timestamp)

            self.mark_delete_msg(i)

        return mail

    def mark_delete_msg(self, msg_id):
        """ Marks single email message for deletion """
        self.mailbox.store(msg_id, "+FLAGS", "\\Deleted")

    def is_ok(self, expected_from, expected_subject):
        """ Return true if has received OK email in last 12 minutes """
        for date in self.get_unseen_router_mail(expected_from, expected_subject):
            delay_seconds = 60 * DELAY_MINS
            now = time.mktime(time.gmtime())
            logger.debug(
                "Ok received {} minutes ago".format(s_to_min(now - date)))
            if (now - date) <= delay_seconds:
                return True
        logger.debug("Not OK")
        return False

    def send_alert(self):
        """ Send email alert """
        try:
            logger.info("*** Sending ALERT ***")
            msg = MIMEText("ALERT!!! POWER OUT!!!", "plain")
            msg['Subject'] = 'Power Outage in casa!'
            msg['From'] = self.__from_address
            msg['To'] = self.__to_address
            server = None
            server = smtplib.SMTP(self.__server, 587)
            server.starttls()
            server.login(self.__from_address, self.__pwd)
            server.sendmail(self.__from_address, [
                self.__to_address], msg.as_string())
            logger.debug("*** ALERT sent ***")
        except Exception, e:
            logger.critical(e)
        finally:
            if server:
                logger.debug("Server quitting...")
                server.quit()
                logger.debug("Server quit successful")
            else:
                logger.debug("No server to quit")


def print_all_dict(dictionary):
    """ Helper to print all dictionary K,V pairs.
        One per line printed to console """
    for k, v in dictionary.items():
        print("{}: {}".format(k, v))


def s_to_min(s):
    """ Convert milliseconds to minutes
        Return float """
    return round(float(s / 60.0), 1)


def toUTC(date, tz):
    """ Return date in local timezone to UTC """
    return tz.normalize(tz.localize(date)).astimezone(pytz.utc)
