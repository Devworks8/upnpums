import os.path
import sndhdr
import audioread

import multitasking
from m3u8 import *
from m3u8_generator import *
from sqlite3.dbapi2 import *
from mutagen.id3 import ID3
from datetime import timedelta


# TODO: Finish error handling.
class DbParser:
    def __init__(self, config):
        self.config = config
        self.db_path = config.get(header='database_path')[0][1]
        self.data = self.__load_database()

    @multitasking.task
    def __load_database(self):
        """
        Create database and cursor objects.
        :return: database object
        """
        if os.path.exists(os.path.join(self.db_path, "CATALOG")):
            data = connect(os.path.join(self.db_path, "CATALOG"))
            self.cursor = data.cursor()
        else:
            try:
                os.mkdir(self.db_path)
            except:
                pass

            data = connect(os.path.join(self.db_path, "CATALOG"))
            self.cursor = data.cursor()
            return self.__setup_database(data=data, cursor=self.cursor)

    def __setup_database(self, data, cursor):
        """
        Initial library setup.
        :param data: database object
        :param cursor: cursor object
        :return:
        """
        # self.taskmanager.add_thread(self.populate, (data, cursor,))
        # self.taskmanager.start('populate')
        return self.populate(data=data, cursor=cursor)

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

    def __validate_string(self, string):
        """
        Removes all invalid characters for sql injection.
        :param string: String
        :return: String
        """
        restricted = {'': ['#'], '_': [' ', '-']}
        results = string

        for k, v in restricted.items():
            for char in v:
                results = results.replace(char, k)

        return results

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
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (group_id VARCHAR (50) PRIMARY KEY, id INTEGER, 
                category VARCHAR (50), title VARCHAR (30), duration TIME, format VARCHAR (10), artist VARCHAR (20), 
                released year, cover VARCHAR (20), frame_rate DOUBLE, channels INTEGER, 
                total_frames DOUBLE, sample_width INTEGER, path VARCHAR (50));
                '''.format(table=self.__validate_string(os.path.basename(root)))

                cursor.execute(query_table)

                for d in dirs:
                    query_entry = '''INSERT INTO {table} (group_id, category) VALUES ("{group_id}", "{category}");
                    '''.format(table=self.__validate_string(os.path.basename(root)),
                               group_id=self.__validate_string(d),
                               category=self.__validate_string(os.path.basename(root)))
                    cursor.execute(query_entry)

                for f in files:
                    if f[0] is not '.':
                        query_entry = '''INSERT INTO {table} (group_id, title, category, duration, format, frame_rate, 
                        channels, total_frames, sample_width, path) 
                        VALUES ("{group_id}", "{title}", "{category}",  "{duration}", "{format}", "{frame_rate}", 
                        "{channels}", "{total_frames}", "{sample_width}", "{path}");
                        '''.format(table=self.__validate_string(os.path.basename(root)),
                                   title=self.__validate_string(f),
                                   group_id=self.__validate_string(f),
                                   category=self.__validate_string(os.path.basename(root)),
                                   duration=self.fetch_tags(root=root, file=f, field='duration'),
                                   format=self.fetch_tags(root=root, file=f, field='filetype'),
                                   frame_rate=self.fetch_tags(root=root, file=f, field='framerate'),
                                   channels=self.fetch_tags(root=root, file=f, field='nchannels'),
                                   total_frames=self.fetch_tags(root=root, file=f, field='nframes'),
                                   sample_width=self.fetch_tags(root=root, file=f, field='sampwidth'),
                                   path=os.path.join(root, f))
                        cursor.execute(query_entry)

                parent = False
            else:
                query_table = '''CREATE TABLE IF NOT EXISTS {table} (id INTEGER, group_id VARCHAR (50), 
                                     category VARCHAR (50), title VARCHAR (30) PRIMARY KEY, duration TIME, 
                                    format VARCHAR (10), artist VARCHAR (20), released year, cover VARCHAR (20), 
                                    frame_rate DOUBLE, channels INTEGER, total_frames DOUBLE, sample_width INTEGER, 
                                    path VARCHAR (50),
                                    FOREIGN KEY (group_id) REFERENCES {group_id} (group_id));
                                    '''.format(table=self.__validate_string(os.path.basename(root)),
                                               group_id=self.__validate_string(self.__db_key(root=root, parent=False)))

                cursor.execute(query_table)

                for d in dirs:
                    query_link = '''INSERT INTO {table} (group_id, category) VALUES ("{group_id}", "{category}");
                    '''.format(table=self.__validate_string(os.path.basename(root)),
                               group_id=self.__validate_string(self.__db_key(root=root, parent=False)),
                               category=self.__validate_string(d))

                    cursor.execute(query_link)

                for f in files:
                    if f[0] is not '.':
                        query_entry = '''INSERT INTO {table} (group_id, title, category, duration, format, frame_rate, 
                        channels, total_frames, sample_width, path) 
                        VALUES ("{group_id}", "{title}", "{category}", "{duration}", "{format}", "{frame_rate}", 
                        "{channels}", "{total_frames}", "{sample_width}", "{path}");
                        '''.format(table=self.__validate_string(os.path.basename(root)),
                                   title=self.__validate_string(f),
                                   group_id=self.__validate_string(self.__db_key(root=root, parent=False)),
                                   category=self.__validate_string(os.path.basename(root)),
                                   duration=self.fetch_tags(root=root, file=f, field='duration'),
                                   format=self.fetch_tags(root=root, file=f, field='filetype'),
                                   frame_rate=self.fetch_tags(root=root, file=f, field='framerate'),
                                   channels=self.fetch_tags(root=root, file=f, field='nchannels'),
                                   total_frames=self.fetch_tags(root=root, file=f, field='nframes'),
                                   sample_width=self.fetch_tags(root=root, file=f, field='sampwidth'),
                                   path=os.path.join(root, f))
                        cursor.execute(query_entry)

        data.commit()
        return data

    # TODO: Finish implementation of del_table()
    def del_table(self, table):
        cursor = self.data.cursor()
        try:
            cursor.execute('''DROP TABLE {}'''.format(table))
            return

        except:
            print("{} table not found.".format(table))
            return

    # TODO: Finish implementation of add_file()
    def add_file(self, table, file=None):
        cursor = self.data.cursor()

        if file:
            query = """INSERT INTO {table} (name) VALUES ("{file}");""".format(table=table, file=file)
        else:
            query = """INSERT INTO {table} (name) VALUES ("file");""".format(table=table)

        cursor.execute(query)
        self.data.commit()

    def cleanup(self):
        """
        Close the database
        :return:
        """
        self.data.close()

    def __identify_media(self, root, file):
        """
        Identify the media.
        :param root: file's path
        :param file: Media file.
        :return: Named tuple
        """
        try:

            ftype = sndhdr.what(os.path.join(root, file))
            return ftype

        except Exception as e:
            return print(e)

    def _format_duration(self, durarion):
        """
        Converts seconds to H:M:S string
        :param durarion: Duration in seconds
        :return: 'H:M:S' formatted string
        """
        return timedelta(seconds=int(durarion))

    # TODO: complete tag extractions for artist, release date, cover art.
    def fetch_tags(self, root, file, field):
        tags = self.__identify_media(root=root, file=file)
        if tags:
            if field is 'duration':
                with audioread.audio_open(os.path.join(root, file)) as f:
                    # duration = self._format_duration(duration=f.duration)
                    # return duration
                    return self._format_duration(f.duration)
            else:
                return eval('tags.' + field)
        else:
            return 0
