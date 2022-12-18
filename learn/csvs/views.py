
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CsvModelForm
from hashlib import scrypt
from base64 import urlsafe_b64encode
import pandas as pd
from django.contrib import messages
from sqlalchemy import create_engine
import re
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from user_manage.models import user_database
from cryptography.fernet import Fernet
from django.core.files.storage import FileSystemStorage
from sqlalchemy.exc import SQLAlchemyError
from .models import db_target_conf
#=================================[Func dbconfserver for  views]===============================================
def fernetkey():
    """
    fungsi untuk membuat kunci yang akan digunakan di enkrsipsi 
    - digunakan di:
    func csvs.view.decryptfunc
    func csvs.view.encryptfunc
    """
    salt = b'TeM4n_d47a_ke!@3^7' #don't change this
    key = scrypt(b'password', salt=salt, n=16384, r=8, p=1, dklen=32)
    key_encoded = urlsafe_b64encode(key)
    fernet = Fernet(key_encoded)
    return fernet
def encryptfunc(textinp):
    """
    fungsi untuk eksripsi data
    - digunakan di:
    func user_manager.view.signup 
    """
    text = textinp
    fernet = fernetkey()
    encryptfunc = fernet.encrypt(text.encode())
    return encryptfunc
def decryptfunc(request):
    """
    fungsi untuk deeksripsi data unutk menekripsi password
    - digunakan di:
    func user_manager.view.blog
    func user_manager.view.
    """
    fernet = fernetkey()
    username= request.user.get_username()
    pass_enc = user_database.objects.filter(username = f'{username}').values_list('password')[0]
    str_pass = (multiple_replace(str(pass_enc),{"('":'',"',)":''}))  
    str_pass_2 = (multiple_replace(str(str_pass),{"b'":'',"'":''}))
    to_byte= bytes(str_pass_2,'utf-8')
    string = fernet.decrypt(to_byte).decode()
    return str(string)
def dbconflocal(dbname,dbuser,dbpass,dbhost,dbport):
    NAME = dbname
    USER = dbuser
    PASSWORD = dbpass
    HOST = dbhost
    PORT = dbport
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}')
    return engine
    
def dbconfserver():
    NAME = 'postgres'
    USER = 'krise'
    PASSWORD = '1232'
    HOST = 'localhost'
    PORT = '5432'
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',isolation_level="AUTOCOMMIT")
    return engine

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

def tras_data(table,connection):
    query = '''select * from {} '''.format(table)
    df = pd.read_sql_query(query,con=connection)
    alldata = []
    for i in range(df.shape[0]):
        temp=df.loc[i]
        alldata.append(dict(temp))
    return alldata,df,query
def dblog(request):
    username= request.user.get_username()
    str_pass = decryptfunc(request)
    fg1 = list(user_database.objects.filter(username = f'{username}').values_list('group'))[0]
    str_db = (multiple_replace(str(fg1),{"('":'',"',)":''}))  
    return str_db,username,str_pass
def save_db(request):
    dbname,dbuser,dbpass = dblog(request)
    dbhost = 'localhost'
    dbport = '5432'
    conn = dbconflocal(dbname,dbuser,dbpass,dbhost,dbport)
    return conn



#==============================================================================================================
"""
type    : function
name    : upload_file_view
html    : upload.html
path    : '/' 
"""
def upload_file_view(request):
    if request.user.is_authenticated:
        """
        Func for upload file
        """
        folder='media' 
        data_type = ['character varying','bigint','date','double precision','timestamp without time zone']
        all_data1 = []
        error = ''
        if request.method == 'POST':
            if request.FILES.get('csv_file'):
                myfile = request.FILES.get('csv_file')
                fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
                file_name = fs.save(myfile.name, myfile)
                request.session['namefile'] = file_name
                df = pd.read_csv('media/'+request.session['namefile'])
                #====================================
                # df = pd.read_csv(myfile)
                # request.session['csv_file'] = df.to_dict()
                # df = pd.DataFrame.from_dict(request.session['csv_file'])
                #===================================
                columns = df.columns
                type = df.dtypes
                # print(type)
                for i in df.columns:
                    if type[i] == 'object':
                        type[i] ='character variying'
                    elif type[i] == 'float64':
                        type[i] ='double precision'
                    elif type[i] == 'int64':
                        type[i] ='bigint'
                print(type)
                isnan = []
                for i in list(df.columns.values):
                    df[i] = df[i].astype(str)
                    isnan.append(df[i].isna().sum())    
                for i in range(df.shape[0]):
                        temp=df.loc[i]
                        all_data1.append(dict(temp))
            else:
                error = ''
                df = pd.read_csv('media/'+request.session['namefile'])
                print(request.session['namefile'])
                if request.POST.get('delete'):
                    df = df.drop(request.POST.get('delete'), axis=1)
                    df.to_csv('media/'+request.session['namefile'],index = False)
                df = pd.read_csv('media/'+request.session['namefile'])
                columns = df.columns
                type = df.dtypes
                for i in df.columns:
                    if type[i] == 'object':
                        type[i] ='character variying'
                    elif type[i] == 'float64':
                        type[i] ='double precision'
                    elif type[i] == 'int64':
                        type[i] ='bigint'
                print(type)
                isnan = []
                for i in list(df.columns.values):
                    df[i] = df[i].astype(str)
                    isnan.append(df[i].isna().sum())    
                for i in range(df.shape[0]):
                        temp=df.loc[i]
                        all_data1.append(dict(temp))
                if request.POST.get("Send") == 'Yes':
                    
                    #create table data
                    try:
                        create_table = "CREATE TABLE " +request.session['namefile'][:-4]+" ( "
                        for idx,i in enumerate(request.POST):
                            if idx >0 and i != 'Send':
                                create_table+= i.replace(" ", "_").replace(":","")
                                if request.POST.get(i) == 'bigint':
                                    create_table+=" bigint, "
                                elif request.POST.get(i) == 'double precision':
                                    create_table+=" float, "
                                elif request.POST.get(i) == 'character varying':
                                    create_table+=" varchar(255), "
                                elif request.POST.get(i) == 'date':
                                    create_table+=" DATE, "
                                elif request.POST.get(i) == 'timestamp without time zone':
                                    create_table+=" timestamp, "
                        create_table = create_table[:-2] +" );"
                        # print(create_table)
                        dbconfserver().execute(create_table)
                        select = dbconfserver().execute('''SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{}\''''.format(request.session['namefile'][:-4]).lower())
                        data = pd.read_sql_query('''select * from {}'''.format(request.session['namefile'][:-4]),con=dbconfserver())
                        # print(data)
                        columns = data.columns
                        type = data.dtypes
                        currentColumn = select.all()
                        for column in currentColumn:
                            type[column[0]] = column[1]
                        print(type)                    
                    except:
                        print('tabel sudah ada')
                    for i in list(df.columns.values):
                        try:
                            if request.POST.get(i) == 'character varying':
                                df[i]= df[i].astype('object')
                                print('berhasil',request.POST.get(i),i)
                            
                            elif request.POST.get(i) == 'bigint':
                                df[i]= df[i].astype('int64')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'date':
                                df[i] = pd.to_datetime(df[i], errors='coerce')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'double precision':
                                df[i]= df[i].astype('float64')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'timestamp without time zone':
                                df[i]= df[i].astype('int64')
                                print('berhasil',request.POST.get(i),i)
                        except:
                            print('gagal',request.POST.get(i),i)
                            
                    try:
                        data = pd.read_sql_query('''select * from {}'''.format(request.session['namefile'][:-4]).lower(),con=dbconfserver())
                        columnsSend=' ('
                        for i in data.columns:
                            columnsSend+=i+","
                        columnsSend=columnsSend[:-1]+") "
                        # print(columnsSend)
                        
                        df = pd.read_csv('media/'+request.session['namefile'])
                        values = []
                        for idx, i in enumerate(df.values.tolist()):
                            value ='('
                            for j in i:
                                value += "'"+str(j).replace("'","''")+"',"
                            value = value[:-1]+"),"
                            values.append(value)
                        
                        value =''
                        for i in values:
                            value+= i
                        value = value[:-1]
                        # print('nilai data ',value)
                        
                        dbconfserver().execute("INSERT INTO "+request.session['namefile'][:-4].lower()+columnsSend +" VALUES "+value)
                        
                    except SQLAlchemyError as e: 
                        error = str(e.__dict__['orig'])
                        arr = error.split('\n')
                        arr = arr[:-2]
                        # print('hasil error',arr)
                        error = arr
                        
                elif request.POST.get("Send") == 'Data':
                    for i in list(df.columns.values):
                        try:
                            if request.POST.get(i) == 'character varying':
                                df[i]= df[i].astype('object')
                                print('berhasil',request.POST.get(i),i)
                            
                            elif request.POST.get(i) == 'bigint':
                                df[i]= df[i].astype('int64')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'date':
                                df[i] = pd.to_datetime(df[i], errors='coerce')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'double precision':
                                df[i]= df[i].astype('float64')
                                print('berhasil',request.POST.get(i),i)
                                
                            elif request.POST.get(i) == 'timestamp without time zone':
                                df[i]= df[i].astype('int64')
                                print('berhasil',request.POST.get(i),i)
                                
                        except:
                            print('gagal',request.POST.get(i),i)
                            
                    try:
                        data = pd.read_sql_query('''select * from {}'''.format(request.session['namefile'][:-4]).lower(),con=dbconfserver())
                        columnsSend=' ('
                        for i in data.columns:
                            columnsSend+=i+","
                        columnsSend=columnsSend[:-1]+") "
                        # print(columnsSend)
                        
                        df = pd.read_csv('media/'+request.session['namefile'])
                        values = []
                        for idx, i in enumerate(df.values.tolist()):
                            value ='('
                            for j in i:
                                value += "'"+str(j).replace("'","''")+"',"
                            value = value[:-1]+"),"
                            values.append(value)
                        
                        value =''
                        for i in values:
                            value+= i
                        value = value[:-1]
                        # print('nilai data ',value)
                        
                        dbconfserver().execute("INSERT INTO "+request.session['namefile'][:-4].lower()+columnsSend +" VALUES "+value)
                        
                    except SQLAlchemyError as e: 
                        error = str(e.__dict__['orig'])
                        arr = error.split('\n')
                        arr = arr[:-2]
                        # print('hasil error',arr)
                        error = arr
                
            # print(request.POST)
            request.POST.get("delete")
            return render(request,'upload.html', {'Data2':all_data1, 'Cols2':zip(columns,type,isnan),'DelCols2':columns, 'datatypes':data_type, 'error':error})
            
        else:
            return render(request,'upload.html')


    else:
        messages.error(request,"silahkan login terlebih dahulu")
        return redirect("login:signin")

#=================================================================================================
"""
type    : function
name    : list_data
html    : list_data.html
path    : 'transfer/' 
"""
def list_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("form_type") == 'Connect Database': 
                dbname = str(request.POST.get('dbname',False))
                dbuser = str(request.POST.get('user',False))
                dbpass = str(request.POST.get('password',False))
                dbhost = str(request.POST.get('host',False))
                dbport = str(request.POST.get('port',False))
                request.session['dbname'] = dbname
                request.session['user'] = dbuser
                request.session['password'] = dbpass
                request.session['host'] = dbhost
                request.session['port'] = dbport
                print('ini_coonect')
                sol = [] 
                try:
                    for i in dbconflocal(dbname,dbuser,dbpass,dbhost,dbport).execute(f"""select schemaname,tablename from pg_catalog.pg_tables where tableowner = '{dbuser}' ;"""):
                        result = (multiple_replace(str(i),{'(':'',')':'',"'":'',',':'',' ':'.'}))
                        sol.append(result)
                except:
                    messages.error(request,'masukan konfigurasi database dengan benar')
                    return redirect('csv_data:transfer')
                return redirect('csv_data:transfer')
            elif request.POST.get('todb') ==  'Import data':
                dbname = request.session['dbname']
                dbuser = request.session['user']
                dbpass = request.session['password']
                dbhost = request.session['host']
                dbport = request.session['port']
                conn_external = dbconflocal(dbname,dbuser,dbpass,dbhost,dbport)
                conn = save_db(request)
                name_table = request.session['input_file']
                table = str(name_table).split(".")[1]
                alldata,df,query_str=tras_data(name_table,conn_external)
                df = pd.DataFrame(df)
                db_target_conf.objects.update_or_create(dbfrom= dbname,table_name=table,query=query_str)
                schema_exists  = conn.execute(f"select 1 from pg_catalog.pg_tables where schemaname='{dbname}';").rowcount > 0
                if schema_exists == True:
                    df.to_sql(table,conn,index = False,schema=dbname)
                else:
                    conn.execute(F'CREATE SCHEMA {dbname};')
                    df.to_sql(table,conn,index = False,schema=dbname)
                messages.success(request,'files sudah masuk db')
                konten = {'Data2':alldata, 'Cols2':df}
                return render(request,'list_data.html',konten)
            else:#this preview
                dbname = request.session['dbname']
                dbuser = request.session['user']
                dbpass = request.session['password']
                dbhost = request.session['host']
                dbport = request.session['port']
                sol = []
                for i in dbconflocal(dbname,dbuser,dbpass,dbhost,dbport).execute(f"""select schemaname,tablename from pg_catalog.pg_tables where tableowner = '{dbuser}' ;"""):
                    result = (multiple_replace(str(i),{'(':'',')':'',"'":'',',':'','_view':'',' ':'.'}))
                    sol.append(result)
                name_table = str(request.POST.get('Dataini',False))
                request.session['input_file'] = name_table
                conn = dbconflocal(dbname,dbuser,dbpass,dbhost,dbport)
                try:
                    alldata,df,query_str = tras_data(name_table,conn)
                except:
                    messages.error(request,'pilih table terlebih dahulu')
                    return redirect('csv_data:transfer')
                context2 = {'Data':alldata, 'Cols':df,'select':sol,'message':f'{name_table}','dbname':f'{dbname}'}
                return render(request,'list_data.html',context2)
        else: 
            try:
                dbname = request.session['dbname']
                dbuser = request.session['user']
                dbpass = request.session['password']
                dbhost = request.session['host']
                dbport = request.session['port']

                print('ini get')
                sol = []
                for i in dbconflocal(dbname,dbuser,dbpass,dbhost,dbport).execute(f"""select schemaname,tablename from pg_catalog.pg_tables where tableowner = '{dbuser}' ;"""):
                    result = (multiple_replace(str(i),{'(':'',')':'',"'":'',',':'',' ':'.'}))
                    sol.append(result)
                user =request.user.is_superuser
                context2 = {'select':sol,'dbname':f'{dbname}','user':user}
                return render(request,'list_data.html',context2)
            except:

                # print(df.dtypes)
                user =request.user.is_superuser
                return render(request,'list_data.html',{'user':user})
                
    else:
        messages.error(request,"silahkan login terlebih dahulu")
        return redirect("login:signin")

#=================================================================================================================
"""
type    : function
name    : data_query
html    : data_query.html
path    : 'data_query/' 
"""
def data_query(request):
    if request.user.is_authenticated:
        db,user,passw = dblog(request)
        dbname = db
        sol = []
        dictschema = {}
        for i in save_db(request).execute(f"""select schemaname,tablename from pg_catalog.pg_tables where tableowner != 'postgres' ;"""):
            result = (multiple_replace(str(i),{'(':'',')':'',"'":'',',':'','_view':'',' ':'.'}))
            sol.append(result)
        for word in sol:
            wordPair = word.split('.')
            if wordPair[0] in dictschema:
                dictschema[wordPair[0]].append(wordPair[1])
            else:
                dictschema[wordPair[0]] = [wordPair[1]]
        if request.method == "POST":
            if request.POST.get("form_type") == 'preview':
                query_dict = {'query':[]}
                request.session['query_session'] = query_dict
                query_read = request.POST.get('query',False)        
                query_dict['query'].append(query_read)
                for k,j in request.session['query_session'].items():
                    qty = j
                load_query = qty[0]
                name_table = request.session['name_table']
                conn = save_db(request)
                df = pd.read_sql('''{}'''.format(query_read),con=conn)
                df.reset_index(drop=True,inplace=True)
                classes = 'table table-striped table-bordered table-hover table-sm'
                html_table = df.to_html(classes=classes,index=False)
                context2 = {'dfhtml':html_table,'load_query':load_query,'dict':dictschema,'message':f'{name_table}','dbname':f'{dbname}','query':f'{query}'}
                return render(request,'data_query.html',context2)

            elif request.POST.get("form_type") == 'submit view':
                query = request.POST.get('query',False)
                for k,j in request.session['query_session'].items():
                    qty = j
                load_query = qty[0]
                name_table = request.session['name_table']
                views = str(name_table).split('.')[0]
                name_views = str(name_table).split('.')[1]
                conn = save_db(request).connect()
                conn.execute(f""" set search_path to public;""")
                conn.execute(f""" CREATE OR REPLACE VIEW {views}_{name_views} as\n {query}""")
                df = pd.read_sql('''{}'''.format(query),con=conn)
                df.reset_index(drop=True,inplace=True)
                classes = 'table table-striped table-bordered table-hover table-sm'
                html_table = df.to_html(classes=classes,index=False)
                messages.success(request,"berhasil membuat view")
                context2 = {'dfhtml':html_table, 'load_query':load_query,'dict':dictschema,'message':f'{name_table}','dbname':f'{dbname}'}
                return render(request,'data_query.html',context2)
            else:
                try:
                    query = request.POST.get('query',False)
                    for j in request.session['query_session'].values():
                        qty = j
                    load_query = qty[0]
                    name_table = (request.POST.get('Dataini',False))
                    request.session['name_table'] = name_table
                    conn = save_db(request)
                    alldata,df,query_str = tras_data(name_table,conn)
                    df.reset_index(drop=True,inplace=True)
                    classes = 'table table-striped table-bordered table-hover table-sm'
                    html_table = df.to_html(classes=classes,index=False)
                    context2 = {'dfhtml':html_table,'load_query':load_query,'dict':dictschema,'message':f'{name_table}','dbname':f'{dbname}'}
                    return render(request,'data_query.html',context2)
                except:
                    name_table = (request.POST.get('Dataini',False))
                    request.session['name_table'] = name_table
                    conn = save_db(request)
                    alldata,df,query_str = tras_data(name_table,conn)
                    df.reset_index(drop=True,inplace=True)
                    classes = 'table table-striped table-bordered table-hover table-sm'
                    html_table = df.to_html(classes=classes,index=False)
                    context2 = { 'dfhtml':html_table,'dict':dictschema,'message':f'{name_table}','dbname':f'{dbname}'}
                    return render(request,'data_query.html',context2)
        else : 
            try:
                query = request.POST.get('query',False)
                for k,j in request.session['query_session'].items():
                    qty = j
                load_query = qty[0]
                context2 = {'dbname':f'{dbname}','load_query':load_query,'dict':dictschema}
            except:
                context2 = {'dbname':f'{dbname}','dict':dictschema}
            try:
                context2 = {'dbname':f'{dbname}','load_query':load_query,'dict':dictschema}
            except:
                context2 = {'dbname':f'{dbname}','dict':dictschema}
            return render(request,'data_query.html',context2)
    else:
        messages.error(request,"silahkan login terlebih dahulu")
        return redirect("login:signin")



