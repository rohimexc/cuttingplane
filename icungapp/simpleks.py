import numpy as np
import pandas as pd
def simplex_tableau(df):
    df = df.replace("M",np.nan)
    column_min = df.idxmin(axis=1)
    kolomkunci = column_min.loc['z']
    df['ratio'] =  df['kons'] / df[kolomkunci]
    positive_result = df[df["ratio"] > 0]
    smallest_positive = positive_result["ratio"].idxmin()
    bariskunci = df.loc[smallest_positive, :]
    bariskunci = bariskunci.name
    angkakunci = df.loc[bariskunci, kolomkunci]
    df2 = df.copy()
    databariskunci=[]
    databariskunci.append(bariskunci)
    df2.loc[bariskunci, :] = df2.loc[bariskunci, :] / angkakunci
    for index, row in df2.iterrows():
      if index != bariskunci:
        df2.loc[index,:]=df2.loc[index,:]-(df2.loc[bariskunci,:]*row[kolomkunci])
    df2 = df2.rename(index={bariskunci: kolomkunci})
    return df2