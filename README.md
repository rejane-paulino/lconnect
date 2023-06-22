# LCONNECT (river-Lake CONNECTivity) <img src="img/lconnect.svg" width="150" align="right" />

LCONNECT framework combines machine learning algorithms and spectral similarity features to predict water surface connectivity between floodplain lakes and their main river. The assumption is that the spectral similarity between river and lake waters is a good proxy for the hydrological connectivity and this methodology is applicable when the main river drives the changes on the optical water properties (i.e., flux of high sediment load waters) of its flooding lakes. Here, the hydrological connectivity means the dynamic flow interactions between large rivers with flooding season and their floodplain lakes, which occurs by channelized and diffuse overbank flows, and affects the surface water connectivity.

## Requirements and Installation:
LCONNECT framework is coded in Python 3.8 and it requires Python packages to run: `numpy pandas geopandas rasterio gdal`

To run the LCONNECT, it is necessary a suitable installation and use of the environment `lconnect` by command line:

            conda env create -f environment.yml
            conda activate lconnect
            cd into the lconnect directory
            python api_superdove.py (or python api_msi.py)

## Input Parameters:
The input patameters must be manualy filled in the file `parameters.txt`. LCONNECT framework requires different input data: `path_IMG path_CLOUD path_gridPoint path_ROI path_OUTPUT sensor`     

* *path_IMG:* directory with images;
* *path_CLOUD:* directory with cloud masks - udm2 (only `SuperDove` data);
* *path_gridPoint:* path with file of points (in shapefile) from reference waterbody (e.g., river);
* *path_ROI:* path with file of polygons (in shapefile) from target waterbody (e.g., lakes); 
* *path_OUTPUT:* output directory;
* *sensor:* applied sensor (`sd` or `msi`). 

### Warning:
> The images .TIFF (in `path_IMG`) must be stacked.

> The `msi` images must be in surface reflectance (from 0 to 1).

> The `sd` images must be in surface reflectance (from 0 to 10,000).

> Spectral bands used for `SuperDove`: `B441 B490 B531 B565 B610 B665 B705 B865`.

> Spectral bands used for `MSI/Sentinel-2`: `B490 B560 B665 B705 B740 B783 B842`           

## Output Parameters:
Two files .csv are available in `path_OUTPUT`: `reference_spectra.csv` and `OutputLakesParameters.csv

* *reference_spectra:* reference spectra obtained from reference waterbody (monthly average);
* *OutputLakesParameters:* lakes' parameters obtained after classification. In this file there are information about: `date`, `id_lake`, `spectral similarity features`, `lakes spectra`, `hydrological connectivity or Conn`.

> The `hydrological connectivity` is represented by values 0-not-connected and 1-connected.           



