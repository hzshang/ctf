from setuptools import setup, find_packages

setup(
    name='challenge',
    version='1.0.0',
    install_requires=[
        'grpcio-tools',
        'peewee',
        'colorlog',
        'bcrypt',
        'gmpy2',
        'psycopg2-binary',
        'cryptography',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cloud-server=challenge.cloud.main:main',
            'node-server=challenge.node.main:main',
        ],
    },
)
