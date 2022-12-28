# SDA Assignment 1

## Our Solution


We have solved the given problem in 3 ways
- Simple python pandas groupby
- Partitioned data (Using Pandas)
    
    1. Date Partition
    2. Region Partition

- Master Slave

    1. 2 Cores
    2. 4 Cores
    3. 6 Cores 


## Setup & Install
We assume you have Python 3.8 or Higher
Make sure you have latest Java installed as well. None of this works if JAVA is not installed (At least on MacOS for sure)

Then go on to install OpenMPI.
I used the MacOS version of OpenMPI. RUN:

```brew install openmpi```

check if OpenMPI is installed correctly using:

Next you'll need the install the python package using

``` pip install mpi4py ```

## Solution Thoughts
I've tried to keep the solution simple single script so that its easy for anyone to understand.

I have used the master also to process a piece of the data and it also does the result compution.

I've used the scatter and gather method to make my solution distinct.

## Running the codes:


## Refrences:
For really great Examples on MPI: 
1. [MPI for python Docs](https://mpi4py.readthedocs.io/en/stable/tutorial.html)
2. [Parallel Computing Presentation](https://hpc-forge.cineca.it/files/ScuolaCalcoloParallelo_WebDAV/public/anno-2016/25_Summer_School/Rome/mpi4py.pdf)