#Data_Scrape

import pandas as pd
import requests

# Target URL
url = "https://ftp.cpc.ncep.noaa.gov/wd52dg/data/indices/tele_index.nh"

# Fetch raw text lines skipping the header instructions
response = requests.get(url)
lines = response.text.split("\n")

# Find where data rows start (skipping label blocks)
data_lines = [l for l in lines if l and l[0].isdigit()]

# Column names specified by NOAA documentation
columns = [
    "Year", "Month", "NAO", "EA", "WP", "EP_NP", "PNA", 
    "EA_WR", "SCA", "TNH", "POL", "PT", "Explained_Variance_Pct"
]

# Standard column width slices for NOAA's fixed-width format
widths = [4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7]

# Parse rows robustly
data = []
for line in data_lines:
    row = []
    start = 0
    for w in widths:
        val = line[start:start+w].strip()
        # Convert -99.90 missing indicators to empty values
        if val == "-99.9" or val == "-99.90":
            val = ""
        row.append(val)
        start += w
    data.append(row)

# Construct DataFrame and export to clean CSV
df = pd.DataFrame(data, columns=columns)
df.to_csv("noaa_nh_teleconnection_indices.csv", index=False)