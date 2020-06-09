import setuptools

with open("README.md") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="stanfordkarel",
    version="0.2.1",
    author="Nicholas Bowman, Kylie Jue, Tyler Yep",
    author_email="tyep10@gmail.com",
    description="Official Stanford Karel library used in CS 106A",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tyleryep/stanford-karel",
    packages=["stanfordkarel"],
    include_package_data=True,
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
