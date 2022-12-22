from setuptools import setup

from yqrc_core import __version__

setup(
    name='yqrc-core',
    version=__version__,
    author='Muhamed Hassan',
    description='YQRCCore is used by all other microservices.',
    packages=['yqrc_core'],
    package_data={'yqrc_core': ['py.typed']},
    install_requires=[
        'fastapi==0.88.0',
        'psycopg2==2.9.5',
        'pydantic==1.10.2',
        'python-dotenv==0.21.0',
        'python-jose==3.3.0',
        'SQLAlchemy==1.4.45',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
