# -*- coding: utf-8 -*-

import json
import platform
from ctypes import *  # NOQA

import regex

from pymspay import settings as ps

pattern = regex.compile(r'(div|meta|link|script)')


def json_2_str(data):
    """
    字典数据转化为字符串
    """
    return json.dumps(data, ensure_ascii=False)


def is_html(data):
    data = data.strip()
    # 一级验证
    if (data.startswith('<!DOCTYPE html>') or data.startswith('<html>')) and data.endswith('</html>'):
        # 二级验证：特殊的元素标签
        if pattern.search(data):
            return True
    return False


def get_sys_cfg():
    """
    获取当前电脑系统
    """
    sys_str = platform.system()
    if sys_str == "Linux":
        return cdll.LoadLibrary(ps.MSYH_PACKAGE)  # NOQA
    elif sys_str == 'Windows':
        return windll.LoadLibrary(ps.MSYH_PACKAGE)  # NOQA
    else:
        raise Exception('Unknown System...')


class Single(type):
    _instance = None

    def __new__(cls, name, bases, attrs):
        if not cls._instance:

            g_key_handle = c_void_p(0)  # NOQA
            cmbc = get_sys_cfg()
            cmbc.Initialize(
                c_char_p(ps.MSYH_PRIVATE_FILE.encode('utf-8')),  # NOQA
                c_char_p(ps.MSYH_PRIVATE_FILE_PASSWORD.encode('utf-8')),  # NOQA
                c_char_p(ps.MSYH_CERT_FILE.encode('utf-8')),  # NOQA
                byref(g_key_handle)  # NOQA
            )
            attrs['cmbc'] = cmbc
            attrs['g_key_handle'] = g_key_handle
            cls._instance = super(Single, cls).__new__(cls, name, bases, attrs)

        return cls._instance
