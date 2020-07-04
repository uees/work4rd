from django.db import models

from apps.basedata.models import Partner, Material, MEASURE


class SaleOrder(models.Model):
    """
    销售订单
    """
    STATUS = (
        ('0', "新订单"),
        ('1', "在生产"),
        ('4', "丢弃"),
        ('9', "已批准"),
        ('99', "已出库"),
    )

    code = models.CharField("订单号", max_length=64, blank=True, default='')
    partner = models.ForeignKey(Partner, verbose_name="客户", limit_choices_to={"partner_type": "C"},
                                on_delete=models.PROTECT)
    order_date = models.DateField("下单日期")
    deliver_date = models.DateField("交付日期")

    title = models.CharField("标题", max_length=128)
    memo = models.TextField("备注", blank=True, default='')
    contact = models.CharField("联系人", max_length=32, blank=True, default='')
    phone = models.CharField("电话", max_length=32, blank=True, default='')
    fax = models.CharField("传真", max_length=32, blank=True, default='')

    deliver_address = models.CharField("交付地址", max_length=128, blank=True, default='')
    invoice_type = models.CharField("发票类型", max_length=64, blank=True, default='')
    amount = models.DecimalField("金额", max_digits=12, decimal_places=2, blank=True, null=True, default=0.00)
    discount_amount = models.DecimalField("优惠额", max_digits=12, decimal_places=2, blank=True, null=True, default=0.00)
    status = models.CharField("状态", max_length=16, default='0', choices=STATUS)
    sale_man = models.CharField("业务员", max_length=32, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.code, self.title)

    class Meta:
        verbose_name = "销售订单"
        verbose_name_plural = verbose_name


class SaleItem(models.Model):
    """
    销售明细
    """
    master = models.ForeignKey(SaleOrder, on_delete = models.CASCADE)
    material = models.ForeignKey(Material,
                                 verbose_name="产品",
                                 limit_choices_to={"is_virtual": "0", 'can_sale': '1'},
                                 blank=True,
                                 null=True,
                                 on_delete = models.PROTECT)
    measure = models.CharField("计量单位", max_length=16, choices=MEASURE, default='kg')
    amount = models.DecimalField("数量", max_digits=14, decimal_places=4)
    sale_price = models.DecimalField("售价", max_digits=14, decimal_places=4, blank=True, null=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    deliver_date = models.DateField("交付日期")
    status = models.BooleanField("状态", default=0)
    memo = models.TextField("备注", blank=True, default='')

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = verbose_name
