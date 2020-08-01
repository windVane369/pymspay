# -*- coding: utf-8 -*-

import inspect
import logging
import requests

from six.moves.urllib.parse import urljoin, urlencode
from .api.base import MSYHPayBaseAPI
from pymspay import settings as ps

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, MSYHPayBaseAPI)


class BaseClient(object):
    _http = requests.Session()

    API_BASE_URL = ps.MSYH_BASE_URL

    def __new__(cls, *args, **kwargs):
        mcs = super(BaseClient, cls).__new__(cls, *args, **kwargs)

        api_endpoints = inspect.getmembers(mcs, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(mcs)
            setattr(mcs, name, api)
        return mcs

    def __init__(self, timeout=None):
        self.timeout = timeout

    def get(self, uri, params=None, **kwargs):
        """
        get 接口请求

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        """
        if params is not None:
            kwargs['params'] = params
        return self.request('GET', uri, **kwargs)

    def post(self, uri, data=None, params=None, **kwargs):
        """
        post 接口请求

        :param uri: 请求url
        :param data: post 数据
        :param params: post接口中url问号后参数（dict 格式）
        """
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)

    def request(self, method, uri, **kwargs):
        try:
            return self._request(method, uri, **kwargs)
        except Exception as exc:
            raise Exception(exc)

    def _request(self, method, uri_or_endpoint, **kwargs):
        if not uri_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, uri_or_endpoint)
        else:
            url = uri_or_endpoint

        if 'headers' not in kwargs:
            kwargs['headers'] = ps.MSYH_HEADERS

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs.get('data', ''), dict):
            kwargs['data'] = urlencode(kwargs['data'])
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as exc:
            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【异常信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), exc)
            raise Exception(exc)

        result = res.text

        logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                     url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result
