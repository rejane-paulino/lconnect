# -*- processing: LCONNECT -*-

from process.main import Lconnect
from mode import SATELLITE
from metadata import ManualParameter

"""
Code to apply LCONNECT to SuperDove data:
    :param path_IMG: directory with images;
    :param path_CLOUD: directory with cloud masks - udm2;
    :param path_gridPoint: path with file of points (.shp) from reference waterbody (e.g., river);
    :param path_ROI: path with file of polygons (.shp) from target waterbody (e.g., lakes);
    :param path_OUTPUT: output directory;
    :param sensor: applied sensor.
"""

parameters = ManualParameter()
sensor = parameters.sensor

if sensor == SATELLITE.SUPERDOVE:
    lconnect = Lconnect(parameters.path_IMG, parameters.path_gridPoint, parameters.path_ROI, parameters.path_OUTPUT, parameters.sensor, parameters.path_CLOUD)
    lconnect.run()

elif sensor == SATELLITE.SENTINEL_2:
    lconnect = Lconnect(parameters.path_IMG, parameters.path_gridPoint, parameters.path_ROI, parameters.path_OUTPUT, parameters.sensor)
    lconnect.run()

else:
    print('Error: Unidentified sensor. Please enter a valid name.')