from setuptools import setup, find_packages

setup(
    name='chat-service',
    version='1.0',
    description='Chat service for SKA',
    author='Amani Ben Hassine',
    author_email='amani.benhassine@esprit.tn',
    packages=find_packages(),
    install_requires=[
        'django',
        'djangorestframework',
        'daphne',
        'py-eureka-client',
        'requests',
        'channels',
        'psycopg2',
        'django-cors-headers',
        'asgiref'
    ],
)
