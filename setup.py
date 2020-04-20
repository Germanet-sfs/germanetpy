import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent
requirements = ["numpy>=1.18.1", "lxml>=4.4.2", "pytest>=5.3.2", "fastenum>=0.0.1", "tqdm>=4.14",
                "python-Levenshtein==0.12.0"]

# The text of the README file
long_description = (HERE / "README.md").read_text()
setuptools.setup(
    name="germanetpy",
    version="0.1.2",
    author="Neele Falk",
    author_email="neele.witte@uni-tuebingen.de",
    description="Python API for GermaNet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blubberli/germanetpy.git",
    install_requires=requirements,
    packages=["germanetpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
