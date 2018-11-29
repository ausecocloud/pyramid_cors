from setuptools import setup, find_packages

version = '0.2.0'

setup(
    name='pyramid_cors',
    version=version,
    description="Pyramid CORS helpers",
    long_description=(open("README.rst").read() + "\n\n" +
                      open("HISTORY.rst").read()),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords='python pyramid cors',
    author='',
    author_email='',
    url='https://github.com/ausecocloud/pyramid_cors',
    license='Apache License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'pyramid',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
        ],
    }
)
