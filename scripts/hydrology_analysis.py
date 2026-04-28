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
# ---------------------------------------------------------
# 3. Reproject to UTM (metres)
# ---------------------------------------------------------
target_crs = "EPSG:32629"

counties = counties.to_crs(target_crs)
rivers = rivers.to_crs(target_crs)
water = water.to_crs(target_crs)
outline = outline.to_crs(target_crs)
# ---------------------------------------------------------
# 4. Column names
# ---------------------------------------------------------
county_name_field = "CountyName"
# ---------------------------------------------------------
# 5. River length per county
# ---------------------------------------------------------
rivers_clip = gpd.overlay(
    rivers,
    counties[[county_name_field, "geometry"]],
    how="intersection"
)

rivers_clip["river_length_km"] = rivers_clip.geometry.length / 1000

river_summary = (
    rivers_clip
    .groupby(county_name_field)["river_length_km"]
    .sum()
    .reset_index()
)

# ---------------------------------------------------------
# 6. Water area per county
# ---------------------------------------------------------
water_clip = gpd.overlay(
    water,
    counties[[county_name_field, "geometry"]],
    how="intersection"
)

water_clip["water_area_km2"] = water_clip.geometry.area / 1_000_000

water_summary = (
    water_clip
    .groupby(county_name_field)["water_area_km2"]
    .sum()
    .reset_index()
)
# ---------------------------------------------------------
# 7. Merge results
# ---------------------------------------------------------
counties["county_area_km2"] = counties.geometry.area / 1_000_000

results = counties[[county_name_field, "county_area_km2", "geometry"]].merge(
    river_summary,
    on=county_name_field,
    how="left"
)

results = results.merge(
    water_summary,
    on=county_name_field,
    how="left"
)

results["river_length_km"] = results["river_length_km"].fillna(0)
results["water_area_km2"] = results["water_area_km2"].fillna(0)

# ---------------------------------------------------------
# 8. Calculate metrics
# ---------------------------------------------------------
results["river_density_km_per_km2"] = (
    results["river_length_km"] / results["county_area_km2"]
)

results["water_coverage_percent"] = (
    results["water_area_km2"] / results["county_area_km2"] * 100
)
# ---------------------------------------------------------
# 9. Print results (TABLE)
# ---------------------------------------------------------
print("\nHydrology results by county:\n")

print(
    results[
        [
            county_name_field,
            "river_length_km",
            "water_area_km2",
            "river_density_km_per_km2",
            "water_coverage_percent"
        ]
    ].round(2)
)

# ---------------------------------------------------------
# 10. Key finding
# ---------------------------------------------------------
top_county = results.loc[
    results["river_density_km_per_km2"].idxmax()
]

print("\nCounty with the most river coverage:")
print(
    f"{top_county[county_name_field]} "
    f"with {top_county['river_density_km_per_km2']:.2f} km of river per km²"
)
