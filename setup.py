from distutils.core import setup

setup(
    name="panoply_mandrill",
    version="0.1dev"
    description="Panoply Data Source for Mandrill API",
    author="Oshri Bienhaker",
    url="http://panoply.io"
    pacakge_dir={"panoply": ""},
    packages=["panoply.mandrill"]
)