from setuptools import setup, find_packages


setup(
    name='typesystem',
    version='0.1',
    description="An abstract type system",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='types rdf',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/granoproject/typesystem',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'python-dateutil==1.5',
        'normality>=0.2.2'
    ],
    tests_require=[],
    entry_points={}
)
