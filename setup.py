from setuptools import setup, find_packages

setup(
    name="fetch_images",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fetch=modules.fetch:sync_wrapper', 
        ],
    },
    install_requires=[],
)