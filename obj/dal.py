from static import cfg
import mysql.connector

class Dal:
    cnx = ''

    def connect(self):
        self.cnx = mysql.connector.connect(**cfg.db_cfg[cfg.env])

    def disconnect(self):
        self.cnx.close()

    def get_table(self, query, params = ''):
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, params)

        res = cursor.fetchall()

        cursor.close()

        return res

    def get_row(self, query, params = ''):
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, params)

        res = cursor.fetchmany(size = 1)

        cursor.close()

        return res[0]

    def execute(self, query, params = ''):
        cursor = self.cnx.cursor(buffered=True)
        
        cursor.execute(query, params)

        lRow = cursor.lastrowid

        cursor.close()

        self.cnx.commit()

        return lRow