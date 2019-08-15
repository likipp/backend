from django.core.paginator import InvalidPage
from django.utils import six

from collections import OrderedDict, namedtuple
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'page'
