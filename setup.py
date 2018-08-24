from setuptools import setup, find_packages

setup(
    name="ya_jsonapi",
    version='0.0.1',
    description="Yet another jsonapi client library. Sync and async, with (TODO) optional orm and caching",
    long_description="TODO",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
    ],
    author="Igor Kotrasiński",
    author_email="i.kotrasinsk@gmail.com",
    url="https://github.com/Wesmania/ya-jsonapi",
    keywords="JSONAPI JSON API client",
    license="BSD-3",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
