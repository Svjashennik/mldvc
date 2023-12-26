from setuptools import setup

import mldvc

AUTHOR = "Nikita Astashkin"
AUTHOR_EMAIL = "nek1212121@gmail.com"
HOME_PAGE = ""

setup(
    name="mldvc",
    version=mldvc.__version__,
    description="Data Version Control Prototype for ML",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=["mldvc"],
    entry_points={"console_scripts": ["mldvc = mldvc.__main__:main"]},
    url=HOME_PAGE,
    license="GPLv3",
    python_requires=">=3.10.12",
)
