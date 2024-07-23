from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from courses import views as paiement

urlpatterns = [
    url(r'^evaluer/', include('evaluer.urls')),
    url(r'^choix/', include('choix.urls')),
    url(r'^$', user_views.home, name='home'),
    url(r'^about/$', user_views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^courses/', include('courses.urls')),
    url(r'^profile/', include('users.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^paiement/(?P<montant>[\d ]+)/$', paiement.initiate_payment, name='Paiement'),
    url(r'^abonnement$',paiement.abonnement , name='abonnement'),
    url(r'^succes$', paiement.succes,name='paiement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
