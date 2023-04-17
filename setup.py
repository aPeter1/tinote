from setuptools import setup, find_packages

setup(
    name="tinote",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ti = tinote.main:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line note-taking tool",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tinote",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
)
