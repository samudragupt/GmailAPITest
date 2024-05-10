import sqlite3
from helper import GmailManagerHelper


def add_mails_to_db(conn, cursor, messages):
    """
    Adds the mail p
    :param conn: connection to the emails database
    :param cursor: cursor the emails database
    :param messages: the emails needed to add to the database
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            recipient TEXT,
            cc TEXT,
            bcc TEXT,
            subject TEXT,
            date DATETIME,
            body TEXT,
            label TEXT
        );''')
    mails_added = 0
    duplicate_mail_id = []
    for message in messages:
        message_id = message.id
        message_sender = message.sender
        message_recipient = message.recipient
        message_cc = ','.join([cc for cc in message.cc])
        message_bcc = ','.join([bcc for bcc in message.bcc])
        message_subject = message.subject
        message_date = GmailManagerHelper().parse_date(message.date)
        message_plain = message.plain
        label_id_str = ','.join([label.id for label in message.label_ids])
        try:
            cursor.execute('''INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (message_id, message_sender, message_recipient, message_cc,
                            message_bcc, message_subject, message_date, message_plain,
                            label_id_str))
            mails_added = mails_added + 1
        except sqlite3.IntegrityError:
            duplicate_mail_id.append(message_id)
        except Exception as e:
            print(e)
    print(f"successfully added {mails_added} mails to DB")
    if len(duplicate_mail_id) != 0:
        print(f"These mails already exist in DB: {duplicate_mail_id}")
    conn.commit()


if __name__ == "__main__":
    mails = GmailManagerHelper().get_mails(days=15)
    db_conn, db_cursor = GmailManagerHelper().get_connection_to_db()
    add_mails_to_db(db_conn, db_cursor, mails)
