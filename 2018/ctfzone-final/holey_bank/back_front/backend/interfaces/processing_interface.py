from mysql.connector import MySQLConnection, Error
from var.messages import ERROR_OK

from var.network import PROCESSING_HOST, PROCESSING_PORT, PROCESSING_DATABASE, PROCESSING_USER, PROCESSING_PASSWORD


class ProcessingInterface:
    def __init__(self):
        self.__creds = {'host': PROCESSING_HOST,
                        'port': PROCESSING_PORT,
                        'database': PROCESSING_DATABASE,
                        'user': PROCESSING_USER,
                        'password': PROCESSING_PASSWORD}

    # create account
    def create_account(self, args):
        try:
            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            result = cursor.callproc('Create_Account', (args['passport'], 0, 0))

            if result[1] > 0:
                conn.commit()
            else:
                conn.rollback()

            response = result[1] > 0
            message = result[2]

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.create_account()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.create_account()')
            return response, message

    # create card
    def create_card(self, args):
        try:
            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            result = cursor.callproc('Create_Card', (args['passport'], 0, 0))

            if result[1] > 0:
                conn.commit()
            else:
                conn.rollback()

            response = result[1] > 0
            message = result[2]

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.create_card()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.create_card()')
            return response, message

    # a2a transaction
    def a2a(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT account from Bank_Accounts WHERE client = %s', (passport,))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]

                cursor.execute('INSERT INTO Transactions (from_, to_, transfer_type, transfer_comment, sum) VALUES (%s, %s, %s, %s, %s)',
                               (account_id,
                                args['to'],
                                'a2a',
                                args['comment'],
                                args['sum'],))

                conn.commit()
                response = True
                message = ERROR_OK

            else:
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.a2a()'

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.a2a()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.a2a()')
            return response, message

    # a2c transaction
    def a2c(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT account from Bank_Accounts WHERE client = %s', (passport,))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]

                cursor.execute('INSERT INTO Transactions (from_, to_, transfer_type, transfer_comment, sum) VALUES (%s, %s, %s, %s, %s)',
                               (account_id,
                                args['to'],
                                'a2c',
                                args['comment'],
                                args['sum'],))

                conn.commit()
                response = True
                message = ERROR_OK

            else:
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.a2c()'

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.a2c()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.a2c()')
            return response, message

    # c2a transaction
    def c2a(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT account from Bank_Accounts WHERE client = %s', (passport,))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]

                cursor.execute(
                    'INSERT INTO Transactions (from_, to_, transfer_type, transfer_comment, sum) VALUES (%s, %s, %s, %s, %s)',
                    (args['from'],
                     account_id,
                     'c2a',
                     args['comment'],
                     args['sum'],))

                conn.commit()
                response = True
                message = ERROR_OK

            else:
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.c2a()'

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.c2a()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.c2a()')
            return response, message

    # c2c transaction
    def c2c(self, args):
        try:
            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO Transactions (from_, to_, transfer_type, transfer_comment, sum) VALUES (%s, %s, %s, %s, %s)',
                (args['from'],
                 args['to'],
                 'c2c',
                 args['comment'],
                 args['sum'],))

            conn.commit()
            response = True
            message = ERROR_OK

            cursor.close()
            conn.close()
            return response, message

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.c2c()')
            return response, message

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.c2c()')
            return response, message

    # get cards and account info
    def get_info(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT id, account, balance, date from Bank_Accounts WHERE client = %s', (passport,))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]
                account_info = {'id': row[1],
                                'balance': row[2],
                                'create_date': str(row[3])}

                cursor.execute('SELECT card, card_limit, card_balance, date from Bank_Cards WHERE account_id = %s ORDER BY date', (account_id,))
                rows = cursor.fetchall()

                cards_info = []
                for row in rows:
                    cards_info.append({'id': row[0],
                                       'limit': row[1],
                                       'balance': row[2],
                                       'create_date': str(row[3])})

                result = {'account': account_info, 'cards': cards_info}
                response = True
                message = ERROR_OK

            else:
                result = {}
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.get_info()'

            cursor.close()
            conn.close()
            return response, message, result

        except Error as e:
            result = {}
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.get_info()')
            return response, message, result

        except Exception as ex:
            result = {}
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.get_info()')
            return response, message, result

    # get cards history
    # @deprecated
    def get_cards_history(self, args):
        try:
            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()

            cursor.execute('SELECT id from Bank_Accounts WHERE client = %s', (args['passport'],))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]

                cardlist = args['cards'].split(',')
                for card in cardlist:
                    cursor.execute('SELECT account_id from Bank_Cards WHERE card = %s', (card,))
                    row = cursor.fetchone()

                    if row is None:
                        continue

                    if row[0] != account_id:
                        raise Exception('User has no permissions to get history for card "{0}"'.format(card))

                cursor.callproc('Get_Cards_Transaction_History', (args['cards'],))

                result = []
                for res in cursor.stored_results():
                    result += res

                cursor.close()
                conn.close()

                data = []
                for row in result:
                    data.append({'from': row[0],
                                 'to': row[1],
                                 'type': row[2],
                                 'comment': row[3],
                                 'date': str(row[4]),
                                 'sum': row[5]})

                response = True
                message = ERROR_OK

            else:
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.get_cards_history()'
                data = None

            return response, message, data

        except Error as e:
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.get_cards_history()')
            return response, message, None

        except Exception as ex:
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.get_cards_history()')
            return response, message, None

    # get cards and account history
    def get_history(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT id, account, balance, date from Bank_Accounts WHERE client = %s', (passport,))
            row = cursor.fetchone()

            if row is not None:
                account_id = row[0]
                account_info = {'id': row[1],
                                'balance': row[2],
                                'create_date': str(row[3])}

                cursor.execute('SELECT from_, to_, transfer_type, date, transfer_comment, sum from Transactions WHERE (from_ = %s OR to_ = %s) ORDER BY date',
                               (account_info['id'], account_info['id'],))

                rows = cursor.fetchall()
                history = []
                for row in rows:
                    if row[0] == account_info['id']:
                        direction = 'OUT'
                        target = row[1]
                    else:
                        direction = 'IN'
                        target = row[0]
                    history.append({'direction': direction,
                                    'target': target,
                                    'type': row[2],
                                    'date': str(row[3]),
                                    'comment': row[4],
                                    'sum': row[5]})

                account_info['history'] = history

                cursor.execute('SELECT card, card_limit, card_balance, date from Bank_Cards WHERE account_id = %s', (account_id,))
                rows = cursor.fetchall()

                cards_info = []
                for row in rows:
                    cursor.execute('SELECT from_, to_, transfer_type, date, transfer_comment, sum from Transactions WHERE (from_ = %s OR to_ = %s) ORDER BY date',
                                   (row[0], row[0],))

                    card_history = cursor.fetchall()
                    history = []
                    for card_history_item in card_history:
                        if card_history_item[0] == row[0]:
                            direction = 'OUT'
                            target = card_history_item[1]
                        else:
                            direction = 'IN'
                            target = card_history_item[0]
                        history.append({'direction': direction,
                                        'target': target,
                                        'type': card_history_item[2],
                                        'date': str(card_history_item[3]),
                                        'comment': card_history_item[4],
                                        'sum': card_history_item[5]})

                    cards_info.append({'id': row[0],
                                       'limit': row[1],
                                       'balance': row[2],
                                       'create_date': str(row[3]),
                                       'history': history})

                result = {'account': account_info, 'cards': cards_info}
                response = True
                message = ERROR_OK

            else:
                result = {}
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.get_history()'

            cursor.close()
            conn.close()
            return response, message, result

        except Error as e:
            result = {}
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.get_history()')
            return response, message, result

        except Exception as ex:
            result = {}
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.get_history()')
            return response, message, result

    # get plain cards and account history
    def get_full_history(self, args):
        try:
            passport = args['passport']

            conn = MySQLConnection(**self.__creds)
            cursor = conn.cursor()
            cursor.execute('SELECT id, account from Bank_Accounts WHERE client = %s', (passport,))
            res = cursor.fetchone()

            if res is not None:
                account_id = res[0]
                account_num = res[1]

                cursor.execute('SELECT card from Bank_Cards WHERE account_id = %s', (account_id,))
                rows = cursor.fetchall()

                ids = [account_num]
                for row in rows:
                    ids.append(row[0])

                format_strings = ','.join(['%s'] * len(ids))
                cursor.execute('SELECT from_, to_, transfer_type, date, transfer_comment, sum from Transactions WHERE (from_ IN (%s) OR to_ IN (%s)) ORDER BY date'
                               % (format_strings, format_strings),
                               tuple(ids + ids))

                rows = cursor.fetchall()
                history = []
                for row in rows:
                    history.append({'from': row[0],
                                    'to': row[1],
                                    'type': row[2],
                                    'date': str(row[3]),
                                    'comment': row[4],
                                    'sum': row[5]})

                result = {'history': history}
                response = True
                message = ERROR_OK

            else:
                result = {}
                response = False
                message = 'Error: no account with such passport in processing database at ProcessingInterface.get_full_history()'

            cursor.close()
            conn.close()
            return response, message, result

        except Error as e:
            result = {}
            response = False
            message = 'Error: {0} at {1}'.format(str(e), 'ProcessingInterface.get_full_history()')
            return response, message, result

        except Exception as ex:
            result = {}
            response = False
            message = 'Exception: {0} at {1}'.format(str(ex), 'ProcessingInterface.get_full_history()')
            return response, message, result
