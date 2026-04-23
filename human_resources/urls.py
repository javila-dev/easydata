from django.urls import path
from human_resources import views


urlpatterns = [
    path('landing/', views.landing),
    path("workers/",views.human_resources),
    path('initial-import/', views.initial_personal_import),
    path('initial-import/start', views.initial_personal_import_start),
    path('initial-import/status/<int:job_id>', views.initial_personal_import_status),
    path('initial-import/stop/<int:job_id>', views.initial_personal_import_stop),
    path('initial-import/download/<int:job_id>', views.initial_personal_import_download),
    path('reports/',views.charts_reports),
    path('budget/', views.personalbudget),
    path('parameters/', views.parameters),
    path('transitions/', views.transitions),
    path('historial/', views.historico),
    path('notifications/',views.errors_and_warnings),
    path('dashboard/',views.dashboard),
    path('utils/dependentlist',views.dependentlist),
    path('masivecreatepartner', views.masivepartnercreation),
]
