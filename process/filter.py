# -*- processing: LCONNECT -*-

import pandas as pd
import numpy as np


class Filter:

    def FilterParameters (self, parameters):
        """ Removes the NaN values and duplicated dates from parameters:
        :param parameters: dataframe with all parameters;
        :param path_OUTPUT: directory of output;
        :return: filtered dataframe.
        """
        # Gets the lakes id:
        nLakes_ = [parameters['id_lake'][0]]
        for i in parameters['id_lake']:
            if str(i) in nLakes_:
                'None--'
            else:
                nLakes_.append(str(i))
        # Filters the data:
        l_data_ = []
        for nlake in nLakes_:
            # Filters per lake's id:
            filter_nLake_ = parameters.loc[parameters['id_lake'] == nlake]
            # Filters the date:
            l_dateCol_ = filter_nLake_.loc[filter_nLake_['sam'] != 999]['date']
            l_date = []
            for i in l_dateCol_:
                if len(l_date) == 0:
                    l_date.append(str(i))
                else:
                    if str(i) in l_date:
                        'None--'
                    else:
                        l_date.append(i)
            # Filters per date from minimum SAM:
            for dt_ in l_date:
                filter_dt_ = filter_nLake_.loc[filter_nLake_['date'] == str(dt_)]
                filter_mSAM_ = filter_dt_.loc[filter_dt_['sam'] == np.min(filter_dt_['sam'])]
                l_data_.append(filter_mSAM_)
        # Output:
        output_ = pd.concat(l_data_)
        return (output_)
