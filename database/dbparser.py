import os.path

from m3u8 import *
from m3u8_generator import *
from sqlite3.dbapi2 import *
from mutagen import *


class DbParser:
    def __init__(self, config):
        self._config = config
        self.data = self.__load_database()

    def __load_database(self):
        db_path = self._config.get(header='database_path')[0][1] + "/catalog"
        if os.path.exists(db_path):
            data = connect(db_path)
        else:
            data = connect(db_path)
            self.__setup_database(data=data, headers=self.__load_headers())
        return data

    def __setup_database(self, data, headers):
        pass

    def __load_headers(self):
        headers = """
        CREATE TABLE 
        """
        return headers

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
