# Generated by Django 3.0.7 on 2020-07-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0002_auto_20200704_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialcategory',
            name='spec',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='规格'),
        ),
        migrations.AlterField(
            model_name='materialcategory',
            name='code',
            field=models.CharField(db_index=True, max_length=64, verbose_name='代码'),
        ),
    ]
