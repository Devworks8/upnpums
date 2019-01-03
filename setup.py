import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UPnPUMS",
    version="0.1.0",
    author="Christian Lachapelle & Jason Major",
    author_email="devworks8@gmail.com",
    description="UPnP Universal Media Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devworks8/upnpums",
    license='GNU General Public License v3 (GPLv3)',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: Twisted",
    ],
    install_requires=["PyAudio",
                      "PyYAML",
                      "Twisted",
                      "audioread",
                      "deepmerge",
                      "m3u8",
                      "m3u8-generator",
                      "requests",
                      "mutagen"],
)

"""
from distutils.core import setup

setup(
    name='UPnPUMS',
    version='0.1.0dev',
    author='Christian Lachapelle & Jason Major',
    author_email='devworks8@gmail.com',
    packages=['upnpums', 'upnpums.config', 'upnpums.database', 'upnpums.network', 'upnpums.network.interfaces',
              'upnpums.network.interfaces.ums', 'upnpums.network.interfaces.upnp', 'upnpums.shell',
              'upnpums.shell.commands'],
    url='http://pypi.python.org/pypi/UPnPUMS/',
    license='LICENSE',
    long_description=open('README.md').read(),
    requires=["PyAudio >= 0.2.11",
              "PyYAML >= 3.13",
              "Twisted >= 18.9.0",
              "audioread == 2.1.6",
              "deepmerge == 0.0.4",
              "m3u8 >= 0.3.7",
              "m3u8-generator >= 1.5",
              "requests == 2.21.0",
              "mutagen == 1.41.1"],

)
"""
