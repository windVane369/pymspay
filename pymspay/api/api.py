# -*- coding: utf-8 -*-

from optionaldict import optionaldict

from pymspay.api.base import MSYHPayBaseAPI
from pymspay.core.utils import json_2_str


class MSYHPay(MSYHPayBaseAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def query_payment_status(self, fn='GW02', cid=None, source='02', order_num=None, **kwargs):
        """
        接口类型： http
        交易名称： 支付查证
        交易码： GW02
        功能描述： 用于支付的查证[现金消费交易]交易
        公共内容说明： 是否必输：（Y必输/N非必输/C在特殊情况下必输）

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            03商户服务器接口请求
            04商户服务平台
            05行内业务平台
        :param order_num: 订单相关信息
        """
        cip_pss = optionaldict({
            'orderNum': order_num
        })
        data = optionaldict({
            "fn": fn,
            "cid": cid,
            "source": source,
            "cipPss": cip_pss
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/cmbcPay/queryPaymentStatus', data, **kwargs))

    def return_order(
            self, fn='GW03', cid=None, source='02', order_num=None,
            refund_types=None, back_amt=None, order_source_num=None, **kwargs
    ):
        """
        接口类型： http
        交易名称： 退货
        交易码： GW03
        功能描述： 用于支付的查证[现金消费交易]交易
        公共内容说明： 是否必输：（Y必输/N非必输/C在特殊情况下必输）

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            03商户服务器接口请求
            04商户服务平台
            05行内业务平台
        :param order_num: 退货单编号
        :param refund_types: 退款方式
        :param back_amt: 退款金额
        :param order_source_num: 原订单编号
        """
        cip_pss = optionaldict({
            'orderNum': order_num,
            'refundTypes': refund_types,
            'backAmt': back_amt,
            'orderSourceNum': order_source_num
        })
        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'cipPss': json_2_str(cip_pss)
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/cmbcCancel/returnOrder', data, **kwargs))

    def query_refund_status(self, fn='GW04', cid=None, source='02', order_num=None, **kwargs):
        """
        接口类型： http
        交易名称： 退货查证
        交易码： GW04
        功能描述： 用于退货的查证[现金消费退货交易]交易
        公共内容说明： 是否必输：（Y必输/N非必输/C在特殊情况下必输）

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            03商户服务器接口请求
            04商户服务平台
            05行内业务平台
        :param order_num: 原订单编号
        """
        cip_pss = optionaldict({
            'orderNum': order_num
        })
        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'cipPss': json_2_str(cip_pss)
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/cmbcCancel/queryRefundStatus', data, **kwargs))

    def download_file(
            self, fn='GW05', cid=None, source='02', account_date=None, start_time=None, end_time=None, **kwargs):
        """
        接口类型：http
        交易名称：日终对账
        交易码：GW05
        功能描述：用于每天订单数据的对账
        公共内容说明：是否必输：（Y必输/N非必输/C在特殊情况下必输）
        接口特殊说明：此接口返回为文件流，响应未加密

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            03商户服务器接口请求
            04商户服务平台
            05行内业务平台
        :param account_date: 订单支付时间
        :param start_time: 订单支付开始时间
        :param end_time: 订单支付结束时间
        """
        cip_pss = optionaldict({
            'accountDate': account_date,
            'startTime': start_time,
            'endTime': end_time
        })

        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'cipPss': json_2_str(cip_pss)
        })
        data = self._sign_and_encrypt(data)
        return self._post('/pay/cmbcCancel/downLoadFile', data, **kwargs)

    def per_paid_order(
            self, fn='GW10', cid=None, source='02', back_url=None, order_num=None, realy_order_amt=None,
            stage_pro_code=None, stage_num=None, id_number=None, rna_address=None, order_amt=None,
            is_activity=None, refund_types=None, is_stage=None, order_info=None, **kwargs
    ):
        """
        接口类型： 页面（通过表单提交至对应访问地址）
        交易名称：支付(存量客户支付)
        交易码：GW12
        功能描述：用于特约商户的消费类交易，支持[现金消费交易]交易
        公共内容说明：是否必输：（Y必输/N非必输/C在特殊情况下必输）
        接口特殊说明：多商编时请参照报文规范和接口使用说明中上送参数

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            02： mobile
        :param back_url: 回调地址
        :param order_num: 订单编号
        :param realy_order_amt: 订单金额
        :param stage_pro_code: 分期产品码
        :param stage_num: 分期期数
        :param id_number: 身份证号码
        :param rna_address: 第三方实名认证接口
        :param order_amt: 订单实付金额
        :param is_activity: 是否允许参加活动
        :param refund_types: 允许退款方式
        :param is_stage: 是否允许分期
        :param order_info: 订单的描述
        """
        cip_pss = optionaldict({
            'orderNum': order_num,
            'realyOrderAmt': realy_order_amt,
            'stageProCode': stage_pro_code,
            'stageNum': stage_num,
            'orderAmt': order_amt,
            'isActivity': is_activity,
            'refundTypes': refund_types,
            'is_stage': is_stage,
            'orderInfo': order_info
        })

        info = optionaldict({
            'idNumber': id_number,
            'rnaAddress': rna_address
        })

        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'backUrl': back_url,
            'cipPss': json_2_str(cip_pss),
            'info': json_2_str(info)
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/cmbcApply/perpaidOrder', data, **kwargs))

    def no_card_per_paid_order(
            self, fn='GW11', cid=None, source='02', back_url=None, order_num=None, realy_order_amt=None,
            stage_pro_code=None, stage_num=None, id_number=None, rna_address=None, **kwargs
    ):
        """
        接口类型：页面（通过表单提交至对应访问地址）
        交易名称：支付(无卡支付)
        交易码：GW11
        功能描述：用于特约商户的消费类交易，支持[现金消费交易]交易
        公共内容说明：是否必输：（Y必输/N非必输/C在特殊情况下必输）
        接口特殊说明：多商编时请参照报文规范和接口使用说明中上送参数

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            02： mobile
        :param back_url: 回调地址
        :param order_num: 订单编号
        :param realy_order_amt: 订单金额
        :param stage_pro_code: 分期产品码
        :param stage_num: 分期期数
        :param id_number: 身份证号码
        :param rna_address: 第三方实名认证接口
        """
        cip_pss = optionaldict({
            'orderNum': order_num,
            'realyOrderAmt': realy_order_amt,
            'stageProCode': stage_pro_code,
            'stageNum': stage_num
        })

        info = optionaldict({
            'idNumber': id_number,
            'rnaAddress': rna_address
        })

        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'backUrl': back_url,
            'cipPss': json_2_str(cip_pss),
            'info': json_2_str(info)
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/noCard/perpaidOrder', data, **kwargs))

    def has_card_per_paid_order(
            self, fn='GW12', cid=None, source='02', back_url=None, order_num=None, realy_order_amt=None,
            stage_pro_code=None, stage_num=None, id_number=None, rna_address=None, **kwargs
    ):
        """
        接口类型： 页面（通过表单提交至对应访问地址）
        交易名称：支付(存量客户支付)
        交易码：GW12
        功能描述：用于特约商户的消费类交易，支持[现金消费交易]交易
        公共内容说明：是否必输：（Y必输/N非必输/C在特殊情况下必输）
        接口特殊说明：多商编时请参照报文规范和接口使用说明中上送参数

        :param fn: 服务码
        :param cid: 商户编号
        :param source: 来源
            02： mobile
        :param back_url: 回调地址
        :param order_num: 订单编号
        :param realy_order_amt: 订单金额
        :param stage_pro_code: 分期产品码
        :param stage_num: 分期期数
        :param id_number: 身份证号码
        :param rna_address: 第三方实名认证接口
        """
        cip_pss = optionaldict({
            'orderNum': order_num,
            'realyOrderAmt': realy_order_amt,
            'stageProCode': stage_pro_code,
            'stageNum': stage_num
        })

        info = optionaldict({
            'idNumber': id_number,
            'rnaAddress': rna_address
        })

        data = optionaldict({
            'fn': fn,
            'cid': cid,
            'source': source,
            'backUrl': back_url,
            'cipPss': json_2_str(cip_pss),
            'info': json_2_str(info)
        })
        data = self._sign_and_encrypt(data)
        return self._decrypt_and_verify(self._post('/pay/hasCard/perpaidOrder', data, **kwargs))
