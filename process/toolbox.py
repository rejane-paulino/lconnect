# -*- processing: LCONNECT -*-

import os
from osgeo import gdal
gdal.UseExceptions()
import pandas as pd
import numpy as np
import warnings

from .aux_f import Auxiliary
from .metrics import metric


def reOutliers(array_1d):
    """
    Removes the outlier values:
    :param array_1d: array with 1d dimension;
    :return: list with values free of outliers;
    """
    df_ = pd.DataFrame(array_1d)
    class_ = df_[~(df_ == 999.0)]
    # Removes the outliers -> IQR (InterQuartile Range) method:
    Q1 = class_.quantile(0.25)
    Q3 = class_.quantile(0.75)
    IQR = Q3 - Q1
    # Selects of values without the outliers:
    value_selection = class_[~((class_ < (Q1 - 1.5 * IQR)) | (class_ > (Q3 + 1.5 * IQR)))]
    return (value_selection)


def rSpectrum_SD(path_image: str, path_cloud: str, path_gridPoint: str):
    """
    It recovers the river spectrum from a single SuperDove image:
    :param path_image: path of the image;
    :param path_cloud: path of the cloud mask;
    :param path_gridPoint: path of shapefile with grid of POINTs from river;
    :return: dataframe with reference spectrum for a single image.
    """
    # Opens the spectral bands and cloud mask:
    image_ = Auxiliary().open_IMAGE(path_image)
    cloud_ = Auxiliary().open_IMAGE(path_cloud)
    # It generates the coordinates:
    riverGridPoints = Auxiliary().open_GridPoints(path_gridPoint)
    l_data_ = []
    for geo in riverGridPoints:
        try:
            # Cuts the spectral bands:
            cutRiver = Auxiliary().cut_IMAGE(image_, geo)
            factor_ = cutRiver[0] / 10000 # multiply factor.
            # Masks -> Cloud and Water:
            cutCloud_ = Auxiliary().cut_IMAGE(cloud_, geo)[0][0]
            cloudMask_ = np.where(cutCloud_ == 1, 1, 0)
            ndwi_ = (factor_[3] - factor_[7]) / (factor_[3] + factor_[7])
            ndwiMask_ = np.where(ndwi_ > 0, 1, 0)
            # Applies the masks and recovers the spectrum per point:
            r_multiply = factor_ * ndwiMask_ * cloudMask_
            for nb in range(0, 8):
                l_data_.append(np.nanmean(r_multiply[nb][r_multiply[0] > 0]))
        except:
            pass
    # Retrieves the dataframe:
    if len(l_data_):
        try:
            m_data_ = []
            for nb in range(0, 8):
                df_ = pd.DataFrame({str(path_image[-47:-43] + '-' + path_image[-43:-41] + '-' + '00'): [l_data_[nb]]}, index=[nb])
                m_data_.append(df_)
            # Joins the data:
            m_concat_ = pd.concat(m_data_)
            return (m_concat_)
        except:
            pass


def rSpectrum_MSI(path_image: str, path_gridPoint: str):
    """
    It recovers the river spectrum from a single MSI/Sentinel-2 image:
    :param path_image: path of the image;
    :param path_gridPoint: path of shapefile with grid of POINTs from river;
    :return: dataframe with reference spectrum for a single image.
    """
    # Opens the spectral bands and cloud mask:
    image_ = Auxiliary().open_IMAGE(path_image)
    # It generates the coordinates:
    riverGridPoints = Auxiliary().open_GridPoints(path_gridPoint)
    l_data_ = []
    for geo in riverGridPoints:
        try:
            # Cuts the spectral bands:
            cutRiver = Auxiliary().cut_IMAGE(image_, geo)
            factor_ = cutRiver[0]
            # Masks -> Water:
            ndwi_ = (factor_[1] - factor_[6]) / (factor_[1] + factor_[6])
            ndwiMask_ = np.where(ndwi_ > 0, 1, 0)
            # Applies the masks and recovers the spectrum per point:
            r_multiply = factor_ * ndwiMask_
            for nb in range(0, 7):
                l_data_.append(np.nanmean(r_multiply[nb][r_multiply[0] > 0]))
        except:
            pass
    # Retrieves the dataframe:
    if len(l_data_):
        try:
            m_data_ = []
            for nb in range(0, 7):
                df_ = pd.DataFrame({str(path_image[-12:-8] + '-' + path_image[-8:-6] + '-' + '00'): [l_data_[nb]]}, index=[nb])
                m_data_.append(df_)
            # Joins the data:
            m_concat_ = pd.concat(m_data_)
            return (m_concat_)
        except:
            pass


def AverageRSPECTRA_SD(path_IMG: str, path_CLOUD: str, path_gridPoint: str, path_OUTPUT: str):
    """
    Generates the average spectrum of River reference from a GridPoint:
    :param path_IMG: directory with images;
    :param path_CLOUD: directory with cloud mask;
    :param path_gridPoint: path of shapefile with grid of POINTs from river;
    :param path_OUTPUT: directory of output;
    :return: dataframe with reference spectra from river for different months.
    """
    # Verifies the id:
    dates_ = []
    for b_i in os.listdir(path_IMG):
        if '.tif' in b_i and 'udm2' not in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            dates_.append(b_i)
    datesCloud_ = []
    for b_i in os.listdir(path_CLOUD):
        if '.tif' in b_i and 'udm2' in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            datesCloud_.append(b_i)
    # Gets the reference dates:
    y_month = [str(dates_[0][0:4]) + str(dates_[0][4:6])]
    for i in dates_:
        if str(i[0:4]) + str(i[4:6]) in y_month:
            'None--'
        else:
            y_month.append(str(i[0:4]) + str(i[4:6]))
    # Retrievals the spectra:
    dates_.sort()
    datesCloud_.sort()
    l_data__ = []
    if len(dates_) != len(datesCloud_):
        print('Error: the number of UDM2 masks is not valid!')
    else:
        for dtImage, dtCloud in zip(dates_, datesCloud_):
            warnings.filterwarnings("ignore")
            rspectrum = rSpectrum_SD(path_image=path_IMG + '/' + dtImage,
                                     path_cloud=path_CLOUD + '/' + dtCloud,
                                     path_gridPoint=path_gridPoint)
            l_data__.append(rspectrum)
    # It calculates the reference river spectrum (Average Spectrum):
    l_data_ = [i for i in l_data__ if i is not None]
    if len(l_data_):
        try:
            # Joins the all data:
            output = [l_data_[0]]
            for int_i in range(1, len(l_data_)):
                merge_ = output[-1].merge(l_data_[int_i], left_index=True, right_index=True)
                output.append(merge_)
            transpose = output[-1].transpose()
            l_mean = []
            for i in y_month:
                filter = transpose[transpose.index.str.contains(i[:4] + '-' + i[4:6])]
                mean = np.mean(filter)
                df = pd.DataFrame({i[:4] + '-' + i[4:6] + '-' + '00': mean}).transpose()
                l_mean.append(df)
            concat = pd.concat(l_mean).transpose()
            # Save:
            name_file_output = 'reference_spectra.csv'
            concat.to_csv(path_OUTPUT + '/' + name_file_output, sep=',')
            return (concat)
        except:
            pass


def AverageRSPECTRA_MSI(path_IMG: str, path_gridPoint: str, path_OUTPUT: str):
    """
    Generates the average spectrum of River reference from a GridPoint:
    :param path_IMG: directory with images;
    :param path_gridPoint: path of shapefile with grid of POINTs from river;
    :param path_OUTPUT: directory of output;
    :return: dataframe with reference spectra from river for different months.
    """
    # Verifies the id:
    dates_ = []
    for b_i in os.listdir(path_IMG):
        if '.tif' in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            dates_.append(b_i)
    # Gets the reference dates:
    y_month = [str(dates_[0][0:4]) + str(dates_[0][4:6])]
    for i in dates_:
        if str(i[0:4]) + str(i[4:6]) in y_month:
            'None--'
        else:
            y_month.append(str(i[0:4]) + str(i[4:6]))
    # Retrievals the spectra:
    dates_.sort()
    l_data__ = []
    for dtImage in dates_:
        warnings.filterwarnings("ignore")
        rspectrum = rSpectrum_MSI(path_image=path_IMG + '/' + dtImage,
                                  path_gridPoint=path_gridPoint)
        l_data__.append(rspectrum)
    # It calculates the reference river spectrum (Average Spectrum):
    l_data_ = [i for i in l_data__ if i is not None]
    if len(l_data_):
        try:
            # Joins the all data:
            output = [l_data_[0]]
            for int_i in range(1, len(l_data_)):
                merge_ = output[-1].merge(l_data_[int_i], left_index=True, right_index=True)
                output.append(merge_)
            transpose = output[-1].transpose()
            l_mean = []
            for i in y_month:
                filter = transpose[transpose.index.str.contains(i[:4] + '-' + i[4:6])]
                mean = np.mean(filter)
                df = pd.DataFrame({i[:4] + '-' + i[4:6] + '-' + '00': mean}).transpose()
                l_mean.append(df)
            concat = pd.concat(l_mean).transpose()
            # Save:
            name_file_output = 'reference_spectra.csv'
            concat.to_csv(path_OUTPUT + '/' + name_file_output, sep=',')
            return (concat)
        except:
            pass


def LakeByDate_SD(input_path_band_IMG: str, input_path_band_CLOUD: str, path_ROI: str, r_spectrum, date: str):
    """
    It recovers the parameters for each lake in a specific date:
    :param input_path_band_IMG: path of image;
    :param input_path_band_CLOUD: path of cloud mask;
    :param path_ROI: path of file .shp with lakes' surface;
    :param r_spectrum: dataframe with reference spectra;
    :param date: date of images;
    :return: dataframe with different parameters from lakes for a single date;
    """
    # Opens the satellite-image and cloud-data:
    image_ = Auxiliary().open_IMAGE(input_path_band_IMG)
    cloud_ = Auxiliary().open_IMAGE(input_path_band_CLOUD) # Takes into count the 'CLEAR' class.
    # Opens the geometry of lakes:
    lakeMask_ = Auxiliary().open_ROI(path_ROI)
    # Cuts the SAM's array from the lake array. It returns the minimum SAM value:
    l_out_ = []
    for n_lake, geo_ in zip(lakeMask_[0], lakeMask_[1]):
        try:
            # Opens the data and prepares the cloud mask:
            cutImage_ = Auxiliary().cut_IMAGE(image_, geo_)[0] / 10000 # Apply to factor.
            cutCloud_ = Auxiliary().cut_IMAGE(cloud_, geo_)[0][0]
            # Builts the mask - cloud and water:
            ndwi_ = (cutImage_[3] - cutImage_[7]) / (cutImage_[3] + cutImage_[7])
            ndwiMask_ = np.where(ndwi_ > 0, 1, 0)
            cloudMask_ = np.where(cutCloud_ == 1, 1, 0)
            # Calculates the features -- SAM | ED | SC | SID:
            FEATURES = metric()
            sam = FEATURES.SAM(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 8)
            ed = FEATURES.ED(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 8)
            sc = FEATURES.SC(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 8)
            sid = FEATURES.SID(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 8)
            # Applies the masks:
            # Applied NDWI to remove other effects like adjacency - threshold in 0:
            productSAM_ = sam * ndwiMask_ * cloudMask_
            maskNaN_ = np.where(productSAM_ == 0, 999, productSAM_)
            # Recoveries the minimum SAM over the lake:
            rOutliers_ = reOutliers(array_1d=maskNaN_.flatten())
            min_sam_ = np.min(rOutliers_)
            if np.all(np.isnan(min_sam_)):
                min_sam_ = 999.0
            else:
                min_sam_ = min_sam_
            # Recoveries the row/column of minimum-SAM:
            index = np.argwhere(maskNaN_ == float(min_sam_)).flatten()
            ed_set = ed[index[0], index[1]]
            sc_set = sc[index[0], index[1]]
            sid_set = sid[index[0], index[1]]
            # Recoveries the lake spectrum:
            l_spectrum = []
            for i in range(0, 8):
                l_spectrum.append(cutImage_[i][index[0], index[1]])
            # Builds the dataframe with data:
            df_ = pd.DataFrame({'date': str(date[0:4]) + '-' + str(date[4:6]) + '-' + str(date[6:8]), 'id_lake': str(n_lake),
                                'sam': float(min_sam_), 'ed': float(ed_set), 'sc': float(sc_set), 'sid': float(sid_set),
                                '441': [float(l_spectrum[0])], '490': [float(l_spectrum[1])], '531': [float(l_spectrum[2])], '565': [float(l_spectrum[3])],
                                '610': [float(l_spectrum[4])], '665': [float(l_spectrum[5])], '705': [float(l_spectrum[6])], '865': [float(l_spectrum[7])]}
                               )
            l_out_.append(df_)
        except:
            pass
    # Join the data:
    if len(l_out_):
        output_ = pd.concat(l_out_)
        return (output_)
    else:
        return (None)


def LakeByDate_MSI(input_path_band_IMG: str, path_ROI: str, r_spectrum, date: str):
    """
    It recovers the parameters for each lake in a specific date:
    :param input_path_band_IMG: path of image;
    :param path_ROI: path of file .shp with lakes' surface;
    :param r_spectrum: dataframe with reference spectra;
    :param date: date of images;
    :return: dataframe with different parameters from lakes for a single date;
    """
    # Opens the satellite-image and cloud-data:
    image_ = Auxiliary().open_IMAGE(input_path_band_IMG)
    # Opens the geometry of lakes:
    lakeMask_ = Auxiliary().open_ROI(path_ROI)
    # Cuts the SAM's array from the lake array. It returns the minimum SAM value:
    l_out_ = []
    for n_lake, geo_ in zip(lakeMask_[0], lakeMask_[1]):
        try:
            # Opens the data and prepares the cloud mask:
            cutImage_ = Auxiliary().cut_IMAGE(image_, geo_)[0]
            # Builts the mask - cloud and water:
            ndwi_ = (cutImage_[1] - cutImage_[6]) / (cutImage_[1] + cutImage_[6])
            ndwiMask_ = np.where(ndwi_ > 0, 1, 0)
            # Calculates the features -- SAM | ED | SC | SID:
            FEATURES = metric()
            sam = FEATURES.SAM(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 7)
            ed = FEATURES.ED(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 7)
            sc = FEATURES.SC(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 7)
            sid = FEATURES.SID(cutImage_, r_spectrum[str(date[:4] + '-' + date[4:6] + '-' + '00')], 7)
            # Applies the masks:
            # Applied NDWI to remove other effects like adjacency - threshold in 0:
            productSAM_ = sam * ndwiMask_
            maskNaN_ = np.where(productSAM_ == 0, 999, productSAM_)
            # Recoveries the minimum SAM over the lake:
            rOutliers_ = reOutliers(array_1d=maskNaN_.flatten())
            min_sam_ = np.min(rOutliers_)
            if np.all(np.isnan(min_sam_)):
                min_sam_ = 999.0
            else:
                min_sam_ = min_sam_
            # Recoveries the row/column of minimum-SAM:
            index = np.argwhere(maskNaN_ == float(min_sam_)).flatten()
            ed_set = ed[index[0], index[1]]
            sc_set = sc[index[0], index[1]]
            sid_set = sid[index[0], index[1]]
            # Recoveries the lake spectrum:
            l_spectrum = []
            for i in range(0, 7):
                l_spectrum.append(cutImage_[i][index[0], index[1]])
            # Builds the dataframe with data:
            df_ = pd.DataFrame({'date': str(date[0:4]) + '-' + str(date[4:6]) + '-' + str(date[6:8]), 'id_lake': str(n_lake),
                                'sam': float(min_sam_), 'ed': float(ed_set), 'sc': float(sc_set), 'sid': float(sid_set),
                                '490': [float(l_spectrum[0])], '560': [float(l_spectrum[1])], '665': [float(l_spectrum[2])], '705': [float(l_spectrum[3])],
                                '740': [float(l_spectrum[4])], '783': [float(l_spectrum[5])], '842': [float(l_spectrum[6])]}
                               )
            l_out_.append(df_)
        except:
            pass
    # Join the data:
    if len(l_out_):
        output_ = pd.concat(l_out_)
        return (output_)
    else:
        return (None)


def TIMESERIES_SD(path_IMG: str, path_CLOUD: str, path_ROI: str, r_spectrum):
    """
    It recovers the parameters for each lake along the time-series:
    :param path_IMG: directory with images;
    :param path_CLOUD: directory with cloud mask;
    :param path_ROI: path of file .shp with lake's surface;
    :param r_spectrum: dataframe with reference spectra;
    :return: dataframe with different parameters from lakes along the time-series.
    """
    # Verifies the id:
    dates_ = []
    for b_i in os.listdir(path_IMG):
        if '.tif' in b_i and 'udm2' not in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            dates_.append(b_i)
    datesCloud_ = []
    for b_i in os.listdir(path_CLOUD):
        if '.tif' in b_i and 'udm2' in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            datesCloud_.append(b_i)
    # Retrievals the spectra:
    dates_.sort()
    datesCloud_.sort()
    l_data_ = []
    if len(dates_) != len(datesCloud_):
        print('Error: the number of UDM2 masks is not valid!')
    else:
        # Retrievals the lake's parameters for all dates:
        for dtImage, dtCloud in zip(dates_, datesCloud_):
            lake_parameters = LakeByDate_SD(input_path_band_IMG=path_IMG + '/' + dtImage,
                                            input_path_band_CLOUD=path_CLOUD + '/' + dtCloud,
                                            path_ROI=path_ROI,
                                            r_spectrum=r_spectrum,
                                            date=str(dtImage[0:8]))
            l_data_.append(lake_parameters)
    # Joins the data:
    if all(i is None for i in l_data_) == True:
        'None__'
    else:
        output_ = pd.concat(l_data_).reset_index()
        return (output_)


def TIMESERIES_MSI(path_IMG: str, path_ROI: str, r_spectrum):
    """
    It recovers the parameters for each lake along the time-series:
    :param path_IMG: directory with images;
    :param path_ROI: path of file .shp with lake's surface;
    :param r_spectrum: dataframe with reference spectra;
    :return: dataframe with different parameters from lakes along the time-series.
    """
    # Verifies the id:
    dates_ = []
    for b_i in os.listdir(path_IMG):
        if '.tif' in b_i and '.txt' not in b_i and '.aux' not in b_i and '.ovr' not in b_i:
            dates_.append(b_i)
    # Retrievals the spectra:
    dates_.sort()
    l_data_ = []
    # Retrievals the lake's parameters for all dates:
    for dtImage in dates_:
        lake_parameters = LakeByDate_MSI(input_path_band_IMG=path_IMG + '/' + dtImage,
                                         path_ROI=path_ROI,
                                         r_spectrum=r_spectrum,
                                         date=str(dtImage[0:8]))
        l_data_.append(lake_parameters)
    # Joins the data:
    if all(i is None for i in l_data_) == True:
        'None__'
    else:
        output_ = pd.concat(l_data_).reset_index()
        return (output_)

