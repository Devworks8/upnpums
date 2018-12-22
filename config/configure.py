import os.path
import collections
from itertools import chain
from deepmerge import always_merger

from yaml import load, dump, YAMLObject

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class CfgManager:
    def __init__(self):
        self.__DEFAULTS = self.__generate_defaults()
        self.settings = self.__load_settings()

    def __load_settings(self):
        if os.path.exists("./settings.yml"):
            with open("./settings.yml") as settings:
                return self._flatten(load(settings))
                # return load(settings)
        else:
            _ = open("./settings.yml", 'w')
            dump(load(self.__DEFAULTS), _, default_flow_style=False)

            return load(self.__DEFAULTS)

    def __generate_defaults(self):
        defaults = """
        database:
            path: None
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
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _inflate(self, d, sep='_'):
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




    def _find_header(self, header=None):
        results = []
        for k, v in self.settings.items():
            if header in k:
                results.append((k, v))
        return results

    """
    def _find_header(self, header=None, value=None, var=None):
        print(var)
        hasattr(var, 'items')
        #if hasattr(var, 'items'):
        for k, v in var.items():
            if k == header:
                yield v
            if isinstance(v, dict):
                for result in self._find_header(header=header, value=value, var=v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self._find_header(header=header, value=value, var=d):
                        yield result
    """

    def get(self, header=None, value=None, var=None):
        print(self.settings)
        print(self._inflate(self.settings))
        return self._find_header(header=header)

    def set(self, header, value):
        pass
