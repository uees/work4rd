from django.db import models

from apps.basedata.models import MEASURE, Material, MaterialCategory


class Formula(models.Model):
    """
    物料的配方
    """
    STATUS_TYPE = (
        ('OFFICIAL', "正式"),
        ('TEST', "中试"),
        ('PAUSE', "待确认"),
        ('DEV', "开发"),
        ('INVALID', "作废"),
    )
    PROCESSING_METHODS = (
        ('MAKE', "制造"),
        ('PACKAGE', "组装"),
        ('SPLIT', "分装"),
    )

    name = models.CharField("配方名称", max_length=128)
    version = models.CharField("配方版本", max_length=32, blank=True, default='')
    per_weight = models.DecimalField("每份重量", max_digits=10, decimal_places=4, blank=True, null=True)
    category = models.ForeignKey(MaterialCategory, verbose_name="类别", blank=True, null=True, on_delete=models.PROTECT)
    status = models.CharField("状态", default='DEV', choices=STATUS_TYPE, max_length=16)
    processing_way = models.CharField("加工方式", default='PACKAGE', choices=PROCESSING_METHODS, max_length=16)
    authors = models.CharField("开发负责人", max_length=64, blank=True, null=True)
    memo = models.CharField("备注", max_length=256, blank=True, null=True)
    history = models.TextField("修改历史", blank=True, null=True)
    created_at = models.DateTimeField("创建日期", auto_now_add=True)
    updated_at = models.DateTimeField("修改日期", null=True, blank=True)
    official_at = models.DateTimeField("转正日期", null=True, blank=True)
    drop_at = models.DateTimeField("作废日期", null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.name, self.version)

    def save(self, *args, **kwargs):
        if not self.version:
            self.version = 'V%03d' % (Formula.objects.filter(name=self.name).all().count() + 1,)
        super().save(*args, **kwargs)

        if self.status == 'OFFICIAL':  # 一个物料同时只能有一个正式配方
            Formula.objects.filter(name=self.name, status='OFFICIAL').exclude(id=self.id) \
                .update(status='INVALID')

        # todo init self.per_weight

    class Meta:
        verbose_name = "配方"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class FormulaMeta(models.Model):
    formula = models.ForeignKey(Formula, verbose_name="配方", on_delete=models.CASCADE)
    name = models.CharField("配方名称", max_length=128)
    value = models.CharField("配方名称", max_length=256)

    class Meta:
        verbose_name = "配方Meta"
        verbose_name_plural = verbose_name


class FormulaDetail(models.Model):
    """
    配方成分
    """
    DATA_TYPE = (
        ('STR', 'STRING'),
        ('NUM', 'NUMBER'),
        ('RATIO', 'RATIO'),
    )

    formula = models.ForeignKey(Formula, verbose_name="配方", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name="物料", on_delete=models.PROTECT)
    workshop = models.CharField("车间", max_length=64, blank=True, default='')
    measure = models.CharField("计量单位", max_length=16, choices=MEASURE, default='kg')
    value_type = models.CharField("数据类型", default='NUM', choices=DATA_TYPE, max_length=16)
    value = models.CharField("数据值", blank=True, default='', max_length=64)
    memo = models.CharField("备注", max_length=256, default='', blank=True)

    def __str__(self):
        return '%s %s %s' % (self.material.name, self.value, self.measure)

    class Meta:
        verbose_name = "配方成分"
        verbose_name_plural = verbose_name
        ordering = ['workshop']
