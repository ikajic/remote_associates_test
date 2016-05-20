# Remote Associates Test
Neural network simulation of the Remote Associates Test as presented in the
paper:

```
Kajić, I., & Wennekers, T. (2015). Neural network model of semantic processing in the remote associates test. In Workshop on Cognitive Computation: Integrating Neural and Symbolic Approaches, 29th Annual Conference on Neural Information Processing Systems (NIPS 2015)
```

There is an algorithmic and a neural network simulation of the test: the
algorithmic version is faster to run because it does not simulate neurons but
search in a graph. The simulation of a model takes much longer, with minor
differences in results. 

The following manual explains how to reproduce figures and numbers from the paper.

### 0. Get this code
Get a copy of this repository by:
```
git clone git@github.com:ikajic/remote_associates_test.git
```

In the cloned directory, install the package (for easier handling of imports in scripts):
```
python setup.py develop
``` 

### 1. Requirements
First, ensure all tools and packages are installed. Most packages are available with `pip`, so from the cloned repository you can either do:
```
pip install -r requirements.txt
```
to get all of them (and a bit more) at once, or install them one by one:

* [Python 2.7](https://www.python.org/)
* [NumPy](http://www.numpy.org/)
* [SciPy](http://www.scipy.org/)
* [matplotlib](http://matplotlib.org/)
* [pandas](http://pandas.pydata.org)

### 2. Fetching and processing the data
You need to manually download the [University of Florida Free Association
Norms](http://w3.usf.edu/FreeAssociation//) to
`./data/raw/freeassociations/data`. There is a README file in that directory
explaining what needs to be contained there.

After downloading the sheets, run the script `process_data.py` in
`./data/raw/freeassociations` to generate the association matrix. It will store
the matrix in the place where the rest of the scripts know how to find it. This
script assumes the norms will be downloaded by right-clicking "Save as..". This
will download a html file for every sheet and those contain html tags at the
beginning and at the end. The `process_data.py` script automatically handles
that by removing the first and the last three rows (it does not check whether
those are html tags, it just removes them). 

If that went well, you should be seeing a file called
`free_associations_vocabulary` in `./data/processed`, this is a Python pickle
file that stores the association matrix and the word vocabularies.

### 3. Running simulations
To run the algorithmic version of the model (fast), go to the `algorithm` directory
and run `run_simulation.py`, otherwise do the same thing for the `model`. The
code for model is not optimized, so it is very slow and eats up a lot of memory.
