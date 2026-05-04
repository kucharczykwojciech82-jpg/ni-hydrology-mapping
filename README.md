Hydrology Mapping of Northern Ireland

This project analyses the spatial distribution of rivers and water bodies across Northern Ireland using Python and GeoPandas.

The aim is to quantify and visualise:

-Total river length per county
-Total water (lake) area per county
-River density (km of river per km²)
-Water coverage (%)

Data

Vector datasets used:

-Counties (polygons)
-Rivers (lines)
-Water bodies (polygons)
-Northern Ireland outline


Outputs:

-River length per county

-Water area per county

-Hydrology map

Installation

Conda
conda env create -f environment.yml
conda activate ni-hydrology

Usage

python scripts/hydrology_analysis.py

Technologies

Python
GeoPandas
Matplotlib
Pandas

License

Educational use only.

Author

Wojciech Kucharczyk

