# coding=utf-8
from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('__file__')


class ResponseErrors(object):

    @staticmethod
    def get_base_error():
        return Response(
            {'message': 'Ошибка обработки значения ',
             'status': 'danger', }, status=status.HTTP_404_NOT_FOUND)
