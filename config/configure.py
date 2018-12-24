import os.path
import collections

from deepmerge import always_merger
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class CfgManager:
    def __init__(self):
        self.__DEFAULTS = self.__generate_defaults()
        self.settings = self.__load_settings()

    def __load_settings(self):
        """
        Load settings from file, ifnotexist, create new file.
        :return: dictionary
        """
        if os.path.exists("./settings.yml") and os.stat("./settings.yml").st_size > 1:
            with open("./settings.yml") as settings:
                return self._flatten(load(settings))
        else:
            with open("./settings.yml", 'w') as _:
                dump(load(self.__DEFAULTS), _, default_flow_style=False)

            return self._flatten(load(self.__DEFAULTS))

    def __generate_defaults(self):
        defaults = """
        database:
            path: './data'
            library: './library'
        m3u8:
            path: None
        interface:
            upnp:
                ip: '285.255.255.255'
                port: 1900
            ums:
                ip: None
                port: None
                """

        return defaults
        # self.__DEFAULTS = self.DbSet(path='./')
        # print(self.__DEFAULTS)

    def _flatten(self, d, parent_key='', sep='_'):
        """
        Flattens nested dictionary.
        :param d: nested dictionary
        :param parent_key: root key
        :param sep: separator to use
        :return: flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _inflate(self, d, sep='_'):
        """
        Expands flattened nested dictionary.
        :param d: flatten dictionary
        :param sep: separator used
        :return: nested dictionary
        """
        results = {}
        for k, v in d.items():
            result = ''
            cap = 0
            for word in k.split(sep):
                result += "{" + "'{}': ".format(word)
                cap += 1
            result += "'{}'".format(v) + "}" * cap
            results = always_merger.merge(results, eval(result))
        return results

    def _find_header(self, header=None, value=None):
        """
        Locate key and value set.
        :param header: key to look for
        :param value: key's value to set
        :return: List of tuples
        """
        results = []
        for k, v in self.settings.items():
            if header in k:
                results.append((k, v))

        if value and results:
            for i in results:
                self.settings[i[0]] = value
            return
        elif results:
            return results
        else:
            return None

    def show_config(self):
        return dump(self._inflate(self.settings), default_flow_style=False)

    def get(self, header=None):
        """
        Get the value associated with header
        :param header: key to search
        :return: list of tuples
        """
        return self._find_header(header=header)

    def set(self, header, value):
        """
        Sets the value associated with the header
        :param header: key to search
        :param value: new value
        :return:
        """
        self._find_header(header=header, value=value)

    def save(self):
        """
        Save current settings to file.
        :return:
        """
        with open("./settings.yml", 'w') as _:
            dump(self._inflate(self.settings), _, default_flow_style=False)
