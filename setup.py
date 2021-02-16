from distutils.core import setup
import os

token = os.environ.get("GITAUTH", "")

setup(
    name="panoply_mandrill",
    version="2.1.1",
    description="Panoply Data Source for Mandrill API",
    author="Panoply Dev Team",
    author_email="support@panoply.io",
    url="http://panoply.io",
    package_dir={"panoply": ""},
    install_requires=[
        "requests==2.21.0",
        "panoply-python-sdk @ git+https://{}@github.com/panoplyio/"
        "panoply-python-sdk.git@v1.6.5#egg==panoply-python-sdk".format(token),
        "csvsort==1.3",
        "mandrill==1.0.57"
    ],
    extras_require={
        "test": [
            "pep8==1.7.0",
            "coverage==4.3.4",
            "mock==1.0.1",
        ]
    },
    packages=["panoply.panoply_mandrill"]
)
