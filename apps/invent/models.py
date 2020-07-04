from django.db import models

from apps.basedata.models import Material, MEASURE


class MinimumInventory(models.Model):
    """最低库存(索引)"""
    title = models.CharField("标题", max_length=128)  # 例如 "2020-05 建议最低库存"
    execute_time = models.DateTimeField("执行时间", blank=True, null=True)


class MinimumInventoryItem(models.Model):
    """最低库存(项)"""
    master = models.ForeignKey(MinimumInventory, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name="物料",
                                 null=True, on_delete=models.CASCADE)
    measure = models.CharField("计量单位", max_length=16, choices=MEASURE, default='kg')
    amount = models.DecimalField("数量", max_digits=14, decimal_places=2)

    def __str__(self):
        des = self.material.spec or ''
        return '%s %s %s' % (self.material.code, self.material.name, des)

    class Meta:
        verbose_name = "最低库存"
        verbose_name_plural = verbose_name


class Inventory(models.Model):
    """
    库存索引
    """

    title = models.CharField("标题", max_length=128)  # 例如 "2020-05-06 库存明细"
    execute_time = models.DateTimeField("执行时间", blank=True, null=True)

    class Meta:
        verbose_name = "库存索引"
        verbose_name_plural = verbose_name


class InventoryDetail(models.Model):
    """库存信息"""
    master = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name="物料", on_delete=models.PROTECT)
    measure = models.CharField("计量单位", max_length=16, choices=MEASURE, default='kg')
    amount = models.DecimalField("数量", max_digits=14, decimal_places=4)
    batch = models.CharField("批号", max_length=32, blank=True, default='')
    product_date = models.DateTimeField("生产日期")

    def __str__(self):
        des = self.material.spec or ''
        return '%s %s %s' % (self.material.code, self.material.name, des)

    class Meta:
        verbose_name = "库存信息"
        verbose_name_plural = verbose_name
        ordering = ['material']


class ProductFlow(models.Model):
    """
    产品流水
    """

    TYPES = (
        (1, "产品进仓"),
        (2, "待转成"),
        (3, "改标进仓"),
        (4, "+调整库存"),
        (5, "成转待"),
        (6, "销售"),
        (7, "-调整库存"),
    )

    created_at = models.DateTimeField("创建日期", auto_now_add=True)
    product_date = models.DateTimeField("生产日期")
    material = models.ForeignKey(Material, verbose_name="物料", limit_choices_to={"is_virtual": "0"},
                                 blank=True, null=True, on_delete=models.PROTECT)
    measure = models.CharField("计量单位", max_length=16, choices=MEASURE, default='kg')
    amount = models.DecimalField("数量", max_digits=14, decimal_places=4, blank=True, null=True)
    batch = models.CharField("批号", max_length=32, blank=True, default='')
    type = models.SmallIntegerField("业务类别", choices=TYPES, default=1)
    memo = models.TextField("备注", blank=True, default='')

    class Meta:
        verbose_name = "产品流水"
        verbose_name_plural = verbose_name
