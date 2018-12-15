"""
pluginmanager.py is part of the interfaces package
"""

from threading import Thread


class PluginManager:
    def __init__(self):
        pass

    def list_plugins(self, scheme=None, plugin=None):
        """
        List all plugins by scheme or by plugin name.
        :param scheme: Service scheme to use; None == All
        :param plugin: Plugin name
        :return: {scheme: [plugin]}
        """
        pass

    def add_plugin(self, scheme=None, plugin=None, position=-1):
        """
        Add a plugin or scheme
        :param scheme: Service scheme to use
        :param plugin: Plugin name
        :return:
        """
        pass

    def remove_plugin(self, scheme=None, plugin=None):
        """
        Remove a plugin.
        :param scheme: Service scheme to remove from; None == All
        :param plugin: Plugin name
        :return:
        """
        pass

    def start_plugin(self, scheme=None, plugin=None):
        """
        Start a plugin or scheme
        :param scheme: Service scheme to use; None == All
        :param plugin: Plugin name
        :return:
        """
        pass

    def stop_plugin(self, scheme=None, plugin=None):
        """
        Stop a plugin or scheme
        :param scheme: Service scheme to use; None == All
        :param plugin: Plugin name
        :return:
        """
        pass


class CommandThread(Thread):
    def __init__(self, device, upnp, ssdp):
        """

        :type device: Device
        :type upnp: UPnP
        :type ssdp: SSDP
        """
        Thread.__init__(self)
        self.device = device
        self.upnp = upnp
        self.ssdp = ssdp

        self.running = True

    def run(self):
        while self.running:
            try:
                command = 'command_' + raw_input('')

                if hasattr(self, command):
                    getattr(self, command)()
            except EOFError:
                self.command_stop()

    def command_stop(self):
        # Send 'byebye' NOTIFY
        self.ssdp.clients.sendall_NOTIFY(None, 'ssdp:byebye', True)

        # Stop everything
        self.upnp.stop()
        self.ssdp.stop()
        reactor.stop()
        self.running = False