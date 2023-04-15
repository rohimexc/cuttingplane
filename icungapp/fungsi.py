from koefisien import koefisien
from simpleks import simplex_tableau
import numpy as np
import pandas as pd
fungsikendala={
    'y1':'150X1+150X2+300X3<=25000',
    'y2':'15X1+15X2+30X3<=15000',
    'y3':'30X1+30X2+60X3<=50000',
    'y4':'50X1+50X2+100X3<=12000',
    'y5':'7.5X1+7.5X2+15X3<=25000',
    'y6':'2.25X1+2.25X2+4.5X3<=200',
    'y7':'9.4X1+9.4X2+18.8X3<=4096',
    'y8':'1.5X1+1.5X2+3X3<=1500',
    'y9':'5.6X1+2.2X2+0X3<=15000',
    'y10':'0X1+3X2+0X3<=10000',
    'y11':'0X1+0X2+6X3<=5000',
    'y12':'1X1+0X2+0X3>=20',
    'y13':'0X1+1X2+0X3>=20',
    'y14':'0X1+0X2+1X3>=10',
}
fungsitujuan= '40000X1+40000X2+40000X3'
header,indeks,data=koefisien(fungsikendala,fungsitujuan)

df = pd.DataFrame(data,columns=header) 
df = df.set_index('vd') 
df = df.reset_index()
df['vd'] = indeks
df = df.set_index('vd')
df = df.replace("M",np.nan)


while True:
    try:
        df = simplex_tableau(df)
        not_negative = (df.loc['z', :] >= 0).all()
        if not_negative:
            df = df.round(4)
            break
        else:
            df = simplex_tableau(df)
            df = df.round(4)
            print(df)
    except Exception as e:
        print(f"An error occurred: {e}")
        break

