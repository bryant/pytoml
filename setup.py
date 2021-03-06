from setuptools import setup, find_packages

install_requires = [
    "pyparsing < 2.0.0",
]
tests_require = [
    "nose >= 1.0",
]

setup(
    name = "pytoml",
    version = "0.1",
    description = "Python de-/serializer for TOML.",
    url = "https://github.com/bryant/pytoml",
    
    license = "MIT License",
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    packages = find_packages(),
    install_requires = install_requires,
    tests_require = tests_require,
    test_suite = "nose.collector",
)
