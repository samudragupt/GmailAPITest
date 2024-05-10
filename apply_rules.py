import json
from helper import GmailManagerHelper


def filter_mail_id_from_db(cursor, query):
    """
    Filters all mail id from db with the given query
    :param cursor: cursor to the database on which query is to be performed
    :param query: query to be performed on the database
    :return: all the mail_id who got filtered by the query
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    mail_ids = []
    for row in rows:
        mail_ids.append(row[0])
    return mail_ids


def apply_actions_on_mail(mail_ids, action):
    """
    Function to apply action on mails present in the gmail
    :param mail_ids: All the mail id on which the action is to be taken
    :param action: The action which is to be performed on the mail ids
    """
    messages = GmailManagerHelper().get_mails(days=15)
    missed_mail_id = []
    updated_mails = 0
    for message in messages:
        if message.id in mail_ids:
            try:
                if action["type"] == "mark as read":
                    message.mark_as_read()
                elif action["type"] == "mark as unread":
                    print(message.subject)
                    message.mark_as_unread()
                elif action["type"] == "move to":
                    if action["move_to"] == "inbox":
                        message.move_to_inbox()
                    elif action["move_to"] == "archive":
                        message.archive()
                    elif action["move_to"] == "trash":
                        message.trash()
                    elif action["move_to"] == "untrash":
                        message.untrash()
                updated_mails += 1
            except Exception as e:
                missed_mail_id.append(message.id)
                pass

    print(f"Updated {updated_mails} mails")
    if len(missed_mail_id) != 0:
        print(f"Unable to update - {missed_mail_id}")


def get_rules():
    """
    Read the rules in rules.json
    :return: the rules in dictionary format
    """
    with open("rules.json", "r") as file:
        data = json.load(file)
    return data


def construct_db_search_query(rule):
    """
    Constructs the DB query based on the rule
    :param rule: Rule on which the query is to be performed
    :return: the query made on the basis of rules
    """
    query = ""
    predicates = ['sender', 'recipient', 'cc', 'bcc']
    for predicate in predicates:
        if rule['predicate'][predicate]['id']:
            if query == "":
                query = "WHERE "
            else:
                query += "AND "
            type = "LIKE" if rule['predicate'][predicate]['type'] == 'contains' else "="
            operator = "%" if rule['predicate'][predicate]['type'] == 'contains' else ""
            query += f'({predicate} {type} "{operator}' + f'{operator}" OR {predicate} {type} "{operator}'.join(
                rule['predicate'][predicate]['id']) + f'{operator}") '
    date_from = rule['predicate']['date_recieved']['from']
    date_to = rule['predicate']['date_recieved']['to']
    date_from = date_from if date_from != -1 else 36500
    date_to = date_to if date_to != -1 else 0
    query += f'AND date >= date("now", "-{date_from} days") '
    query += f'AND date < date("now", "-{date_to} days") '
    return "SELECT id from emails " + query + ";"


if __name__ == "__main__":
    db_conn, db_cursor = GmailManagerHelper().get_connection_to_db()
    all_rules = get_rules()
    for rules in all_rules:
        sql_query = construct_db_search_query(rules)
        mail_id_list = filter_mail_id_from_db(db_cursor, sql_query)
        apply_actions_on_mail(mail_id_list, rules['action'])
