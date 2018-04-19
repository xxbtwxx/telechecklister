from obj.dal import Dal

db = Dal()

class ListController:

    chat_id = -1

    def __init__(self, chat_id, list_name = ''):
        self.chat_id = chat_id

    def get_list_names(self):

        query = '''SELECT `list_name`
                   FROM `tydi$teleBot`.`lists`
                   WHERE `chat_id` = %s'''

        db.connect()
        lists = db.get_table(query, (self.chat_id,))
        db.disconnect()

        return lists

    def list_exist(self, list_name):
        if list_name not in [x[0] for x in self.get_list_names()]:
            return False
        return True

    def item_in_list(self, list_name, item_name):
        if item_name not in [x[0] for x in self.get_list_items(list_name)]:
            return False
        return True

    def check_item(self, list_name, item_name):
        if self.item_in_list(list_name, item_name) == False:
            return False

        query = '''UPDATE `tydi$teleBot`.`items`
                   SET `checked` = 1
                   WHERE `chat_id` = %s
                   AND `list_name` = %s
                   AND `item` = %s'''
        params = (self.chat_id, list_name, item_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True

    def uncheck_item(self, list_name, item_name):
        if self.item_in_list(list_name, item_name) == False:
            return False

        query = '''UPDATE `tydi$teleBot`.`items`
                   SET `checked` = 0
                   WHERE `chat_id` = %s
                   AND `list_name` = %s
                   AND `item` = %s'''
        params = (self.chat_id, list_name, item_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True

    def delete_item(self, list_name, item_name):
        if self.item_in_list(list_name, item_name) == False:
            return False

        query = '''DELETE FROM `tydi$teleBot`.`items`
                   WHERE `chat_id` = %s
                   AND `list_name` = %s
                   AND `item` = %s'''
        params = (self.chat_id, list_name, item_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True


    def create_list(self, list_name):
        if self.list_exist(list_name)  == True:
            return False

        query = '''INSERT INTO
                   `tydi$teleBot`.`lists`
                   (`chat_id`, `list_name`)
                   VALUES (%s, %s)'''
        params = (self.chat_id, list_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True

    def list_completeness(self, list_name = ''):
        if list_name == '':
            return '0/0'

        items_count = list(self.get_items_count(list_name))

        out = str(items_count[0]) + '/' + str(items_count[2])
        return out


    def delete_list(self, list_name):

        if self.list_exist(list_name) == False:
            return False

        query_items = '''DELETE FROM `tydi$teleBot`.`items`
                         WHERE `chat_id` = %s
                         AND `list_name` = %s'''
        query_list = '''DELETE FROM `tydi$teleBot`.`lists`
                        WHERE `chat_id` = %s
                        AND `list_name` = %s'''

        params = (self.chat_id, list_name)

        db.connect()
        db.execute(query_items, params)
        db.execute(query_list, params)
        db.disconnect()

        return True

    def get_items_count(self, list_name = ''):
        if list_name == '':
            return [0, 0, 0]

        query = '''SELECT 
        ( 
            SELECT COUNT(*) 
            FROM `tydi$teleBot`.`items` 
            WHERE`checked` = 1
            AND `chat_id` = %s
            AND `list_name` = %s
        ) AS `checked`, 
        ( 
            SELECT COUNT(*) 
            FROM `tydi$teleBot`.`items` 
            WHERE `checked` = 0
            AND `chat_id` = %s
            AND `list_name` = %s
        ) AS `unchecked`, 
        (   
            SELECT
            (`checked` + `unchecked`)
        ) AS `total`'''

        params = (self.chat_id, list_name, self.chat_id, list_name)

        db.connect()
        stats = db.get_row(query, params)
        db.disconnect()

        return stats

    def get_list_items(self, list_name, mode='all'):

        if self.list_exist(list_name) == False:
            return []

        query = '''SELECT `item`, `checked`
                   FROM `tydi$teleBot`.`items`
                   WHERE `chat_id` = %s
                   AND `list_name` = %s
                '''
        if mode == 'checked':
            query += 'AND `checked` = 1'
        elif mode == 'unchecked':
            query += 'AND `checked` = 0'

        params = (self.chat_id, list_name)

        db.connect()
        result = db.get_table(query, params)
        db.disconnect()
        return result

    def add_to_list(self, list_name, item_name):
        if self.list_exist(list_name) == False:
            return False

        if self.item_in_list(list_name, item_name) == True:
            return False

        query = '''INSERT INTO
                   `tydi$teleBot`.`items`
                   (`chat_id`, `list_name`, `item`)
                   VALUES (%s, %s, %s)'''
        params = (self.chat_id, list_name, item_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True

    def delete_from_list(self, list_name, item_name):
        if self.list_exist(list_name) == False:
            return False

        if self.item_in_list(list_name, item_name) == False:
            return False

        query = '''DELETE FROM `tydi$teleBot`.`items`
                   WHERE `chat_id` = %s
                   AND `list_name` = %s
                   AND `item` = %s'''
        params = (self.chat_id, list_name, item_name)

        db.connect()
        db.execute(query, params)
        db.disconnect()

        return True

