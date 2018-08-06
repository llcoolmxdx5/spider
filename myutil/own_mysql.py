import pymysql

class OwnMySQL:
    def __init__(self, host='localhost', user='root',
                 password='123456', port=3306, db=None):
        self.db = pymysql.connect(host=host, user=user,
                  password=password, port=port, db=db)
        self.cursor = self.db.cursor()
    
    def __del__(self):
        self.db.close()
        
    def create_db(self, db):
        '''
        :params: db
        :return:
        '''
        params = (db,)
        sql = 'CREATE DATABASE %s DEFAULT CHARACTER SET utf8'
        self.cursor.execute(sql, params)
        self.use_db(db)
     
    def use_db(self, db):
        sql = 'USE {db}'.format(db=db)
        self.cursor.execute(sql)

    def create_table(self, sql):
        self.cursor.execute(sql)
    
    def insert_data(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'\
              .format(table=table, keys=keys, values=values)
        try:
            if self.cursor.execute(sql, tuple(data.values())):
                self.db.commit()
        except:
            self.db.rollback()
            raise
    
    def update_data(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) \
               ON DUPLICATE KEY UPDATE'.format(table=table, 
                                               keys=keys, 
                                               values=values)
        update = ','.join(['{key}=%s'.format(key=key) for key in data])
        sql += update
        try: 
            if self.cursor.execute(sql, tuple(data.values())*2):
                self.db.commit()
        except:
            self.db.rollback()
            raise
    
    def delete_data(self, table, condition):
        sql = 'DELETE FROM {table} WHERE {condition}'\
              .format(table=table, condition=condition)
        try:
            self.cursor.execute(sql)
        except:
            self.db.rollback()
            raise
 
    def select_data(self, sql, params):
        return self.cursor.execute(sql, params)
    
    def drop_table(self, table):
        sql = 'DROP TABLE %s'
        try:
            self.cursor.execute(sql, tuple(table))
        except:
            self.db.rollback()
            raise
    
    def other_handle(self):
        return self.cursor
