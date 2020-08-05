# -*- coding: utf-8 -*-
from pymspay.api.api import MSYHPay
from pymspay.client import Client
from pymspay.core.signature import SignatureCertification


class Context(SignatureCertification):
    # 商家编号加密私钥
    MSYH_PRIVATE_FILE = '123123'
    # 商家密码
    MSYH_PRIVATE_FILE_PASSWORD = 'cmbc123'
    # 银行公钥
    MSYH_CERT_FILE = 'sdfsafd'
    # 加密解密的第三方包
    # # Linux so文件
    # # Windows dll文件
    MSYH_PACKAGE = 'sdfsdf.so'


context = Context()
pay = MSYHPay(
    client=Client(
        cid='30510001520K224',
        api_base_url='http://www/baidu.com',
        headers={'origin': 'http://www.baidu.com'}
    ),
    context=context
)


def download_file():
    df = pay.download_file(
        fn='GW05',
        source='01',
        account_date='2019-06-04-00:00:00',
        start_time='2019-06-13 00:00:00',
        end_time='2019-06-13 23:23:23'
    )
    print(df)


def query_payment_status():
    qps = pay.query_payment_status(
        fn='GW02',
        source='01',
        order_num='46313123245612333'
    )
    print(qps)


def per_paid_order():
    ppo = pay.per_paid_order(
        fn='GW10',
        source='02',
        back_url='https://test-p.pxjy.com/api/pay/test',
        order_num='46313123245610933',
        realy_order_amt='1000',
        refund_types='3',
        is_activity='0',
        is_stage='0',
        stage_num='',
        stage_pro_code='',
        order_amt='',
        order_info='',
        id_number=''
    )
    print(ppo)


if __name__ == '__main__':
    # download_file()
    # query_payment_status()
    per_paid_order()
