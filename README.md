# The Cognitive Rent Disruption: Generative AI Exposure, Task Displacements, and the Reversal of Skill-Biased Technical Change Across Regional Labor Markets

**Author:** Danil Popov  
**Correspondence:** `perque.balom@gmail.com`  
**Working Paper Date:** October 2026  

---

## Overview

This repository contains the empirical replication files for the paper *"The Cognitive Rent Disruption: Generative AI Exposure, Task Displacements, and the Reversal of Skill-Biased Technical Change Across Regional Labor Markets"*. 

The paper examines how the commercial diffusion of Generative Artificial Intelligence (foundation language and code models) impacts occupational wage growth, intra-occupational earnings dispersion, and spatial convergence across U.S. regional labor markets.

### Summary of Empirical Findings
1. **Occupational Wage Deceleration:** Post-2023, a 1-standard-deviation increase in Language Modeling Exposure (LME) is associated with a 1.32% annual deceleration in occupational mean wages ($t = -5.28, p < 0.001$).
2. **Skill-Bias Reversal:** Triple-difference estimates confirm that this slowdown is concentrated in college-educated professions ($\hat{\beta}_{\text{DDD}} = -0.0148, p < 0.001$), while physical trades and in-person services show wage resilience.
3. **Upper-Tail Dissipation:** Within college occupations, the 90th percentile wage contracts substantially ($\ln(P90/P50)$ contracts by 2.45 log points per $\sigma$), while lower-tail dispersion ($\ln(P50/P10)$) remains unaffected.
4. **Spatial Convergence:** Employment-weighted county wage growth in cognitive metropolitan hubs slowed by 0.86% per $\sigma$ of exposure ($p < 0.001$), reversing decades of regional divergence.

---

## Repository Structure

```text
├── data/
│   └── processed/
│       ├── oews_ai_occupational_panel.csv   # Balanced 2018-2025 BLS OEWS panel (753 SOCs)
│       └── qcew_aige_county_panel.csv       # Balanced 2018-2025 BLS QCEW county panel (3,218 counties)
├── figures/                                 # Output vector graphics (PDF & 300 DPI PNG)
│   ├── fig1_theoretical_inversion.{pdf,png}
│   ├── fig2_event_study_lme.{pdf,png}
│   ├── fig3_scatter_education_compression.{pdf,png}
│   └── fig4_county_wage_convergence.{pdf,png}
├── paper/
│   ├── main.tex                             # Complete monolithic LaTeX manuscript & appendix
│   └── figures/                             # Figures embedded in the manuscript
├── src/
│   ├── __init__.py
│   ├── data_prep.py                         # Panel loading, log transforms, and variable construction
│   ├── estimate_models.py                   # Econometric estimation (Tables 2-5)
│   └── generate_figures.py                  # Figure generation (Figures 1-4)
├── generate_figures.py                      # Standalone figure generator (root convenience)
├── run_all.py                               # Master execution script
├── requirements.txt                         # Python package requirements
├── .gitignore
├── LICENSE                                  # MIT License
└── README.md
```

---

## Requirements and Installation

The code is written in Python 3.10+ and relies on standard scientific libraries (`numpy`, `scipy`, `pandas`, `matplotlib`).

To clone the repository and install dependencies:
```bash
git clone https://github.com/karodg/cognitive-rent-disruption-.git
cd cognitive-rent-disruption-
pip install -r requirements.txt
```

---

## Replication Instructions

### Master Run
To run the entire pipeline (data validation, regression models, and figure generation) in one step:
```bash
python run_all.py
```
Total execution time is under 5 seconds on standard hardware.

### Running Individual Components

1. **Verify and clean data panels:**
   ```bash
   python -m src.data_prep
   ```

2. **Estimate econometric models (Tables 2–5):**
   ```bash
   python -m src.estimate_models
   ```

3. **Re-generate figures (Figures 1–4):**
   ```bash
   python generate_figures.py
   ```
   All generated figures will be saved in `figures/` as both vector PDF and high-resolution PNG.

---

## Data Sources and Crosswalks

- **BLS Occupational Employment and Wage Statistics (OEWS):** Annual research files (May 2018 – May 2025). 2010 and 2018 SOC codes harmonized to 2018 SOC 6-digit definitions.
- **BLS Quarterly Census of Employment and Wages (QCEW):** Annual county-level employment and wage aggregates across 3,218 U.S. counties.
- **AI Exposure Metrics:** Edward Felten, Manav Raj, and Robert Seamans (2021, 2023), *"Occupational, Industry, and Geographic Exposure to Artificial Intelligence"* and *"How will Language Modelers like ChatGPT Affect Occupations and Industries?"*.
- **Telework Feasibility:** Jonathan Dingel and Brent Neiman (2020), *"How Many Jobs Can be Done at Home?"*, *Journal of Public Economics*.

---

## Citation

```bibtex
@article{popov2026cognitive,
  title={The Cognitive Rent Disruption: Generative AI Exposure, Task Displacements, and the Reversal of Skill-Biased Technical Change Across Regional Labor Markets},
  author={Popov, Danil},
  journal={Working Paper},
  year={2026},
  url={https://github.com/karodg/cognitive-rent-disruption-}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
