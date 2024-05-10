import sqlite3
from datetime import datetime
from simplegmail import Gmail
from simplegmail.query import construct_query


class GmailManagerHelper:
    def __init__(self):
        self.conn, self.cursor = self.get_connection_to_db()
        self.gmail = Gmail()

    def get_connection_to_db(self):
        """
        Creates a connection to the emails database
        :return: cursor of the database
        """
        # Connecting to the database
        conn = sqlite3.connect('emails.db')
        cursor = conn.cursor()
        return conn, cursor

    def parse_date(self, date_str):
        """
        converts date into a specified format to store date in the db
        :param date_str: date in 2024-05-08 14:15:34+05:30 or Tue, 7 May 2024 19:31:12 +0530 (GMT+05:30) format
        :return: date in 2024-05-08 14:15:34 format
        """
        date_str = date_str.split('(')[0].strip()
        date_formats = [
            '%Y-%m-%d %H:%M:%S%z',  # Format: 2024-05-08 14:15:34+05:30
            '%a, %d %b %Y %H:%M:%S %z',  # Format: Tue, 7 May 2024 19:31:12 +0530
            # Add more date formats here as needed
        ]
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass  # Try the next format
        raise ValueError("Unable to parse date string: {}".format(date_str))

    def get_mails(self, days=365):
        """
        Function to return mails from gmail
        :param days: number of days for which mail is needed
        :return: returns all the mails from past days
        """
        query_params = {"newer_than": (days, "day")}
        messages = self.gmail.get_messages(query=construct_query(query_params))
        return messages

    def close_connection(self):
        """
        Closes the connection to the database
        """
        self.conn.close()
