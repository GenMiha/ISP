import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universal-parser",
    version="1.0",
    author="Mihail Bogomolov",
    author_email="michail.bogomolov@gmail.com",
    description="Json/Pickle/Toml/Yaml parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GenMiha/ISP/Lab2/project_parser",
    project_urls={
        "Bug Tracker": "https://github.com/GenMiha/ISP/Lab2/project_parser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['format_converter=project_parser.main:main'],
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML>=5.4.1',
        'pytomlpp>=0.3.5',
        ],
    python_requires=">=3.6",
)