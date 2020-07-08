import glob
import logging
import os

from django.core.management.base import BaseCommand, CommandError

from apps.development.service import add_formula
from tools.formula.parser import FormulaParser

logger = logging.getLogger("work4rd")


class Command(BaseCommand):
    help = '读取 Excel2007 格式的配方, 导入到数据库'

    def add_arguments(self, parser):
        parser.add_argument('--path', help='配方目录', )
        parser.add_argument('--status', help='配方状态', )

    def handle(self, *args, **options):
        if not options['path'] or not options['status']:
            raise CommandError("未知参数")

        if options['status'] == "正式":
            options['status'] = "OFFICIAL"
        elif options['status'] == "待确认":
            options['status'] = "PAUSE"
        elif options['status'] == "试样" or options['status'] == "中试":
            options['status'] = "TEST"

        if os.path.isdir(options['path']):
            formula_files = glob.glob(f"{options['path']}/**/*.xlsx", recursive=True)
            for filepath in formula_files:
                if filepath.startswith('~$'):
                    continue

                self.add_formula(filepath, options['status'])

        elif os.path.isfile(options['path']):
            self.add_formula(options['path'], options['status'])

        else:
            raise CommandError("路径有误")

        self.stdout.write(self.style.SUCCESS("转化完成"))

    def add_formula(self, filepath, status):
        logger.info(f"开始解析{filepath}")
        parser = FormulaParser(filepath)
        formulas = parser.parse()
        for data in formulas:
            add_formula(data, status)
