""" clms.types Installer
"""
from os.path import join
from setuptools import setup, find_packages

NAME = "clms.types"
PATH = NAME.split(".") + ["version.txt"]
with open(join(*PATH)) as version_file:
    VERSION = version_file.read().strip()
with open("README.rst") as readme_file:
    readme = readme_file.read()
with open(join("docs", "HISTORY.txt")) as history_file:
    history = history_file.read()

setup(
    name=NAME,
    version=VERSION,
    description="An add-on with content-types for CLMS site",
    long_description_content_type="text/x-rst",
    long_description="{}\n{}".format(
        readme,
        history,
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="EEA Add-ons Plone Zope",
    author="European Environment Agency - CodeSyntax",
    author_email="mlarreategi@codesyntax.com",
    url="https://github.com/eea/clms.types",
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["clms"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "setuptools",
        "collective.z3cform.datagridfield",
        # -*- Extra requirements: -*-
        "plone.restapi",
        "collective.volto.dropdownmenu",
        "plone.schema",
        "collective.taxonomy",
        "clms.downloadtool",
        "clms.statstool",
        "plone.volto",
        "lxml",
        "requests",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework[debug]",
            "plone.restapi",
            "collective.MockMailHost",
            "coverage",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
