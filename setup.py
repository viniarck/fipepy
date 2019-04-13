from setuptools import setup
from fipepy.version import __version__

desc = "fipe api"

setup(
    name="fipepy",
    version=__version__,
    description=desc,
    author="Vinicius Arcanjo",
    author_email="viniark@gmail.com",
    keywords="fipe cars carros tabela preço",
    url="http://github.com/viniarck/fipepy",
    packages=["fipepy"],
    license="Apache",
    install_requires=[
        "django==2.2",
        "djangorestframework==3.9.2",
        "django-cors-headers==2.5.2",
        "fire==0.1.3",
        "requests==2.21.0",
        "django-rest-swagger==2.2.0",
        "psycopg2-binary==2.8.1",
    ],
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    zip_safe=False,
)
