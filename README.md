# Social Network Analysis of South Asian–Southern African Trade (2024)

This repository contains two complementary versions of the project:

1. **Gephi (original project):** the supplied native Gephi project and final report.
2. **Python (reproducible implementation):** a notebook and supporting script that reconstruct the directed, weighted network from the supplied node and edge tables, calculate network measures, generate visualizations, and compare selected results.

## Research question
How is trade structured, integrated, and distributed in terms of power and influence among selected South Asian and Southern African countries when represented as a directed, weighted network?

## Data and network
- 19 country nodes and 79 directed export links.
- Edge direction: exporter → importer.
- Edge weight: export value as supplied in the source CSV.
- Reference year: 2024.
- Download/retrieval timing reported by the project team: December 2025.
- Source named in the original report: UN Comtrade.

The supplied materials do not contain the complete UN Comtrade query metadata (commodity classification/code, reporter/partner selection logic, trade-value field/unit, and API/query parameters). These details are not inferred; see [DATA-SOURCE.md](DATA-SOURCE.md).

## Repository structure
```text
README.md
DATA-SOURCE.md
SNA_Final_Report.pdf
data/
  SASA_NODES.csv
  SASA_EDGES.csv
gephi/
  SNA_Trade_Network.gephi
python/
  SNA_Trade_Network_Analysis.ipynb
  sna_analysis.py
  requirements.txt
  figures/
  outputs/
```

## Run the Python version
From the repository root:

```bash
python -m pip install -r python/requirements.txt
jupyter notebook python/SNA_Trade_Network_Analysis.ipynb
```

The notebook locates the `data/` directory relative to the repository root. It exports metric tables and figures into `python/outputs/` and `python/figures/`.

## Measures covered
- Degree, in-degree, out-degree, weighted in-degree, weighted out-degree, and total weighted degree
- Eigenvector, closeness, betweenness, PageRank, and HITS hub/authority scores
- Density, reciprocity, weakly and strongly connected components
- Clustering and transitivity on explicitly stated graph representations
- Modularity communities
- Diameter and average shortest path length
- Robustness under single-node and sequential targeted node removal

## Interpretation and comparability
The directed export network has one weakly connected component and 16 strongly connected components. It is connected when edge direction is ignored, but it is not strongly connected: not every country can reach every other country by following export directions.

The report's Gephi average path length (1.3189655) and diameter (2) are retained as reported values. These values correspond to directed shortest paths averaged over reachable ordered pairs; unreachable pairs are excluded. The Python implementation reports its graph representation and calculation explicitly rather than assuming all path statistics are interchangeable.

The report identifies Bangladesh as the largest importer, but the supplied edge table gives India the largest weighted in-degree and Bangladesh the second largest. The CSV ranking is preserved; the discrepancy is not silently edited.

Trade weights represent export values (strength/volume), not travel costs. They are not used directly as shortest-path distances.

## Report status
The supplied final report is included with student ID numbers removed from the contribution page while contributor names and task descriptions are retained. The earlier proposal is excluded because it concerned a different topic and was not used for this final project.
