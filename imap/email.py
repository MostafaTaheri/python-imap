import email
import imaplib
import logging
from datetime import datetime, timedelta


class Email:
    """Operations of email.

    You can read all emails and fetch the contents
    and another operations.

    Example:
        email = Email()
        email.read()
    """

    def __init__(self, handler: dict):
        """Defines and set value for variables.

        Parameters:
            self.hostname: The name of host.
            self.username: Then username of email.
            self.password: The password of email.
            self.port: The port number of host.
            self.select: The name of selected part. ex: inbox.
            self.flag: Can be contain UNSEEN, SEEN and ALL.
            self.handler: Contains the information of configuration.
            self.since: Filters email based on date
        """
        self.hostname = handler.get('hostname')
        self.username = handler.get('username')
        self.password = handler.get('password')
        self.port = handler.get('port')
        self.select = handler.get('select')
        self.flag = handler.get('flag')
        self.handler = handler
        self.since = (datetime.today() - timedelta(1)).strftime("%d-%b-%Y")

    def read(self):
        """Reads all emails.

        Returns:
            The list of email contents.
        """
        try:
            self.mail = imaplib.IMAP4_SSL(self.hostname, self.port)
            self.mail.login(self.username, self.password)
            return  self._read()
        except Exception as Exp:
            logging.exception(Exp)
        return 0

    def _read(self) -> list:
        """Reads all emails and get attachments.

        Returns:
            The list of email contents.
        """
        self.mail.list()
        self.mail.select(self.select)
        self.filter = '(SINCE "' + self.since + '")' if self.handler[
                                                       'search'] == 'SINCE' else None

        self.result, self.data = self.mail.uid('search', self.filter,
                                               self.flag)
        self.uids = self.data[0].split()
        self.attachments = []

        for uid in self.uids:
            self.result, self.email_data = self.mail.uid(
                'fetch', uid, '(RFC822)')
            self.raw_email = self.email_data[0][1]
            self.raw_email_string = self.raw_email.decode('utf-8')
            self.parsed_email = email.message_from_bytes(self.raw_email)

            for part in self.parsed_email.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_content_type() not in ['text/html', 'text/plain']:
                    self.attachments.append({
                        'name':
                            part.get_filename(),
                        'content_type':
                            part.get_content_type(),
                        'bytes':
                            part.get_payload(decode=True)
                    })

            self.content.append({
                'from':
                    self.parsed_email['From'],
                'to':
                    self.parsed_email['To'],
                'cc':
                    self.parsed_email['CC'],
                'attachments':
                    self.attachments,
                'subject':
                    str(
                        email.header.make_header(
                            email.header.decode_header(self.parsed_email['Subject'])))
            })
        return self.content
