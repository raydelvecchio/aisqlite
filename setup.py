from setuptools import setup, find_packages

setup(
    name='aisqlite',
    version='1.0.0',
    author='Ray Del Vecchio',
    author_email='ray@cerebralvalley.ai',
    description='AI enhanced SQLite',
    url='https://github.com/raydelvecchio/aisql',
    packages=find_packages(),
    install_requires=[
        'setuptools', 
        'twine',
        'openai',
        'wheel',
    ],
)
