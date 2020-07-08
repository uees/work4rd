import glob
import os

from pywintypes import com_error  # noqa
from win32com.client import Dispatch


def xls2xlsx(origin_dir: str, to_dir: str):
    """
    :param origin_dir: xls 文件夹路径
    :param to_dir: 要保存的路径
    :return:
    """
    files = glob.glob(f"{origin_dir}/**/*.xls*", recursive=True)
    excel = Dispatch("Excel.Application")
    excel.Visible = False

    for filepath in files:
        if os.path.basename(filepath).startswith('~$'):
            # 删除 office 临时文件
            os.remove(filepath)

        print(f"开始转化 {filepath}")
        try:
            workbook = excel.Workbooks.Open(filepath)

            new_filepath = filepath.replace(origin_dir, to_dir)
            new_file_dir = os.path.dirname(new_filepath)
            if not os.path.exists(new_file_dir):
                os.makedirs(new_file_dir)

            # xlWorkbookDefault = 51, FileFormat=51 表示用 Excel2007 或 2010 的格式（*.xlsx）来储存
            workbook.SaveAs(Filename=new_filepath, FileFormat=51)
            workbook.Close()
            print(f"转化成功 {new_filepath}")
        except com_error:
            print(f"转化 {filepath} 失败")
            continue

    excel.Quit()
