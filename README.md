# NOAA Dashboard Python

Python prototype that downloads NOAA GSOD data and renders a Plotly world map of the hottest and coldest weather stations.

## What It Does

1. Downloads the NOAA Global Surface Summary of the Day dataset through Kaggle.
2. Reads station metadata and recent yearly archives.
3. Aggregates station temperatures and identifies daily extremes.
4. Displays the result as an interactive Plotly geographic chart.

## Requirements

- Python 3.10+
- A Kaggle account and API credentials configured for the Kaggle CLI
- `unzip` available on the command line
- Access to the NOAA/Kaggle dataset and its terms of use

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The script downloads data into `../input/gsod_all_years` relative to the working directory and uses Plotly's notebook display integration. Run it from the repository root.

## Notes

- This is a research prototype rather than a packaged application.
- Runtime data and downloaded archives are intentionally not committed.
- Dataset access and redistribution are governed by the original NOAA/Kaggle terms.

## License

No license was present in the source repository. Treat the code as all rights reserved until a license is added by the copyright holder.
