from django.urls import path
from reports import views


urlpatterns = [
    path("landing/",views.landing),
    path('expenses/',views.expenses),
    path('expenses/analyze/<date_from>/<date_to>',views.analyze_expenses),
    path('expenses/detail',views.expenses_detail),
    path('expenses/classify', views.classifications),
    path('expenses/ajax/deleteclassify', views.delete_classify),
    path('dashboard',views.dashboarddata)
]