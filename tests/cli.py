# -*- coding: utf-8 -*-
from pymspay.api.api import MSYHPay
from pymspay.base import BaseClient

pay = MSYHPay(client=BaseClient(cid='30510001520K224'))


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
