import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.mode.chained_assignment = None


class Data:
    def __init__(self, file):

        # Loading the file into a dataframe and extracting information
        self.df = pd.read_csv(file, sep='\t')

        # Adding some info about the loaded file to the class
        self.sweep = self.df.columns[0]
        self.columns = pd.Series(self.df.columns).drop(index=0).tolist()
        self.runs = int(self.df.iloc[0, 0].split('/')[1].split(')')[0])

        # Add 2 Columns to the DataFrame that indicate the used parameters in the run
        info_list = self.df[self.df.iloc[:, 1].isnull()].iloc[:, 0].tolist()
        elec_list = []
        rho_list = []
        irs_list = []

        for info in info_list:
            try:
                elec_list.append(info.split('Elec=')[1].split(' ')[0])
            except IndexError:
                elec_list.append('None')
            try:
                rho_list.append(info.split('Rho=')[1].split(' ')[0])
            except IndexError:
                rho_list.append('None')
            try:
                irs_list.append(info.split('I_rs=')[1].split(' ')[0])
            except IndexError:
                irs_list.append('None')


        self.elecs = list(dict.fromkeys(elec_list))
        self.rhos = list(dict.fromkeys(rho_list))
        self.irs = list(dict.fromkeys(rho_list))

        nans = self.df[self.df.iloc[:, 1].isnull()].iloc[:, 0].index
        self.steps = nans[1] - 1

        elec_index = []
        for parameter in elec_list:
            for step in range(self.steps):
                elec_index.append(parameter)

        rho_index = []
        for parameter in rho_list:
            for step in range(self.steps):
                rho_index.append(parameter)

        irs_index = []
        for parameter in irs_list:
            for step in range(self.steps):
                irs_index.append(parameter)

        self.df.drop(index=nans, inplace=True)

        self.df['elec'] = elec_index
        self.df['rho'] = rho_index
        self.df['irs'] = irs_index

        # Adding a DataFrame that shows all unique combinations & the number of plats necessary
        self.unique = self.df[['elec', 'rho', 'irs']].drop_duplicates()
        self.combinations = len(self.unique)

        # Resolving dtype issue of the 0 column
        self.df[self.sweep] = pd.to_numeric(self.df[self.sweep])


def lineplot(data, prime_parameters):
    ax = 0  # just to prevent errors
    if prime_parameters == 'elec':
        if len(data.elecs) == 4:
            fig, ax = plt.subplots(2, 2, figsize=(10, 10))

        if len(data.elecs) == 6:
            fig, ax = plt.subplots(3, 3, figsize=(10, 10))

        fig_count = 0
        for i, axes in enumerate(ax.flat):
            df_to_plot = data.df[(data.df["elec"] == data.elecs[fig_count])]
            sns.lineplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue="rho", ax=axes)
            axes.set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel='Plating Current $I_{RS}$(A)',
                     ylabel='$C_{FS/RS}$', title='$R_{rho}$ =' + data.elecs[fig_count] + '\u03A9')
            fig_count += 1

    if prime_parameters == 'rho':
        if len(data.rhos) == 4:
            fig, ax = plt.subplots(2, 2, figsize=(10, 10))

        if len(data.rhos) == 6:
            fig, ax = plt.subplots(3, 3, figsize=(10, 10))

        fig_count = 0
        for i, axes in enumerate(ax.flat):
            df_to_plot = data.df[(data.df["rho"] == data.rhos[fig_count])]
            sns.lineplot(data=df_to_plot, x=data.sweep, y="I(R_vs)/I(R_rs)", hue="elec", ax=axes)
            axes.set(ylim=(0.1, 10), xscale="log", yscale="log", xlabel='Plating Current $I_{RS}$(A)',
                     ylabel='$C_{FS/RS}$', title='$R_{rho}$ =' + data.rhos[fig_count] + '\u03A9')
            fig_count += 1

    plt.show()


data = Data('FBP_Case6spec.txt')
print(data.df)
#lineplot(data, 'rho')
