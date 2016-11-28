from distutils.core import setup

setup(
    name="panoply_mandrill",
    version="0.2",
    description="Panoply Data Source for Mandrill API",
    author="Oshri Bienhaker, Kfir Gez",
    author_email="oshri@panoply.io, kfir@panoply.io",
    url="http://panoply.io",
    package_dir={"panoply": ""},
    install_requires=[
        "panoply-python-sdk",
        "mock==1.0.1",
        "mandrill==1.0.57"
    ],
    packages=["panoply.mandrill"]
)
