import numpy as np
import pandas as pd
import re

def koefisien(fungsikendala,fungsitujuan):
  slack = ['+0S{}'.format(a+1) for a in range(sum(['<=' in x for x in fungsikendala.values()]))]
  #variabel surplus
  surplus1 = ['-0S{}+0A{}'.format(len(slack)+a+1,a+1) for a in range(sum(['>=' in x for x in fungsikendala.values()]))]
  surplus2 = ['+0A{}'.format(a+1) for a in range(sum(['>=' in x for x in fungsikendala.values()]))]

  slacktujuan=['+0S{}'.format(a+1) for a in range(len(fungsikendala))]
  surplustujuan = ['-MA{}'.format(a+1) for a in range(sum(['>=' in x for x in fungsikendala.values()]))]
  gabungkendala= ''.join(slack+surplus2)
  gabungtujuan = ''.join(slacktujuan + surplustujuan)
  #fungsi tujuan gabung dengan var tambahan
  fungsitujuan = fungsitujuan + gabungtujuan

  aaa = [slacktujuan+surplus2] * len(fungsikendala)
  aaa = np.array(aaa)
  listkendala = list(fungsikendala.values())
  for a in range(len(listkendala)):
    for b in range(len(aaa)):
      if '<=' in listkendala[a]:
        if a==b:
          aaa[a][a] = f"+1S{a+1}"
      elif '>=' in listkendala[a]:
        j=1
        if a==b:
          j=j+1
          k=len(surplus2)
          aaa[a][a] = f"-N1S{a+1}"
          aaa[a][a+k] = f"+1A{a-len(slack)+1}"

  result = []
  for sublist in aaa:
    result.append(''.join(sublist))
  siapsimpleks=[]
  listkendala = list(fungsikendala.values())
  for a in range(len(listkendala)):
    for b in range(len(result)):
      if '<=' in listkendala[a]:
        if a==b:
          siapsimpleks.append(listkendala[a].replace("<=","{}=".format(result[b])))
      elif '>=' in listkendala[a]:
        if a==b:
          siapsimpleks.append(listkendala[a].replace(">=","{}=".format(result[b])))

  print(siapsimpleks)
  header = re.findall(r'[A-Z][0-9]+', fungsitujuan)
  header.append('KONS')
  header.append('RATIO')
  header.insert(0,'Z')
  header.insert(0,'VD')
  indeks = re.findall(r'[A-S][0-9]+', gabungkendala)
  indeks.insert(0,'Z')



  #CARI KOEFISIEN UNTUK TABEL SIMPLEKS
  def cari_koefisien(fx):
    y1_rep=fx.replace(" ","")
    y1_spl=re.split('\<=|\-|\+|\>=|\>|\<|\=', y1_rep)
    koef=[]
    for a in y1_spl:
      cek=a.isnumeric()
      if cek == True:
        b=a
      elif a.replace('.','',1).isnumeric():
        b=a
      else:
        a=a.replace('N','-')
        match = re.search('[A-Za-z]', a)
        if match:
          result = len(a) - match.end()
        b=a[0:-(result+1)]
      #cek integer atau float
      if b.isnumeric():
        koef.append(int(b))
      elif b.replace('.','',1).isnumeric():
        koef.append(float(b))
      else:
        if len(b)>0:
          koef.append(int(b))
        else:
          koef.append(0)
    return koef
  koefkendala=[]
  for x in siapsimpleks:
    koefkendala.append(cari_koefisien(x))
    
  koeftujuan=cari_koefisien(fungsitujuan)
  koeftujuan.append(0)
  #UBAH KOEF TUJUAN
  newkoeftujuan=[]
  for a in koeftujuan:
    newkoeftujuan.append(a*-1)
  koefkendala.insert(0,newkoeftujuan)

  column_ratio=[]
  for a in range(len(koefkendala)):
    column_ratio.append(0)
    
  z_awal=[]
  for a in range(len(koefkendala)):
    z_awal.append(1)
  z_awal[0]=1
    
  for i in range(len(koefkendala)):
    koefkendala[i].append(column_ratio[i])
    koefkendala[i].insert(0,z_awal[i])
    koefkendala[i].insert(0,z_awal[i])
    
  header = [col.lower() for col in header]
  indeks = [col.lower() for col in indeks] 
  header = header
  data = koefkendala
  print(data)
  print(header)
  print(indeks)
  return header,indeks, data






