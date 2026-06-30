# Marquetry Veneer Seam Cipher Reconstruction

Complete Eris-style challenge package for a from-scratch permutation reconstruction task.

- `raw/generate_raw.py` creates deterministic raw veneer packet rows.
- `dataset_description_eris_upload.md` is the dataset description for Eris.
- `prepare.py` hashes identifiers, encodes seam signatures, and creates deterministic public/private splits.
- `problem.md` is the solver-facing challenge statement.
- `grade.py` computes chance-adjusted pairwise order agreement.
- `rubrics.yaml` contains task-specific rubric criteria.
- `solution.ipynb`, `solution.py`, and `reference_solution.py` provide a solvability baseline.

## Submission Mapping

Dataset upload:

- Title: `Marquetry Veneer Seam Cipher Dataset`
- Description: paste `dataset_description_eris_upload.md`
- Data files: upload a zip containing top-level `data.csv` and `generate_raw.py`
- License: `CC0 1.0 Public Domain`
- Source URL: use the GitHub repository URL once uploaded, or note deterministic synthetic local generation if the field accepts text.

Challenge:

- Domain: `From Scratch`
- Difficulty: `Medium`
- GPU: `A10G`
- Title: `Marquetry Veneer Seam Cipher Reconstruction`
- Grade direction: `Maximize`
- Min score: `0`
- Max score: `1`
- Tags: `feature-engineering`, `small-data`
- Problem description: paste `problem.md`
- Grading script: paste `grade.py`
- Prepare script: paste `prepare.py`
- Rubrics: use `rubrics.yaml`
- Reference solution: upload `solution.ipynb`
