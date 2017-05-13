from django.conf.urls import url, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from pairing import views
from django.views.generic.base import TemplateView

router = DefaultRouter()
router.register('players', views.PlayerViewSet)
router.register('results', views.ResultViewSet)
router.register('rounds', views.RoundViewSet)
router.register('standings', views.StandingViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
