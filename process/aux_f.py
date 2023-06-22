# -*- processing: LCONNECT -*-

import rasterio
from rasterio.mask import mask
import geopandas as gpd

class Auxiliary:

    def open_IMAGE(self, path_image: str):
        """
        Opens the image:
        :param path_image: directory of images;
        :return: codified image.
        """
        return (rasterio.open(path_image))


    def cut_IMAGE(self, image, ROI):
        """
        Cut the image using geometry:
        :param image: array;
        :param ROI: geometry of lakes.
        :return: list with array cut and image transform information.
        """
        out_image, out_transform = mask(image, shapes=ROI, crop=True, nodata=999)
        return ([out_image, out_transform])


    def open_ROI(self, path_ROI: str):
        """
        Read the shapefile geometry --lakes:
        :param path_ROI: path with ROI (region-of-interest)
        :return: list with lakes' id and geometry.
        """
        input_mask = gpd.read_file(path_ROI)
        id_lakes_ = []
        geometry_ = []
        for i, id_lake in zip(input_mask['geometry'], input_mask.index):
            r_geometry = gpd.GeoDataFrame(geometry=[i])['geometry']
            geometry_.append(r_geometry)
            id_lakes_.append(id_lake)
        return ([id_lakes_, geometry_])


    def open_GridPoints(self, path_gridPoint: str):
        """
        Opens the grid of points from river:
        :param path_gridPoint: path with grid of POINTS of main river;
        :return: list with geometry of buffers from river.
        """
        # Coordinates:
        full_data=gpd.read_file(path_gridPoint)
        geometry = []
        for point in full_data.index:
            point = full_data.loc[full_data.index == point]
            geometry_ = gpd.GeoDataFrame.buffer(point, 10)
            geometry.append(geometry_)
        return (geometry)
