# -*- processing: LCONNECT -*-

import pandas as pd


class Model():

    def __init__(self, parameters, path_OUTPUT):
        self.parameters = parameters
        self.path_OUTPUT = path_OUTPUT

    def Estimative(self):
        """
        Applies the model to estimate the hydrological connectivity from floodplain lakes:
        :return: dataframe with connectivity status.
        """
        # Model to estimate the hydrological connectivity:
        dfMODEL = pd.read_pickle(r'doc/Model_SMOTE88_15122022.pkl')
        # Selects the similarity features:
        X = self.parameters[['sam', 'ed', 'sc', 'sid']].to_numpy()
        # Applies the model:
        model_ = dfMODEL['model'][0]
        Y = model_.predict(X)
        # Adds the connectivity status:
        self.parameters['Conn'] = Y
        # Save:
        output_ = self.parameters.drop(columns=['index'])
        name_file_output = 'OutputLakesParameters.csv'
        output_.to_csv(str(self.path_OUTPUT) + '/' + name_file_output, sep=',', index=False)
