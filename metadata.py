# -*- processing: LCONNECT -*-

import pandas as pd


class Metadata():

    def __init__(self, path_IMG, path_CLOUD, path_gridPoint, path_ROI, path_OUTPUT, sensor):
        self.path_IMG = path_IMG
        self.path_CLOUD = path_CLOUD
        self.path_gridPoint = path_gridPoint
        self.path_ROI = path_ROI
        self.path_OUTPUT = path_OUTPUT
        self.sensor = sensor


    def loadMetadata(self):
        dInput = pd.read_csv(r'./parameters.txt', sep=';')
        self.path_IMG = str(dInput.iloc[0][1]).strip()
        self.path_CLOUD = str(dInput.iloc[1][1]).strip()
        self.path_gridPoint = str(dInput.iloc[2][1]).strip()
        self.path_ROI = str(dInput.iloc[3][1]).strip()
        self.path_OUTPUT = str(dInput.iloc[4][1]).strip()
        self.sensor = str(dInput.iloc[5][1]).strip()


class ManualParameter(Metadata):

    def __init__(self):
        super(ManualParameter, self).loadMetadata()

