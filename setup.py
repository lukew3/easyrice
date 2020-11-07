from setuptools import setup, find_packages

setup(
    name='easyrice',
    version='0.0.1',
    description='A rice setup manager',
    url='https://github.com/lukew3/easyrice',
    author='Luke Weiler',
    author_email='lukew25073@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'easyrice=easyrice.cli:cli',
        ],
    },
)
