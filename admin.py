import argparse

from tinydb import Query, TinyDB
from model import update_status, update_status_and_token
from utils import send_email


def send_email_to_status_0():
    db = TinyDB("data.json")
    People = Query()
    target_users = db.search(People.status == 1)
    print('there are %s target_users' % len(target_users))
    for user in target_users:
        update_status(user['email'], 0)
    print('all done')
    db.close()


def count_status():
    db = TinyDB("data.json")
    People = Query()
    for i in range(5):
        c = db.count(People.status == i)
        print('status', i, 'have', c, 'people')
    db.close()


def change_status_to_0():
    db = TinyDB("data.json")
    People = Query()
    target_users = db.search(People.status.one_of([2, 3]))
    for user in target_users:
        update_status(user['email'], 0)
    db.close()


def search_by_email(email):
    db = TinyDB("data.json")
    People = Query()
    target_user = db.search(People.email.matches('.*%s.*' % email))
    for user in target_user:
        print(user)
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', default='search_by_email', choices=['search_by_email', 'reset_status'])
    parser.add_argument('email')
    args = parser.parse_args()
    if args.action == 'search_by_email':
        search_by_email(args.email)
    elif args.action == 'reset_status':
        update_status(args.email, status=0)
    else:
    # change_status_to_0()
    # search_by_email('')
    # search_by_email('')
    # emails = ('vincentchon77@yahoo.com', )
    # for i in emails:
    #     update_status(i, 0)
        count_status()


