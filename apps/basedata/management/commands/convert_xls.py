from django.core.management.base import BaseCommand, CommandError

from tools.formula.converter import xls2xlsx


class Command(BaseCommand):
    help = '批量把 Excel2003 格式文件转为 Excel2007 格式'

    def add_arguments(self, parser):
        parser.add_argument('--path', help='配方目录', )
        parser.add_argument('--to', help='转化后保存目录', )

    def handle(self, *args, **options):
        if not options['path'] or not options['to']:
            raise CommandError("未知参数")

        xls2xlsx(options['path'], options['to'])
        self.stdout.write(self.style.SUCCESS("转化完成"))
