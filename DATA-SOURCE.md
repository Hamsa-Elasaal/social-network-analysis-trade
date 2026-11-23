# Data source and provenance

The supplied final report identifies **UN Comtrade** as the source of bilateral export data. The project team stated that the reference period is **2024** and that the data were downloaded in **December 2025**.

The repository preserves the supplied node and edge CSV files. Their columns identify source and target country IDs/labels, export weight, and directed/export edge type.

## What is documented from the supplied materials
- Database named by the report: UN Comtrade.
- Reference year: 2024 (team-provided clarification).
- Download timing: December 2025 (team-provided clarification).
- Network scope: selected South Asian and Southern African countries.
- Edge interpretation in the report: exporter → importer.
- Weight interpretation in the report: export value.

## Metadata still needed for full reproducibility
The supplied files and report do not specify the exact UN Comtrade query in enough detail to reconstruct it independently. The following are intentionally marked as **not specified in the supplied materials**:
- Commodity/HS classification and product code(s)
- Reporter and partner code selection and exact inclusion rule
- Whether exports are reported or mirror-adjusted
- Trade-value measure and currency/unit
- Treatment of re-exports, aggregates, and confidential/suppressed values
- Exact API endpoint/query parameters or saved query URL

Do not infer these fields from the resulting network. If the original query/export settings become available, add them here and cite the saved query or download metadata.
