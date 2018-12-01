from setuptools import setup, find_packages

setup(
    name='clusterDb',
    version='0.1.0',
    description='RESTful API for single cell clusters.',
    url='https://github.com/Stuartlab-UCSC/clusterDb',
    author='Teresa Swatloski',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.12.1'],
)
