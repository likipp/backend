from datetime import datetime

from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.response import Response

from .models import KPI, GroupKPI, KpiInput, User
from .serializers import KPISerializers, GroupKPISerializers, KpiInputSerializers
from account.serializers import DepartmentsSerializer
from account.models import Departments
from .filters import KPIFilter, GroupKPIFilter, KpiInputFilter
# from utils import select


def select(inputlist, list_a, dep_dict, kpi):
    for item in inputlist:
        if item.r_value:
            list_a[item.month.strftime('%Y-%m-%d')] = item.r_value
        else:
            list_a[item.month.strftime('%Y-%m-%d')] = 'NA'
        list_sort = sorted(list_a.items(), key=lambda x: x[0])
        dep_dict[kpi] = {"t_value": item.groupkpi.t_value,
                         "l_limit": item.groupkpi.l_limit,
                         "r_value": dict(list_sort)}


class KPIViewset(viewsets.ModelViewSet):
    """
        retrieve:
                返回指定KPI信息
        list:
                返回KPI列表
        update:
                更新KPI信息
        destroy:
                删除KPI记录
        create:
                创建KPI记录
        partial_update:
                更新记录部分字段
    """
    queryset = KPI.objects.all()
    serializer_class = KPISerializers
    filterset_class = KPIFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name']


class GroupKPIViewset(viewsets.ModelViewSet):
    """
        retrieve:
                返回指定部门KPI信息
        list:
                返回部门KPI列表
        update:
                更新部门KPI信息
        destroy:
                删除部门KPI记录
        create:
                创建部门KPI记录
        partial_update:
                更新记录部分字段
    """
    queryset = GroupKPI.objects.all()
    serializer_class = GroupKPISerializers
    filterset_class = GroupKPIFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['dep__name', 'kpi__name']

    # def create(self, request, *args, **kwargs):
    #     dep = request.data['dep']
    #     has_kpi = GroupKPI.objects.filter(request.data['dep']).all()
    #     if has_kpi:
    #         kpi = GroupKPI.objects.exclude(request.data['dep'])
    #     print(request.data)
    #     pass


class KpiInputViewset(viewsets.ModelViewSet):
    """
            retrieve:
                    返回指定KPI录入信息
            list:
                    返回KPI录入信息列表
            update:
                    更新KPI录入信息
            destroy:
                    删除KPI录入记录
            create:
                    创建KPI录入记录
            partial_update:
                    更新记录部分字段
        """
    queryset = KpiInput.objects.all()
    serializer_class = KpiInputSerializers
    filterset_class = KpiInputFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['groupkpi__dep__name', 'groupkpi__kpi__name']

    def list(self, request, *args, **kwargs):
        print(request.user, 222, self)
        user = User.objects.filter(username=request.user).first()
        kpis = KpiInput.objects.filter(user=user)
        return Response(kpis)


class KpiDashViewset(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = KpiInputSerializers
    serializer_dep = DepartmentsSerializer
    serializer_groupkpi = GroupKPISerializers
    serializer_kpi = KPISerializers

    def create(self, request, *args, **kwargs):
        ret = dict()
        dep_dict = dict()
        dep = request.data.get('name')
        kpi = request.data.get('kpi') or None
        kpi_id = self.serializer_kpi.Meta.model.objects.filter(name=kpi).first()
        dep_id = Departments.objects.filter(name=dep).first().id
        if kpi:
            groupkpi = kpi_id.group_kpi.first()
            inputlist = groupkpi.input_group.all()
            list_a = dict()
            # for item in inputlist:
            #     if item.r_value:
            #         list_a[item.month.strftime('%Y/%m')] = item.r_value
            #     else:
            #         list_a[item.month.strftime('%Y/%m')] = 'NA'
            #     list_sort = sorted(list_a.items(), key=lambda x: x[0])
            #     dep_dict[kpi] = {"t_value": item.groupkpi.t_value,
            #                      "l_limit": item.groupkpi.l_limit,
            #                      "r_value": dict(list_sort)}
            select(inputlist, list_a, dep_dict, kpi)
            ret[dep] = dep_dict
        else:
            groupkpi = GroupKPI.objects.filter(dep=dep_id)
            for i in groupkpi:
                inputlist = i.input_group.all()
                list_a = dict()
                kpi = i.kpi.name
                select(inputlist, list_a, dep_dict, kpi)
                ret[dep] = dep_dict
        return Response(ret)
