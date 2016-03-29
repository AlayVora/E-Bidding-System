from django.conf.urls import include, url
from django.contrib import admin
from blog import views
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^home/$', views.home, name='home'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'', include('mama_cas.urls')),
    url(r'^cas/', include('mama_cas.urls')),
    url(r'^category/$', views.category, name='category'),
    url(r'^process_register/$', views.process_register, name='process_register'),
    url(r'^buy_bids/$', views.buy_bids, name='buy_bids'),
    url(r'^addproduct/$', views.addproduct, name='addproduct'),
    url(r'^orderhistory/$', views.orderhistory, name='orderhistory'),
    url(r'^searchproducts/$', views.searchproducts, name='searchproducts'),
    url(r'^viewproduct/(?P<category_id>\d+)/$', views.viewproduct, name='viewproduct'),    
    url(r'^products_in_category/(?P<category_id>\d+)/$', views.products_in_category, name='products_in_category'),
    url(r'^processbids/$', views.processbids, name='processbids'),
    url(r'^getmaxbidder/$', views.getmaxbidder.as_view(), name='getmaxbidder'),
    url(r'^loginform/$', views.loginform, name='loginform'),
    url(r'^mybidproducts/$', views.mybidproducts, name='mybidproducts'),
    url(r'^changePassword/$', views.changePassword, name='changePassword'),
    url(r'^account_management/$', views.account_management, name='account_management'),
    url(r'^logoutview/$', views.logoutview, name='logoutview'),
    url(r'^CurrrentDateTime/$', views.CurrrentDateTime.as_view(), name='CurrrentDateTime'),
    url(r'^buybidservice/$', views.buybidservice.as_view(), name='buybidservice'),
    url(r'^search/$', views.search.as_view(), name='search'),
    url(r'^sold/$', views.sold, name='sold'),
    url(r'^autobid/$', views.autobid.as_view(), name='autobid'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),

]
