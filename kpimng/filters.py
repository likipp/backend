from django_filters import rest_framework as filters

from account.models import Departments
from .models import KPI, GroupKPI, KpiInput


class GroupKPIFilter(filters.FilterSet):
    dep = filters.ModelChoiceFilter(queryset=Departments.objects.all())
    kpi = filters.ModelChoiceFilter(queryset=KPI.objects.all())

    class Meta:
        model = GroupKPI
        fields = ["dep", "kpi"]


class KPIFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")

    class Meta:
        model = KPI
        fields = ["name"]


class KpiInputFilter(filters.FilterSet):
    groupkpi = filters.ModelChoiceFilter(queryset=GroupKPI.objects.all())
    kpi = filters.ModelChoiceFilter(queryset=KPI.objects.all())

    class Meta:
        model = KpiInput
        fields = ["groupkpi", "kpi"]