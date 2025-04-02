# Fenwick_Trees
This repo hosts the code used in our bachelor project on Fenwick Trees at ITU

# Description
This repo will host code for manim animations that visualize how Fenwick Trees work (how do they store information, update and output based on quries. There will be some sample code for a Fenwick Tree implementation (WIP This may turn into a full fledged library at some point, hoping to use pyo3 for faster exection of heavier operations). There will potentially also be a small chapter written documenting how fenwick trees work in the style of a algorithms course book.

# Visualization
...

# Code
...

# Test Viewer
The repo includes a small golang package that helps visualize the output from treeTester.py. An optinal flag will output the test as a json file that can be opened with this. It will then let you select any test from that run and view things like running time for each subtest as well as give a bargraph overview of the entire test comparing running time. If any errors were present during the test and the user enabled the disable_panic flag you can view every test that output an error to try and help debug issues with the BIT implementation.  

To run the test viewer:
```
$ go run main.go [output.json]
```
The output.json is optional there is a built in file picker that you can select any json file from as well

# Setting up conda environment
The `environment.yml` file defines the conda environment that can be used to run and develop on the project.

Create the environment:
```
$ conda env create -f environment.yml
```

Activate environment:
```
$ conda activate fenwick_manim
```