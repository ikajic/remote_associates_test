## Data

The data used to create and simulate the RAT model.

The `raw` directory contains experimental data from other researchers:

* freeassociations: word pair association strengths from the free association
experiment by Nelson, McEvoy and Schreiber (1998) at the University of Florida.
The directory contains a reference to the original sheets, scripts to process
sheets and to create a connection matrix.

* ratproblems/bowden: 144 RAT problems used to create a normative database by
Bowden and Jung-Beeman (2003). The directory contains an xlsx sheet with the
problems and the performance data (transcript from the original paper) and
a script to process the xlsx sheet.

The `processed` directory contains the processed and extracted data from the 
`raw` directory. It includes data stored in a format to be read by Python scripts.

### References:
 Nelson, D. L., McEvoy, C. L., & Schreiber, T. A. (1998). The University of
 South Florida word association, rhyme, and word fragment norms.
 http://www.usf.edu/FreeAssociation/.

 Bowden, E.M., & Jung-Beeman, M.  (2003).  Normative data for 144 compound
 remote associate problems.  Behavioral Research Methods, Instrumentation, and
 Computers, 35, 634-639.
