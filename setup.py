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
        "Development Status :: 2 - Pre-Alpha ",
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

