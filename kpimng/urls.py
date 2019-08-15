from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("kpi", KPIViewset, base_name="kpi")
router.register("groupkpi", GroupKPIViewset, base_name="groupkpi")
router.register("kpiinput", KpiInputViewset, base_name="kpiinput")
router.register("kpidash", KpiDashViewset, base_name="kpidash")

urlpatterns = [
    url('^', include(router.urls)),
]
