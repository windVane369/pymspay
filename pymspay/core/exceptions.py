# -*- coding: utf-8 -*-
from pymspay.core.utils import to_text


class PyMsPay(Exception):

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return to_text(f'Error code: {self.errcode}, message: {self.errmsg}')

    def __repr__(self):
        return to_text(f'{self.__class__.__name__}({self.errcode}, {self.errmsg})')


class InvalidVerifyException(PyMsPay):

    def __init__(self, errcode=10000, errmsg='Invalid Verify Exception'):
        super().__init__(errcode, errmsg)


class PayException(PyMsPay):

    def __init__(self, errcode=20000, errmsg='Pay Exception'):
        super().__init__(errcode, errmsg)


class OthersException(PyMsPay):

    def __init__(self, errcode=30000, errmsg='Others Exception'):
        super().__init__(errcode, errmsg)
