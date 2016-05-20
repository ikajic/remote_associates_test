#### run_simulation.py
Run this script as:
```bash
python run_simulation.py
```

to produce the `Figure 2` in the paper. The figure in the paper is
a simulation with the model and what is plotted here are the results using the
algorithmic simulation, which do contain small differences if you look
carefully. If the stored data (`numpy` arrays in `npz` format) is available,
use this data, otherwise the simulations are run again.

#### spreading_activity.py
Implementation of a spreading activation algorithm (`Algorithm 1` in the
paper) used for the algorithmic simulation.

#### simulation.py
The algorithm for solving RAT problems from the Bowden data set using spreading
activation. It divides problems into three categories (easy, mid and
hard) and computes the percentage of correctly solved items for each category.

Run from terminal:
```bash
python simulation.py
```

