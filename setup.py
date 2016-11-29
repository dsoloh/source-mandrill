from distutils.core import setup

setup(
    name="panoply_mandrill",
    version="1.0.1",
    description="Panoply Data Source for Mandrill API",
    author="Kfir Gez, Oshri Bienhaker",
    author_email="kfir@panoply.io, oshri@panoply.io",
    url="http://panoply.io",
    package_dir={"panoply": ""},
    install_requires=[
        "panoply-python-sdk",
        "mock==1.0.1",
        "mandrill==1.0.57"
    ],
    packages=["panoply.mandrill"]
)
