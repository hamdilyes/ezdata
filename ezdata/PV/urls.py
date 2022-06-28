from django.urls import path, include
from . import views
from . import admin_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('accounts', include('django.contrib.auth.urls')),

    path('clients', views.test, name='clients'),
    path('<int:id_enseigne>/clients', views.test_exists, name='clients_exists'),

    path('<int:id_enseigne>/batiments', views.batiments, name='batiments'),
    path('<int:id_enseigne>/personnalise',
         views.personnalise, name='personnalise'),
    path('<int:id_enseigne>/profilperso',
         views.profilperso, name='profilperso'),
    path('<int:id_enseigne>/energie', views.energie, name='energie'),
    path('<int:id_enseigne>/mobilite', views.mobilite, name='mobilite'),

    path('<int:id_enseigne>/results', views.results_catalogue, name='results'),
    path('<int:id_enseigne>/factu', views.factu_catalogue, name='factu'),
    path('<int:id_enseigne>/mde', views.mde, name='mde'),
    path('<int:id_enseigne>/mobi', views.mobi, name='mobi'),
    path('<int:id_enseigne>/bilan', views.bilan_catalogue, name='bilan'),
    path('<int:id_enseigne>/multi-sites',
         views.multi_sites_catalogue, name='multi-sites'),

    path('<int:id_enseigne>/pdf/<str:templatepath>/<int:nsite>',
         views.render_pdf_view, name='pdftest'),

    path('<int:id>/dimens-centrale',
         admin_views.dimens_centrale_admin, name='dimens-centrale'),
    path('<int:id>/<str:centrale>/<str:batterie>/devis',
         admin_views.devis, name='devis'),

    path('<int:id_projet>/xls', views.export_xls, name='xls'),

]
urlpatterns += staticfiles_urlpatterns()
