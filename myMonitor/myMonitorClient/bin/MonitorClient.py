#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import sys, os

#获取父父级目录，追加到模块寻找路径中，不然会引起 from core import main寻找不到模块
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main


if __name__ == '__main__':
    main.CommandHandler(sys.argv)
