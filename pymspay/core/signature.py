# -*- coding: utf-8 -*-

from ctypes import *  # NOQA

from pymspay.core.exceptions import InvalidVerifyException
from pymspay.core.utils import Single, json_2_str


class SignatureCertification(metaclass=Single):

    def sign_and_encrypt(self, data):
        """
        签名及加密
        """
        if isinstance(data, dict):
            data = json_2_str(data)
        if isinstance(data, str):
            data = data.encode('utf-8')
        source_data = (c_ubyte * len(data))()  # NOQA
        for i, char in enumerate(data):
            source_data[i] = char
        source_data_size = c_int(len(data))  # NOQA
        base64_envelope_ptr = c_char_p(None)  # NOQA
        base64_envelope_ptr = cast(base64_envelope_ptr, POINTER(c_ubyte))  # NOQA

        result = self.cmbc.SignAndEncrypt(
            self.g_key_handle, source_data, source_data_size, byref(base64_envelope_ptr))  # NOQA
        if result != 0:
            return InvalidVerifyException(errmsg='Sign And Encrypt Failed')

        out_str = cast(base64_envelope_ptr, c_char_p).value  # NOQA
        self.cmbc.FreeMemory(base64_envelope_ptr)
        return str(out_str, encoding='utf-8')

    def decrypt_and_verify(self, data):
        """
        解密及验证
        """
        base64_envelope_encrypted_ptr = c_char_p(data.encode('utf-8'))  # NOQA
        plain_data = c_char_p(None)  # NOQA
        plain_data_ptr = cast(plain_data, POINTER(c_ubyte))  # NOQA
        plain_data_size = c_int(0)  # NOQA

        result = self.cmbc.DecryptAndVerify(
            self.g_key_handle, base64_envelope_encrypted_ptr, byref(plain_data_ptr), byref(plain_data_size))  # NOQA
        if result != 0:
            return InvalidVerifyException(errmsg='Decrypt And Verify Failed')

        out_str = cast(plain_data_ptr, c_char_p).value  # NOQA
        self.cmbc.FreeMemory(plain_data_ptr)
        return str(out_str, encoding='utf-8')
