import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# 1. Set data folder
# ---------------------------------------------------------
data_dir = Path("data")

counties_file = data_dir / "Counties.shp"
rivers_file = data_dir / "Rivers.shp"
water_file = data_dir / "Water.shp"
outline_file = data_dir / "NI_outline.shp"
# ---------------------------------------------------------
# 2. Load shapefiles
# ---------------------------------------------------------
counties = gpd.read_file(counties_file)
rivers = gpd.read_file(rivers_file)
water = gpd.read_file(water_file)
outline = gpd.read_file(outline_file)

