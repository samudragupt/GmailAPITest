# GmailAPITest

Step 1 : Create a virtual environment and enter into it
python -m venv GmailAPITest
source GmailAPITest/bin/activate
Result : Virtual Environment would have been created. You will have (GmailAPITest) in the beginning with the parenthesis.

Step2 : Install simplegmail
pip3 install simplegmail

Step3 : Run add_mails_to_db.py which will ask authentication from your gmail to read mails, and then create a db to store all the mails in last 15 days.
python3 add_mails_to_db.py
Allow permissions from your email-id to read mail.
Result: Two new files gmail_token.json and emails.db would have been created. emails.db stores all the emails that you had in last 15 days.

Step4: Run apply_rules.py to filter the mails from your db and take action on email-id according to the rules.json.
python3 apply_rules.py

You can add your own rules to rules.json to add your new rules.
 
