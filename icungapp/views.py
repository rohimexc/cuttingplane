from django.shortcuts import render, redirect 
from .cuttingplane import cutting_plane
from .simpleks import simplex_tableau
from .koefisien import koefisien
import numpy as np
import pandas as pd
from .models import *
import ast
import secrets
import sympy
import math
from django.contrib import messages
def home(request):
    jumlah_penggunaan=DataProses.objects.all().count()
    context={'jumlah_penggunaan':jumlah_penggunaan}
    return render(request, 'icungapp/index.html',context)

def input_fungsi(request):
    variabel=[]
    prob_kendala=[]
    if request.method == 'POST':
        var =int(request.POST.get('var'))
        kendala =int(request.POST.get('kendala'))
        token=secrets.token_urlsafe(16),
        kendala_save=DataProses.objects.create(
            token=token,
            kendala=kendala,
            hasil=''   
        )
        kendala_save.save()
        for a in range (1,var+1):
            variabel.append('X{}'.format(a))
        for a in range(1,kendala+1):
            prob_kendala.append(a)
    context={'kendala':prob_kendala, 'variabel':variabel,'token':token}
    return render(request, 'icungapp/input_fungsi.html',context)

def proses(request, token):
    kendala=list(DataProses.objects.values_list("kendala",flat= True))[-1]
    fungsi_kendala={}
    header=[]
    indeks=[]
    data=[]
    tabel_simpleks=[]
    hasilTabel=DataProses.objects.get(token=token)
    if request.method == 'POST':
        hasil =request.POST.get('hasil')
        hasilTabel.hasil=hasil
        hasilTabel.save()
        for a in range(1,kendala+1):
            fungsi_kendala[f'y{a}']=request.POST.get(f'kendala{a}')
        print(fungsi_kendala)
        fungsitujuan=request.POST.get('tujuan')
        header,indeks,data=koefisien(fungsi_kendala,fungsitujuan)
        df = pd.DataFrame(data,columns=header) 
        df = df.set_index('vd') 
        df = df.reset_index()
        df['vd'] = indeks
        df = df.set_index('vd')
        df = df.replace("M",np.nan)
        
        while True:
            df = simplex_tableau(df)
            
            not_negative = (df.loc['z', :] >= 0).all()
            if not_negative:
                df = df.round(4)
                
                break
            else:
                df = simplex_tableau(df)
                df = df.round(4)

            tabel_simpleks = df.to_html(table_id='dataTable',classes='table table-bordered')
            tabelhasilsimpleks=df.copy()
            tabelcek=df.copy()
        

        # mengubah nilai yang berakhiran desimal .00 pada kolom 'kons' menjadi integer
        #tabelcek['kons'] = tabelcek['kons'].astype(str).str.rstrip('.00').astype(float).astype(int)
        # tabelcek['kons'] = tabelcek['kons'].astype(str).apply(lambda x: x.split('.')[0]).astype(np.int64)
        tabelcek['kons'] = tabelcek['kons'].apply(lambda x: float(str(x).replace('e+', '')))
        tabelcek['kons'] = tabelcek['kons'].astype(float).apply(lambda x: round(x, 2))
        # Cek nilai pada baris z
        nilai_baris_z = tabelhasilsimpleks.loc['z', :]
        if (nilai_baris_z.loc[nilai_baris_z.index.str.startswith('a')] >= 0).all() or (nilai_baris_z.loc[nilai_baris_z.index.str.startswith('s')] >= 0).all():
            messages.warning(request,"Semua nilai pada baris z yang dimulai dengan a atau s tidak negatif")
            basis_positive=1
        else:
            basis_positive=0
        nilai_var_simpleks = tabelcek.loc[tabelcek.index.str.startswith('x')]['kons']
        # mengecek apakah ada setidaknya satu nilai float pada nilai_x
        if nilai_var_simpleks.apply(lambda x: isinstance(x, float)).any():
            perlu_cp = 1
        else:
            perlu_cp = 0
        
        index_baru = tabelhasilsimpleks.index.tolist()
        
        perbedaan = list(set(index_baru) - set(indeks))
        #hapus kolom ratio
        tabel_cutting_plane = {}
        tabelhasilsimpleks = tabelhasilsimpleks.drop(columns=['ratio'])
        #tabelhasilsimpleks = tabelhasilsimpleks.drop(tabelhasilsimpleks.index[tabelhasilsimpleks.index.str.startswith('a')])
        #tabelhasilsimpleks = tabelhasilsimpleks.filter(regex='^(?!a).*')
        # Get the index labels x as a list
        index_list_x = [val for val in perbedaan if val.startswith('x')]
        iterasi = 1
        max_iterasi = 10
        tabelbaru, value_baru, index_baru,kolomkunci, iter = cutting_plane(tabelhasilsimpleks, index_list_x, iterasi)
        
        while True:
            try:
                if len(value_baru) > 0 and kolomkunci != 'z':
                    print(value_baru)
                    tabelbaru, value_baru, index_baru,kolomkunci, iter = cutting_plane(tabelbaru, index_baru, iter)
                    tabelbaru = tabelbaru.round(1)
                else:
                    break
                tabel_cutting_plane[f'Iterasi Ke - {iterasi}'] = tabelbaru.iloc[:, :-1].to_html(table_id='dataTable', classes='table table-bordered')
                
                iterasi += 1
                if iterasi > max_iterasi:
                    break
                
            except TypeError:
                messages.warning(request,"Tidak Diperlukan Metode Cutting Plane")
                break

        if perlu_cp==0:
            # mengubah series nilai_x menjadi dictionary
            variabel_hasil = nilai_var_simpleks.to_dict()
            print(variabel_hasil)
        else:
            print(tabelbaru)
            nilai_var_cp = tabelbaru.loc[tabelbaru.index.str.startswith('x')]['kons']
            print(nilai_var_cp)
            variabel_hasil = nilai_var_cp.to_dict()
        variabel_hasil = {k.upper(): v for k, v in variabel_hasil.items()}
        
        jumlah_grid=12
        if len(variabel_hasil)>4:
            jumlah_grid=3
        else:
            jumlah_grid=int(12/len(variabel_hasil))
        # substitusi nilai dari dictionary nilai_x pada persamaan
        # Membuat dictionary variabel
        my_var = {}
        # Loop untuk setiap key dalam list header
        for key in header:
            # Jika key dimulai dengan "x"
            if key.startswith('x'):
                # Tambahkan key ke dictionary dengan nilai 0
                my_var[key] = 0
        my_var = {k.upper(): v for k, v in my_var.items()}
        # Loop untuk setiap key dalam dictionary a

        for key in variabel_hasil:
            # Jika key ada dalam dictionary b
            if key in my_var:
                # Ganti nilai b dengan nilai a pada key yang sama
                my_var[key] = variabel_hasil[key]
        
        for key, val in my_var.items():
            fungsitujuan = fungsitujuan.replace(key.lower(),'*' + str(val))
            fungsitujuan = fungsitujuan.replace(key.upper(),'*' + str(val))
        fungsitujuan = fungsitujuan.replace(' ', '')  # hapus spasi
        print(fungsitujuan)
        #hitung hasil
        hasil_hitung = sympy.sympify(fungsitujuan)
        hasil_hitung=hasil_hitung.evalf()
        if math.isnan(hasil_hitung):
            hasil_hitung=hasil_hitung
        else:
            hasil_hitung=int(round(hasil_hitung,0))
    context = {
        'header':header,
        'indeks':indeks,
        'data':data,
        'tabel_simpleks':tabel_simpleks,
        'tabel_cutting_plane':tabel_cutting_plane,
        'variabel_hasil':variabel_hasil,
        'hasil':hasil,
        'hasil_hitung':hasil_hitung,
        'jumlah_grid' :jumlah_grid
    }
    return render(request, 'icungapp/proses.html',context)

