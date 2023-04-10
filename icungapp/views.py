from django.shortcuts import render, redirect 
from .cuttingplane import cutting_plane
from .simpleks import simplex_tableau
from .koefisien import koefisien
import numpy as np
import pandas as pd
from .models import *
import ast
import secrets
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
        
        for a in range(0,3):
            df=simplex_tableau(df)
            not_negative = (df.loc['z', :] >= 0).all()
            if not_negative == False:
                df=simplex_tableau(df)
                df=df.round(4)
                
            else:
                df=df.round(4)
                break
            tabel_simpleks = df.to_html(table_id='dataTable',classes='table table-bordered' )
            tabelhasilsimpleks=df.copy()
        index_baru = tabelhasilsimpleks.index.tolist()
        perbedaan = list(set(index_baru) - set(indeks))
        #hapus kolom ratio
        tabelhasilsimpleks = tabelhasilsimpleks.drop(columns=['ratio'])
        # Get the index labels x as a list
        index_list_x = [val for val in perbedaan if val.startswith('x')]
        #cari index dengan nilai kons tidak integer
        iterasi=1
        tabelbaru,index_list_baru,iter = cutting_plane(tabelhasilsimpleks, index_list_x, iterasi)
        tabel_cutting_plane={}
        for iterasi in range(0,2):
            if len(index_baru)>0:
                tabelbaru,index_baru,iter=cutting_plane(tabelbaru,index_baru,iter)
                index_baru = [val for val in index_baru if val.startswith('x')]
                tabelbaru=tabelbaru.round(2)
            else:
                tabelbaru=tabelbaru.round(2)
                break
            tabel_cutting_plane[f'Iterasi Ke - {iterasi+1}']=tabelbaru.to_html(table_id='dataTable',classes='table table-bordered' )
        
    context = {
        'header':header,
        'indeks':indeks,
        'data':data,
        'tabel_simpleks':tabel_simpleks,
        'tabel_cutting_plane':tabel_cutting_plane,
        'hasil':hasil,
    }
    return render(request, 'icungapp/proses.html',context)

