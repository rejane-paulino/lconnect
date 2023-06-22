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

> Consider the description below for best experience with LCONNEC.

* *path_IMG:* directory with images;
* *path_CLOUD:* directory with cloud masks - udm2 (only SUPERDOVE data);
* *path_gridPoint:* path with file of points (in shapefile) from reference waterbody (e.g., river);
* *path_ROI:* path with file of polygons (in shapefile) from target waterbody (e.g., lakes); 
* *path_OUTPUT:* output directory;
* *sensor:* applied sensor (sd or msi). 

## Outuput Parameters:





 `path_IMG path_CLOUD path_gridPoint path_ROI path_OUTPUT sensor`


