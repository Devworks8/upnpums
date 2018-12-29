import os.path

from m3u8 import *
from m3u8_generator import *
from sqlite3.dbapi2 import *
from sqlitedict import SqliteDict
from mutagen.id3 import ID3


class DbParser:
    def __init__(self, config):
        self.config = config
        self.db_path = config.get(header='database_path')[0][1] + "/catalog.db"
        self.data = self.populate(data=self.db_path)

    def __load_database(self):
        if os.path.exists(self.db_path):
            data = connect(self.db_path)
        else:
            data = connect(self.db_path)
            self.__setup_database(data=data, headers=self.__load_headers())
        return data

    def __setup_database(self, data, headers):
        cursor = data.cursor()
        self.populate(data=data, cursor=cursor)
        """
        count = 1
        for header in headers:
            cursor.execute(header[1])
            data.commit()
            query = '''INSERT INTO {table} (cat) VALUES ("{name}");'''.format(table=header[0], cat=header[0])
            cursor.execute(query)
            data.commit()
            count += 1

        data.commit()
        """

    def __load_headers(self):
        audio = """CREATE TABLE audio(id INTEGER PRIMARY KEY, name VARCHAR (10));"""
        video = """CREATE TABLE video(id INTEGER PRIMARY KEY, name VARCHAR (10));"""
        image = """CREATE TABLE image(id  PRIMARY KEY, name VARCHAR (10));"""

        headers = [('audio', audio), ('video', video), ('image', image)]
        return headers

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
        if parent:
            return None

        elif len(root.split('/')) <= 2:
            return os.path.basename(root).replace(' ', '_')

        else:
            return root.split('/')[-2]

    def populate(self, data):
        sqltable = SqliteDict(data, autocommit=True)
        for root, dirs, files in os.walk(self.config.get('database_library')[0][1]):
            sqltable[os.path.basename(root)] = None
        for f in files:
            if f[0] is not '.':
                sqltable[f] = None

        for key, value in sqltable.iteritems():
            print(key)
            print(value)

        return sqltable

    """

    def populate(self, data, cursor):
        parent = True

        for root, dirs, files in os.walk(self.config.get('database_library')[0][1]):
            if parent:
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (id INTEGER, pid VARCHAR (15) PRIMARY KEY, 
                title VARCHAR (30), duration TIME, format VARCHAR (10), artist VARCHAR (20), cat VARCHAR (15),
                released year, art VARCHAR (20));'''.format(table=os.path.basename(root).replace(' ', '_'))

                parent = False
            else:
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, pid VARCHAR (15), 
                                    title VARCHAR (30), duration TIME, format VARCHAR (10), artist VARCHAR (20), 
                                    released year, art VARCHAR (20), group_id INTEGER, cat VARCHAR (15),
                                    FOREIGN KEY (pid) REFERENCES {pid} (parent));'''.format(
                    table=os.path.basename(root).replace(' ', '_'), pid=self.__db_key(root=root, parent=parent))

            cursor.execute(query_table)

            for d in dirs:
                query_link = '''INSERT INTO {table} (pid, cat) VALUES ("{pid}", "{cat}");'''.format(
                    table=os.path.basename(root).replace(' ', '_'), pid=self.__db_key(root=root, parent=parent), cat=d)

                cursor.execute(query_link)

            for f in files:
                if f[0] is not '.':
                    query_entry = '''INSERT INTO {table} (pid, title) VALUES ("{pid}", "{title}");'''.format(
                        table=os.path.basename(root).replace(' ', '_'),
                        title=f.replace(' ', '_'), pid=self.__db_key(root=root, parent=parent))
                    cursor.execute(query_entry)

        data.commit()
        return

    """

    def list_files(self, startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

    def cleanup(self):
        """
        Close the database
        :return:
        """
        self.data.close()
