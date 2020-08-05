# -*- coding: utf-8 -*-

import inspect
import logging
import requests

from six.moves.urllib.parse import urljoin, urlencode

from pymspay.core.exceptions import PayException
from .api.base import MSYHPayBaseAPI

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, MSYHPayBaseAPI)


class Client(object):
    _http = requests.Session()

    def __new__(cls, *args, **kwargs):
        mcs = super(Client, cls).__new__(cls, *args, **kwargs)

        api_endpoints = inspect.getmembers(mcs, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(mcs)
            setattr(mcs, name, api)
        return mcs

    def __init__(self, *, cid, api_base_url, headers, timeout=None):
        """
        :param cid: 商家编号，必传项
        :param api_base_url: 请求域名地址，必传项
        :param headers: 请求头信息，必传项
        :param timeout: 超时时间，非必传
        """
        self.timeout = timeout
        self.cid = cid
        self.api_base_url = api_base_url
        self.headers = headers

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
            api_base_url = kwargs.pop('api_base_url', self.api_base_url)
            url = urljoin(api_base_url, uri_or_endpoint)
        else:
            url = uri_or_endpoint

        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers

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
            raise PayException(errmsg=exc)

        result = res.text

        logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                     url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result
