import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stanfordkarel",
    version="0.0.3",
    author="Nicholas Bowman, Kylie Jue, Tyler Yep",
    author_email="tyep10@gmail.com",
    description="Official Stanford Karel library used in CS 106A",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tyleryep/stanford-karel",
    packages=["stanfordkarel"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
