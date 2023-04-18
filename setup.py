from setuptools import setup, find_packages
from setuptools.command.install import install
import configparser


def get_version():
    config = configparser.ConfigParser()
    config.read('.bumpversion.cfg')
    return config['bumpversion']['current_version']


VERSION = get_version()


class CustomInstall(install):
    def run(self):
        from tinote.update import update
        update(VERSION)
        super().run()


setup(
    name="tinote",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ti = tinote.main:main"
        ]
    },
    cmdclass={
        'install': CustomInstall
    },
    author="Alec Petersen",
    author_email="k.alecpetersen@gmail.com",
    description="A command-line note-taking tool",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aPeter1/tinote",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Terminals"
    ],
    python_requires=">=3.6",
)

