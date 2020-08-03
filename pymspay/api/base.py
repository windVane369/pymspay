# -*- coding: utf-8 -*-
from pymspay.core.signature import SignatureCertification
from pymspay.core.utils import is_html


class MSYHPayBaseAPI(object):

    def __init__(self, client=None):
        self._client = client
        self.sign_func = SignatureCertification()

    def _get(self, url, params=None, **kwargs):
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data, decrypt_and_verify_or_not=True, params=None, **kwargs):
        data = self._sign_and_encrypt(data)
        response_data = self._client.post(url, data, params, **kwargs)
        if decrypt_and_verify_or_not:
            return self._decrypt_and_verify(response_data)
        return response_data

    def _sign_and_encrypt(self, data):
        crypt_data = self.sign_func.sign_and_encrypt(data)
        return {
            '_cryptDatas': crypt_data,
            '_merNum': data.get('cid')
        }

    def _decrypt_and_verify(self, data):
        # 检查数据需要解密
        if is_html(data):
            return data
        return self.sign_func.decrypt_and_verify(data)

    @property
    def cid(self):
        return self._client.cid
