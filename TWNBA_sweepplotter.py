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

        # Adding a DataFrame that shows all unique combinations & the total number
        self.unique = self.df[self.parameters].drop_duplicates()
        self.combinations = len(self.unique)

        # Resolving dtype issue of the 0 column
        self.df[self.sweep] = pd.to_numeric(self.df[self.sweep])


def lineplot(data, num_plots, position1, position2, hue, first_param, first_value, second_param='None', second_value='None'):
    ax = 0  # just to prevent errors
    if num_plots == 4:
        fig, ax = plt.subplots(2, 2, figsize=(10, 10))

    if num_plots == 9:
        fig, ax = plt.subplots(3, 3, figsize=(10, 10))

    if second_param == 'None':
        df_to_plot = data.df[(data.df[first_param] == first_value)]
    else:
        df_to_plot = data.df[(data.df[first_param] == first_value) & (data.df[second_param] == second_value)]

    sns.lineplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue=hue, ax=ax[position1, position2])
    ax[position1, position2].set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel='Sweep',
                                 ylabel='Parameter 2', title='Parameter 1')

    plt.show()
    return fig


#data_test = Data('FBP_Case1spec.txt')
#print(data_test.dict_of_unique_param)
#print(data.parameters)
#lineplot(data_test, 6, 0, 0, 'I_rs', 'Elec', '100m', 'Rho', '100m')
