from distutils.core import setup

setup(
    name="panoply_mandrill",
    version="0.1dev",
    description="Panoply Data Source for Mandrill API",
    author="Oshri Bienhaker",
    author_email="oshri@panoply.io",
    url="http://panoply.io",
    package_dir={"panoply": ""},
    install_requires=[
        "panoply-python-sdk",
        "mock==1.0.1"
    ],
    packages=["panoply.mandrill"]
)
