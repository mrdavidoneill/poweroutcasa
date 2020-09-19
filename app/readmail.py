import smtplib
import time
import imaplib
import email
import time
from email.mime.text import MIMEText
from datetime import datetime


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
        print("Closing...")
        self.mailbox.close()
        print("Mailbox closed")
        self.mailbox.logout()
        print("Mailbox logged out")

    def login(self):
        try:
            self.mailbox = imaplib.IMAP4_SSL(self.__server)
            self.mailbox.login(self.__from_address, self.__pwd)
            self.mailbox.select('inbox')
            return True
        except Exception, e:
            print str(e)
            return False

    def get_unseen_router_mail(self, expected_from, expected_subject):
        """ Retrieves mail from mailbox """
        mail = []
        typ, data = self.mailbox.search(None, "UNSEEN")
        mail_ids = data[0]
        id_list = mail_ids.split()

        for i in reversed(id_list[-2:-1]):
            typ, data = self.mailbox.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    date = msg['date']
                    date = email.utils.parsedate(date)

                    if email_subject != expected_subject:
                        continue
                    if email_from != expected_from:
                        continue

                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
                    # print 'Date : ' + date + '\n'
                    print(date)

                    mail.append(time.mktime(date))
        return mail

    def is_ok(self, expected_from, expected_subject):
        """ Return true if has received OK email in last 12 minutes """
        for date in self.get_unseen_router_mail(expected_from, expected_subject):
            twelve_min = 1000 * 60 * 12
            now = time.time()
            print(date)
            print(now)
            print((now - date) <= twelve_min)
            print(ms_to_min(now - date))
            if (now - date) <= twelve_min:
                return True
        return False

    def send_alert(self):
        """ Send email alert """
        try:
            print("*** Sending ALERT ***")
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
            print("*** ALERT sent ***")
        except Exception, e:
            print(e)
        finally:
            if server:
                server.quit()


def print_all_dict(dictionary):
    for k, v in dictionary.items():
        print("{}: {}".format(k, v))


def ms_to_min(ms):
    """ Convert milliseconds to minutes 
        Return float
    """
    return float(ms / 1000.0 / 60.0)
