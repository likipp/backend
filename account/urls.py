from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("departments", DepartmentsViewset, base_name="departments")
router.register("users", UserViewset, base_name="users")
router.register("groups", GroupViewSet, base_name="groups")

urlpatterns = [
    url('^', include(router.urls)),
]
