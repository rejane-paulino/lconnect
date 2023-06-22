# -*- processing: LCONNECT -*-

from .toolbox import AverageRSPECTRA_SD
from .toolbox import TIMESERIES_SD
from .toolbox import AverageRSPECTRA_MSI
from .toolbox import TIMESERIES_MSI
from .filter import Filter
from .model import Model


class Lconnect():
    def __init__(self, path_IMG, path_gridPoint, path_ROI, path_OUTPUT, sensor, path_CLOUD=None):
        self.path_IMG = path_IMG
        self.path_gridPoint = path_gridPoint
        self.path_ROI = path_ROI
        self.path_OUTPUT = path_OUTPUT
        self.sensor = sensor
        self.path_CLOUD = path_CLOUD


    def run(self):
        if self.sensor == 'sd':
            # Runs the Lconnect framework for SuperDove/PlanetScope data:
            r_spectrum = AverageRSPECTRA_SD(self.path_IMG, self.path_CLOUD, self.path_gridPoint, self.path_OUTPUT)
            parameters = TIMESERIES_SD(self.path_IMG, self.path_CLOUD, self.path_ROI, r_spectrum)
            dataset = Filter().FilterParameters(parameters)
            output = Model(dataset, self.path_OUTPUT)
            output.Estimative()

        elif self.sensor == 'msi':
            # Runs the Lconnect framework for MSI/Sentinel-2 data:
            r_spectrum = AverageRSPECTRA_MSI(self.path_IMG, self.path_gridPoint, self.path_OUTPUT)
            parameters = TIMESERIES_MSI(self.path_IMG, self.path_ROI, r_spectrum)
            dataset = Filter().FilterParameters(parameters)
            output = Model(dataset, self.path_OUTPUT)
            output.Estimative()

        else:
            print('Error: Unidentified sensor. Please enter a valid name.')

