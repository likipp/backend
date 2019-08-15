from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("departments", DepartmentsViewset, base_name="departments")
router.register("users", UserViewset, base_name="users")

urlpatterns = [
    url('^', include(router.urls)),
]
