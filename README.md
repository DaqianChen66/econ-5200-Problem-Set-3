# econ-5200-Problem-Set-3
# ECON 5200 Problem Set 3  
## The Rollout That Looked Like It Worked

This project evaluates a staggered county-level workforce training rollout and shows why a conventional two-way fixed effects (TWFE) estimate can be misleading when treatment effects vary with exposure.

## Main Results

The simulated panel contains 40 counties in 8 regional workforce boards over 12 years. Treatment is assigned at the board level and adoption is staggered across boards.

Key estimates:

- True average treatment effect on treated observations: **2.690**
- Agency-style TWFE estimate: **1.523**
- Minimum true treatment effect: **2.000**
- Share of TWFE weight from already-treated control comparisons: **30.5%**
- Clean staggered-adoption ATT using never-treated or not-yet-treated controls: **2.430**
- Board-clustered standard error for TWFE: **0.468**
- Conventional board-clustered p-value: **0.0011**
- Exact wild cluster bootstrap p-value: **0.0078**

The main finding is that the positive and statistically significant TWFE coefficient substantially understates the true average effect because it places weight on comparisons that use already-treated units as controls.

## Methods

The notebook includes:

- Card and Krueger two-by-two DiD replication
- TWFE estimation under staggered adoption
- Decomposition of valid and forbidden comparisons
- Group-time ATT estimation using only never-treated or not-yet-treated controls
- Event-study analysis
- County- and board-clustered inference
- Exact wild cluster bootstrap with all \(2^8 = 256\) Rademacher sign vectors
- A budget-office memo and hostile-read robustness exercise

## Files

- `Econ_5200_PS3.ipynb` — main analysis notebook
- `src/did_toolkit.py` — reusable DiD and inference functions
- `ai-appendix.md` — required AI prompts and raw model responses
- `README.md` — project overview

## Reproducibility

The simulation uses seed **42**. The notebook is designed to run from top to bottom with the final **Truth and headline numbers** cell providing a traceable record of the simulation parameters and reported results.
