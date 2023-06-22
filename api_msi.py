# -*- processing: LCONNECT -*-

from process.main import Lconnect
from mode import SATELLITE


"""
Code to apply LCONNECT to MSI/Sentinel-2 data:
    :param path_IMG: directory with images;
    :param path_gridPoint: path with file of points (.shp) from reference waterbody (e.g., river);
    :param path_ROI: path with file of polygons (.shp) from target waterbody (e.g., lakes);
    :param path_OUTPUT: output directory;
    :param sensor: applied sensor.
"""


# {Input}:
path_IMG = r"C:\..."
path_gridPoint = r"C:\..."
path_ROI = r"C:\..."
path_OUTPUT = r'C:\...'
sensor = SATELLITE.SENTINEL_2


# {Process}:
lconnect = Lconnect(path_IMG, path_gridPoint, path_ROI, path_OUTPUT, sensor)
lconnect.run()