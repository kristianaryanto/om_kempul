from django.urls import path
from .views import *

app_name = 'csv_data'

urlpatterns = [
        path('',upload_file_view, name='upload-view'),
        # path('export_db/',to_db,name='export_db'),
        # path('change/',change_data,name='change'),
        # path('delete/',delete_data,name='delete'),
        path('transfer/',list_data,name='transfer'),
        path('data_query/',data_query,name='data_query'),
        # path('empty/iframe_query/',iframe_quert,name='iframe_quert'),
        # path('empty/',empty,name='empty'),

]