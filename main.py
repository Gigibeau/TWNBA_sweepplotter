import numpy as np
import pandas as pd

class Data:
    def __init__(self, file):

        # Loading the file into a dataframe and extracting information (runs, elec, rho)
        df = pd.read_csv(file, sep='\t')
        self.runs = int(df.iloc[0, 0].split('/')[1].split(')')[0])
        try:
            self.elec = df.iloc[0, 0].split('Elec=')[1].split(' ')[0]
            self.rho = df.iloc[0, 0].split('Rho=')[1].split(' ')[0]
        except(IndexError):
            pass

        # Seperating the measured values into pandas series
        i_vs = df.iloc[1:, 0]
        r_rs = df.iloc[1:, 1]
        r_vs = df.iloc[1:, 2]
        r_vs_rs = df.iloc[1:, 3]

        # Putting the desired dataframes together
        nans = r_rs[r_rs.isnull()].index
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

        self.df_r_rs = rearrange_to_dataframe(r_rs)
        self.df_r_vs = rearrange_to_dataframe(r_vs)
        self.df_r_vs_rs = rearrange_to_dataframe(r_vs_rs)

        self.sweep = i_vs[0:self.steps].reset_index(drop=True)

case1 = Data('FBP_Case1spec.txt')
case6 = Data('FBP_Case6_spec.txt')
case18 = Data('LIP_Case18spec.txt')

print('hi')