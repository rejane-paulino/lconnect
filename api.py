# -*- processing: LCONNECT -*-

from process.main import Lconnect
from metadata import ManualParameter
from mode import SATELLITE


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