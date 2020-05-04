# germanetpy
Welcome. This is the Python API for the German wordnet GermaNet. GermaNet is a lexical-semantic net that relates German nouns, verbs, and adjectives semantically by grouping lexical units that express the same concept into synsets and by defining semantic relations between these synsets.
This API can be used to extract structured information from the GermaNet with python.
More information about GermaNet can be found on the following page:

https://uni-tuebingen.de/en/142806

## Installation

You can install germanetpy from PyPI (https://pypi.org/project/germanetpy/):

    pip install germanetpy

Get the GermaNet data as XML files and put all files in a data directory. When you use the API to load the data, the path pointing to the directory containing the XML files needs to be specified. The API is supported with Python 3.

## How to use

You can read the documentation [here](https://germanetpy.readthedocs.io/en/latest/)

The API provides functionality that can be used to load the data from GermaNet and query it. The data has to be retrieved
via a license agreement from the University of Tübingen, Seminar für Sprachwissenschaften:

https://uni-tuebingen.de/en/142828

To use the data for queries you first have to create a Germanet object, which loads the data specified as an argument once. This takes a few seconds:

    from germanetpy import germanet
    
    germanet_object = germanet.Germanet(path_to_the_GermaNet_XML_files)
    
This repository also provides a Tutorial [https://github.com/Blubberli/germanetpy/blob/master/germanetpy_tutorial.ipynb] that shows how to use the API to query GermaNet.
If you want to use the tutorial as an interactive jupyter notebook, clone this repository:
```
git clone https://github.com/Germanet-sfs/germanetTutorials.git
```
and follow the instructions in the README https://github.com/Germanet-sfs/germanetTutorials
