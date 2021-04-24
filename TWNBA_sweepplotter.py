import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

pd.options.mode.chained_assignment = None


class Data:
    def __init__(self, file):

        # Loading the file into a dataframe and extracting information
        self.df = pd.read_csv(file, sep='\t')

        # Adding some info about the loaded file to the class
        self.sweep = self.df.columns[0]
        self.columns = pd.Series(self.df.columns).drop(index=0).tolist()
        self.runs = int(self.df.iloc[0, 0].split('/')[1].split(')')[0])
        self.num_of_param = len(self.df.iloc[0, 0].split('=')) - 1
        list_num_of_param = [2]
        self.parameters = []
        for num in range((self.num_of_param - 1)):
            list_num_of_param.append(list_num_of_param[-1] + 2)

        slices = re.split('[ =]', self.df.iloc[0, 0])
        for num in list_num_of_param:
            self.parameters.append(slices[num])

        # Adding Columns to the DataFrame that indicate the used parameters for the values
        info_list = self.df[self.df.iloc[:, 1].isnull()].iloc[:, 0].tolist()
        self.dict_of_param = {}
        for param in self.parameters:
            self.dict_of_param[param] = []

        for key in self.dict_of_param:
            for info in info_list:
                self.dict_of_param[key].append(info.split(key + '=')[1].split(' ')[0])

        self.dict_of_unique_param = {}
        for key in self.dict_of_param:
            self.dict_of_unique_param[key] = list(dict.fromkeys(self.dict_of_param[key]))

        nans = self.df[self.df.iloc[:, 1].isnull()].iloc[:, 0].index
        self.steps = nans[1] - 1

        dict_of_indices = {}
        for param in self.parameters:
            dict_of_indices[param] = []

        for key in dict_of_indices:
            for param in self.dict_of_param[key]:
                for step in range(self.steps):
                    dict_of_indices[key].append(param)

        self.df.drop(index=nans, inplace=True)

        for key in dict_of_indices:
            self.df[key] = dict_of_indices[key]

        # Adding a DataFrame that shows all unique combinations & the number of plats necessary
        self.unique = self.df[self.parameters].drop_duplicates()
        self.combinations = len(self.unique)

        # Resolving dtype issue of the 0 column
        self.df[self.sweep] = pd.to_numeric(self.df[self.sweep])

data = Data('FBP_Case1spec.txt')
print(data.unique)