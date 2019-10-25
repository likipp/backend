from django.conf.urls import include, url
from django.views.static import serve

from rest_framework.routers import DefaultRouter

from .views import *
from kpiweb import settings

router = DefaultRouter()
router.register("departments", DepartmentsViewset, base_name="departments")
router.register("users", UserViewset, base_name="users")
router.register("groups", GroupViewSet, base_name="groups")
router.register("change-password", PersonalCenterViewSet, base_name="change_password")

urlpatterns = [
    url('^', include(router.urls)),
    # url('^auth/$', AuthView.as_view())
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
