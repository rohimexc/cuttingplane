import numpy as np
import pandas as pd

def cutting_plane(tabelhasilsimpleks, index_list_x, iterasi):
    try:
        index_list_x = [val for val in index_list_x if val.startswith('x')]
        index_float = tabelhasilsimpleks.index[tabelhasilsimpleks.index.isin(index_list_x) & ~tabelhasilsimpleks['kons'].apply(float.is_integer)].tolist()
        print(index_list_x)
        value_float = tabelhasilsimpleks.loc[index_list_x, 'kons'][~tabelhasilsimpleks['kons'].apply(float.is_integer)].tolist()
        #cari value dengan nilai rendah
        pecahan_list=[]
        for v in (value_float):
            aja=v-int(v)
            pecahan_list.append(aja)
        pecahan_list.reverse()
        pecahan_terkecil=min(pecahan_list)
        # Get index of pecahan_terkecil
        index_of_pt= pecahan_list.index(pecahan_terkecil)
        tabelhasilsimpleks.loc[f'sg{iterasi}'] = tabelhasilsimpleks.loc[index_float[index_of_pt]]
        tabelhasilsimpleks[f'sg{iterasi}'] = 0

        sg = tabelhasilsimpleks.loc[f'sg{iterasi}'].tolist()
        new_sg=[]
        for a in sg:
            if a >= 0:
                fraction = a - int(a)
            else:
                fraction = int(a) - 1 - a
            new_sg.append(round(fraction,4)*-1)
        tabelhasilsimpleks.loc[f'sg{iterasi}'] = new_sg
        tabelhasilsimpleks.loc[f'sg{iterasi}',f'sg{iterasi}'] = 1

        tabelhasilsimpleks.loc['ratio']=tabelhasilsimpleks.loc['z'] / tabelhasilsimpleks.loc[f'sg{iterasi}']
        tabelhasilsimpleks.loc['ratio'] = tabelhasilsimpleks.loc['ratio'].replace(-np.inf, np.nan)
        #cari kolom kunci
        print(tabelhasilsimpleks)
        row_a1 = tabelhasilsimpleks.loc['ratio', tabelhasilsimpleks.columns != 'kons']
        
        # Remove the last column from row_a1_abs
        row_a1_abs = row_a1.abs()
        
        row_a1_abs_no_last = row_a1_abs.iloc[:-1]
        print(row_a1_abs_no_last)
        min_ratio = row_a1_abs_no_last[row_a1_abs_no_last.index.str[0] != 'a'].min()
        print('min_ratio',min_ratio)
        kolomkunci = row_a1_abs[row_a1_abs == min_ratio].index[0]
        #kolomkunci = row_a1[row_a1 == min_neg].index[0]
        print('kolomkunci',kolomkunci)
        #cari angka kunci
        bariskunci=f'sg{iterasi}'
        angkakunci=tabelhasilsimpleks.loc[bariskunci,kolomkunci]
        print('angkakunci',angkakunci)
        tabelbaru=tabelhasilsimpleks.copy()
        tabelbaru=tabelbaru.round(2)
        tabelbaru.loc[bariskunci, :] = tabelbaru.loc[bariskunci, :] / angkakunci
        for index, row in tabelbaru.iterrows():
          if index != bariskunci:
            tabelbaru.loc[index,:]=tabelbaru.loc[index,:]-(tabelbaru.loc[bariskunci,:]*row[kolomkunci])
        tabelbaru = tabelbaru.rename(index={bariskunci: kolomkunci})
        tabelbaru=tabelbaru.round(2)
        iterasi=iterasi+1
        return tabelbaru,value_float,index_float,kolomkunci,iterasi
    except KeyError as e:
        print(f"Terjadi kesalahan KeyError: {e}")
        return None, None,None,None,iterasi
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None,None,None,None,iterasi

    
    