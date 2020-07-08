from django.db import models

MEASURE = (
    ('kg', "千克"),
    ('ge', "个"),
    ('gal', "加仑"),
    ('ratio', "比率"),
)


class MaterialCategory(models.Model):
    """
    物料分类 fk=self
    """
    parent = models.ForeignKey('self', verbose_name="父类", null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField("代码", max_length=64, db_index=True)
    spec = models.CharField("规格", max_length=256, blank=True, default='')
    name = models.CharField("名称", max_length=128, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name


class Material(models.Model):
    """
    物料 fk=MaterialCategory
    """

    # A0103
    code = models.CharField("材料代码", max_length=20, db_index=True)
    barcode = models.CharField("条形码", max_length=40, blank=True, default='', db_index=True)
    name = models.CharField("材料名称", max_length=120, db_index=True)
    spec = models.CharField("规格", max_length=120, blank=True, default='')
    category = models.ForeignKey(MaterialCategory, verbose_name="类别", blank=True, null=True, on_delete=models.PROTECT)
    status = models.BooleanField("是否在用", default=True)
    formula = models.ForeignKey("development.Formula", verbose_name="配方", blank=True, null=True, on_delete=models.SET_NULL)
    # 设备？
    is_equip = models.BooleanField("是否设备", default=False)
    # 可销售
    can_sale = models.BooleanField("可销售", default=True)
    # 虚拟？
    is_virtual = models.BooleanField("虚拟", default=False)

    def __str__(self):
        return "%s %s %s" % (self.code, self.name, self.spec)

    class Meta:
        verbose_name = "材料"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = ("code", "name", "spec")


class Partner(models.Model):
    """
    合作伙伴
    """

    PARTNER_TYPE = (
        ('C', "客户"),
        ('S', "供应商"),
    )

    LEVEL = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    code = models.CharField("代码", max_length=32, blank=True, default='')
    name = models.CharField("名称", max_length=128, db_index=True)
    short = models.CharField("简称", max_length=64, blank=True, default='')
    partner_type = models.CharField("类别", max_length=16, choices=PARTNER_TYPE, default='C')
    level = models.CharField("等级", max_length=16, choices=LEVEL, default='C')

    tax_num = models.CharField("纳税识别号", max_length=64, blank=True, default='')
    tax_address = models.CharField("开票地址", max_length=128, blank=True, default='')
    tax_account = models.CharField("发票开户行", max_length=64, blank=True, default='')

    contacts = models.CharField("联系人", max_length=64, blank=True, default='')
    phone = models.CharField("联系电话", max_length=64, blank=True, default='')
    memo = models.TextField("备注", blank=True, default='')

    class Meta:
        verbose_name = "合作伙伴"
        verbose_name_plural = verbose_name
        permissions = (
            ('view_all_customer', "查看所有客户"),
            ('view_all_supplier', "查看所有供应商"),
        )
