# -*- coding: utf-8 -*-

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 银行相关文件存储基础地址
MSYH_FILE_BASE_DIR = os.path.join(os.path.join(os.path.join(BASE_DIR, 'pymspay'), 'core'), 'files')
if not os.path.exists(MSYH_FILE_BASE_DIR):
    os.makedirs(MSYH_FILE_BASE_DIR)

# 商家编号加密私钥
MSYH_PRIVATE_FILE = os.path.join(MSYH_FILE_BASE_DIR, '文件名')
# 商家密码
MSYH_PRIVATE_FILE_PASSWORD = '密码'
# 银行公钥
MSYH_CERT_FILE = os.path.join(MSYH_FILE_BASE_DIR, '银行数据解密公钥')
# 加密解密的第三方包
# # Linux so文件
# # Windows dll文件
MSYH_PACKAGE = os.path.join(MSYH_FILE_BASE_DIR, 'so文件/dll文件')

# 支付相关地址
MSYH_BASE_URL = ''

# 请求头
MSYH_HEADERS = {
    "origin": "origin添加"
}
