from setuptools import setup, find_packages

setup(
    name='clusterDb',
    version='0.1.0',
    description='RESTful API for single cell clusters.',
    url='https://github.com/terraswat/clusterDb',
    author='Teresa Swatloski',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=[
        'flask-restplus==0.12.1',
        'pytest==4.0.2',
        'flask-cors==3.0.7'
    ],
)
