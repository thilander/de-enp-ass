#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 0.1.0

# Copyright © 2016 Andreas Thilander <andreasthilander@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

import re, sys, os, csv


def get_item_title(item):
    return item.strip().split('\n')[0]


def get_item_part(item, part):
    """Returns a specific part of the item, like 'password'"""
    try:
        return re.findall('{} (.*?)\n'.format(part), '{}\n'.format(item),
                          re.IGNORECASE)[0]
    except IndexError:
        return ''


def get_item_notes(item):
    """Returns everything in the item that does not have a 'label'
        (like 'password' or 'username')
    """
    notes = '{}\n'.format('\n'.join(item.strip().split('\n')[1:]))
    notes = re.sub('password (.*?)\n', '', notes, flags=re.I)
    notes = re.sub('username (.*?)\n', '', notes, flags=re.I)
    notes = re.sub('email (.*?)\n', '', notes, flags=re.I)
    notes = re.sub('url (.*?)\n', '', notes, flags=re.I)
    notes = re.sub('label (.*?)\n', '', notes, flags=re.I)
    notes = re.sub('grouping: (.*?)\n', '', notes, flags=re.I)
    return notes


def to_password_item(item):
    """Returns a dict version of an item"""
    return {
        'title': get_item_title(item),
        'password': get_item_part(item, 'password'),
        'username': get_item_part(item, 'username'),
        'email': get_item_part(item, 'email'),
        'url': get_item_part(item, 'url'),
        'label': get_item_part(item, 'label'),
        'grouping': get_item_part(item, 'grouping:').lower(),
        'notes': get_item_notes(item)
    }


def normalized_groupings(file):
    """Normalize grouping
    In some cases the grouping value gets a new line...
    In some cases the grouping is not appended by a colon...
    In some cases grouping: is not appended by a space...
    Lets normalize that...
    """
    file = file.replace('\ngrouping ', '\ngrouping:')\
            .replace('\ngrouping:\n', '\ngrouping: ')\
            .replace('\ngrouping:', '\ngrouping: ')\
            .replace('\ngrouping:  ', '\ngrouping: ')\
            .replace('\ngrouping:\n', '\ngrouping: ')
    return file


def parse_credit_card(password):
    return {
        'title': password['title'],
        'card number': get_item_part(password['notes'], 'number'),
        'expiry date': get_item_part(password['notes'], 'expiry date'),
        'cardholder': get_item_part(password['notes'], 'cardholder'),
        'pin': get_item_part(password['notes'], 'pin'),
        'bank name': get_item_part(password['notes'], 'Issuing bank'),
        'CVV': get_item_part(password['notes'], 'CVC'),
        # it's harder to parse note so everything is included
        'notes': password['notes']
    }


def is_credit_card(password):
    return (get_item_part(password['notes'], 'cardholder') and
            get_item_part(password['notes'], 'type'))


def is_secure_note(password):
    return password['grouping'] == 'secure notes'


def is_login(password):
    return (not is_secure_note(password) and not is_credit_card(password))


def get_logins(passwords):
    return [{
        'title': p['title'],
        'URL': p['url'],
        'username': p['username'],
        'password': p['password'],
        'notes': p['notes'],
        'email': p['email'],
        'label': p['label']
    } for p in passwords if is_login(p)]


def get_secure_notes(passwords):
    return [{'title': p['title'], 'text': p['notes']}
            for p in passwords if is_secure_note(p)]


def get_credit_cards(passwords):
    p_cards = [p for p in passwords if is_credit_card(p)]
    return [parse_credit_card(p) for p in p_cards]


def write_csv_file(path, passwords, fieldnames):
    with open(path, 'w') as file:
        file.truncate()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(passwords)
        file.close()


def main(file_path):
    """Do all the things"""
    with open(file_path, 'r') as enpass_file:
        file = enpass_file.read().strip()
        file = normalized_groupings(file)
        items = file.split('\n\n')
        passwords = [to_password_item(item) for item in items]

        secure_notes = get_secure_notes(passwords)
        credit_cards = get_credit_cards(passwords)
        logins = get_logins(passwords)

        print('Found {} items:'.format(len(passwords)))
        print('{} logins'.format(len(logins)))
        print('{} credit cards'.format(len(credit_cards)))
        print('{} secure notes'.format(len(secure_notes)))

        file_name = os.path.splitext(file_path)[0]

        logins_path = '{}-logins.csv'.format(file_name)
        cc_path = '{}-credit-cards.csv'.format(file_name)
        notes_path = '{}-notes.csv'.format(file_name)

        write_csv_file(notes_path, secure_notes, ['title', 'text'])
        write_csv_file(cc_path, credit_cards, ['title', 'card number', 'expiry date',
                                               'cardholder', 'pin', 'bank name',
                                               'CVV', 'notes'])
        write_csv_file(logins_path, logins, ['title', 'URL', 'username', 'password',
                                             'notes', 'email', 'label'])
        print('conversion complete')
        enpass_file.close()


if __name__ == '__main__':
    main(sys.argv[1])
