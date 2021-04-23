import numpy as np
import pandas as pd

class Data:
    def __init__(self, file):

        # Loading the file into a dataframe and extracting information
        df = pd.read_csv(file, sep='\t')
        columns = pd.Series(df.columns).drop(index=0)

        self.dict_of_measurements = {}
        count = 0
        for column in df.columns:
            self.dict_of_measurements[column] = df.iloc[1:, count]
            count += 1

        self.sweep = df.columns[0]
        self.runs = int(df.iloc[0, 0].split('/')[1].split(')')[0])
        try:
            self.elec = df.iloc[0, 0].split('Elec=')[1].split(' ')[0]
            self.rho = df.iloc[0, 0].split('Rho=')[1].split(' ')[0]
        except(IndexError):
            pass

        # Putting the desired dataframes together
        nans = self.dict_of_measurements[columns[1]][self.dict_of_measurements[columns[1]].isnull()].index
        self.steps = nans[0] - 1

        def rearrange_to_dataframe(series):
            counter = 0
            span = counter + self.steps
            desired_df = pd.DataFrame(series.iloc[counter:span]).reset_index(drop=True)
            while counter < (len(series) - self.steps):
                counter = span + 1
                span = counter + self.steps
                temp_df = pd.DataFrame(series.iloc[counter:span]).reset_index(drop=True)
                desired_df = pd.concat([desired_df, temp_df], axis=1)
            desired_df.columns = range(self.runs)
            return desired_df

        self.dict_of_df = {}
        for column in columns:
            self.dict_of_df[column] = rearrange_to_dataframe(self.dict_of_measurements[column])

        self.dict_of_df[df.columns[0]] = self.dict_of_measurements[df.columns[0]][0:self.steps].reset_index(drop=True)


case1 = Data('FBP_Case1spec.txt')
case6 = Data('FBP_Case6_spec.txt')
case18 = Data('LIP_Case18spec.txt')

