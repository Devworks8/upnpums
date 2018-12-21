import os.path
import itertools

from yaml import load, dump, YAMLObject

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class CfgManager(YAMLObject):
    def __init__(self):
        self.__DEFAULTS = self.__generate_defaults()
        self.settings = self.__load_settings()

    def __load_settings(self):
        if os.path.exists("./settings.yml"):
            with open("./settings.yml") as settings:
                return load(settings)

        else:
            _ = open("./settings.yml", 'w')
            dump(load(self.__DEFAULTS), _)
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

    def _find_header(self, header, value, var):
        if hasattr(var, 'iteritems'):
            for k, v in var.iteritems():
                if k == header:
                    yield v
                if isinstance(v, dict):
                    for result in self._find_header(header=header, value=value, var=v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self._find_header(header=header, value=value, var=d):
                            yield result

    def get(self, header, value):

        self._find_header(header=header, value=value, var=itertools.Iterable(self.settings))

        pass

    def set(self, header, value):
        pass


class
