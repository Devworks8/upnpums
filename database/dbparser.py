import os.path

from m3u8 import *
from m3u8_generator import *
from sqlite3.dbapi2 import *
from mutagen.id3 import ID3


class DbParser:
    def __init__(self, config):
        self.config = config
        self.db_path = config.get(header='database_path')[0][1] + "/catalog.db"
        self.data = self.__load_database()

    def __load_database(self):
        """
        Create database and cursor objects.
        :return: database object
        """
        if os.path.exists(self.db_path):
            data = connect(self.db_path)
            self.cursor = data.cursor()
        else:
            data = connect(self.db_path)
            self.cursor = data.cursor()
            self.__setup_database(data=data, cursor=self.cursor)
        return data

    def __setup_database(self, data, cursor):
        """
        Initial library setup.
        :param data: database object
        :param cursor: cursor object
        :return:
        """
        self.populate(data=data, cursor=cursor)

    def del_table(self, table):
        cursor = self.data.cursor()
        try:
            cursor.execute('''DROP TABLE {}'''.format(table))
            return

        except:
            print("{} table not found.".format(table))
            return

    def add_file(self, table, file=None):
        cursor = self.data.cursor()

        if file:
            query = """INSERT INTO {table} (name) VALUES ("{file}");""".format(table=table, file=file)
        else:
            query = """INSERT INTO {table} (name) VALUES ("file");""".format(table=table)

        cursor.execute(query)
        self.data.commit()

    def __db_key(self, root, parent):
        """
        Find the proper key based on the provided path.
        :param root: path string
        :param parent: parent directory bool
        :return: key string
        """
        if parent:
            return None

        elif len(root.split('/')) <= 2:
            return os.path.basename(root).replace(' ', '_')

        else:
            return root.split('/')[-2]

    def populate(self, data, cursor):
        """
        Dynamically create a database using the library directory structure.
        :param data: database object
        :param cursor: cursor object
        :return:
        """
        parent = True

        for root, dirs, files in os.walk(self.config.get('database_library')[0][1]):
            if parent:
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (group_id VARCHAR (15) PRIMARY KEY, id INTEGER, 
                category VARCHAR (15), title VARCHAR (30), duration TIME, format VARCHAR (10), artist VARCHAR (20), 
                released year, cover VARCHAR (20));'''.format(table=os.path.basename(root).replace(' ', '_'))

                cursor.execute(query_table)

                for d in dirs:
                    query_entry = '''INSERT INTO {table} (group_id, category) VALUES ("{group_id}", "{category}");
                    '''.format(table=os.path.basename(root).replace(' ', '_'), group_id=d.replace(' ', '_'),
                               category=os.path.basename(root))
                    cursor.execute(query_entry)

                for f in files:
                    if f[0] is not '.':
                        query_entry = '''INSERT INTO {table} (group_id, title, category) 
                        VALUES ("{group_id}", "{title}", "{category}");
                        '''.format(table=os.path.basename(root).replace(' ', '_'), title=f.replace(' ', '_'),
                                   group_id=f.replace(' ', '_'), category=os.path.basename(root))
                        cursor.execute(query_entry)

                parent = False
            else:
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (id INTEGER, group_id VARCHAR (15), 
                                     category VARCHAR (15), title VARCHAR (30) PRIMARY KEY, duration TIME, 
                                    format VARCHAR (10), artist VARCHAR (20), released year, cover VARCHAR (20),
                                    FOREIGN KEY (group_id) REFERENCES {group_id} (group_id));
                                    '''.format(table=os.path.basename(root).replace(' ', '_'),
                                               group_id=self.__db_key(root=root, parent=False))

                cursor.execute(query_table)

                for d in dirs:
                    query_link = '''INSERT INTO {table} (group_id, category) VALUES ("{group_id}", "{category}");
                    '''.format(table=os.path.basename(root).replace(' ', '_'),
                               group_id=self.__db_key(root=root, parent=False), category=d)

                    cursor.execute(query_link)

                for f in files:
                    if f[0] is not '.':
                        query_entry = '''INSERT INTO {table} (group_id, title, category) 
                        VALUES ("{group_id}", "{title}", "{category}");
                        '''.format(table=os.path.basename(root).replace(' ', '_'), title=f.replace(' ', '_'),
                                   group_id=self.__db_key(root=root, parent=False), category=os.path.basename(root))
                        cursor.execute(query_entry)

        data.commit()
        return

    def cleanup(self):
        """
        Close the database
        :return:
        """
        self.data.close()
