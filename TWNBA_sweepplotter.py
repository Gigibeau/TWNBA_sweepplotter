import pandas as pd
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

        for info in info_list:
            try:
                elec_list.append(info.split('Elec=')[1].split(' ')[0])
            except IndexError:
                elec_list.append('None')
            try:
                rho_list.append(info.split('Rho=')[1].split(' ')[0])
            except IndexError:
                rho_list.append('None')

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

        self.df.drop(index=nans, inplace=True)

        self.df['elec'] = elec_index
        self.df['rho'] = rho_index

        # Adding a DataFrame that shows all unique combinations & the number of plats necessary
        self.unique = self.df[['elec', 'rho']].drop_duplicates()
        self.combinations = len(data.unique)

data = Data('FBP_Case6spec.txt')
print(len(data.unique))

