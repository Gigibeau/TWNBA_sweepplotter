import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

pd.options.mode.chained_assignment = None

# Parameters
global fig
global ax
first_digit_4 = [0, 0, 1, 1]
second_digit_4 = [0, 1, 0, 1]
first_digit_9 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
second_digit_9 = [0, 1, 2, 0, 1, 2, 0, 1, 2]


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


def set_grid(num_plots):
    global fig, ax
    if num_plots == 4:
        fig, ax = plt.subplots(2, 2, figsize=(10, 8))

    if num_plots == 9:
        fig, ax = plt.subplots(3, 3, figsize=(10, 8))

    if num_plots == 1:
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))


def lineplot(data, position1, position2, hue, first_param, first_value, second_param='None', second_value='None'):
    if second_param == 'None':
        df_to_plot = data.df[(data.df[first_param] == first_value)]
        second_param = ' '
        second_value = ' '
    else:
        df_to_plot = data.df[(data.df[first_param] == first_value) & (data.df[second_param] == second_value)]

    if position1 == 'None':
        sns.lineplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue=hue
                     ).legend(fontsize=5, frameon=False)
        ax.set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel=data.sweep,
               ylabel=(second_param + ' ' + second_value), title=(first_param + ' ' + first_value))

    else:
        sns.lineplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue=hue,
                     ax=ax[position1, position2]).legend(fontsize=5, frameon=False)
        ax[position1, position2].set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel=data.sweep,
                                     ylabel=(second_param + ' ' + second_value),
                                     title=(first_param + ' ' + first_value))

    fig.tight_layout()
    return fig


def kdeplot(data, position1, position2, hue, first_param, first_value, second_param='None', second_value='None'):
    if second_param == 'None':
        df_to_plot = data.df[(data.df[first_param] == first_value)]
        second_param = ' '
        second_value = ' '
    else:
        df_to_plot = data.df[(data.df[first_param] == first_value) & (data.df[second_param] == second_value)]

    if position1 == 'None':
        sns.kdeplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue=hue
                    ).legend(fontsize=5, frameon=False)
        ax.set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel=data.sweep,
               ylabel=(second_param + ' ' + second_value), title=(first_param + ' ' + first_value))

    else:
        sns.kdeplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue=hue,
                    ax=ax[position1, position2]).legend(fontsize=5, frameon=False)
        ax[position1, position2].set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel=data.sweep,
                                     ylabel=(second_param + ' ' + second_value),
                                     title=(first_param + ' ' + first_value))

    fig.tight_layout()
    return fig


def save_plot(name, num_plots):
    plt.savefig(name)

    name_num = 1
    if num_plots == 4:
        for x in range(4):
            extent = ax[first_digit_4[x], second_digit_4[x]].get_window_extent().transformed(
                fig.dpi_scale_trans.inverted())
            fig.savefig(name + '_' + str(name_num) + '.png', bbox_inches=extent.expanded(1.32, 1.3))
            name_num += 1

    if num_plots == 9:
        for x in range(9):
            extent = ax[first_digit_9[x], second_digit_9[x]].get_window_extent().transformed(
                fig.dpi_scale_trans.inverted())
            fig.savefig(name + '_' + str(name_num) + '.png', bbox_inches=extent.expanded(1.32, 1.3))
            name_num += 1
