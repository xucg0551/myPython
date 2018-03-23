#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from proxypool.api import app
from proxypool.schedule import Schedule



# import os, sys
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proxypool'))
# import schedule


def main():
    s = Schedule()
    s.run()
    app.run()


if __name__ == '__main__':
    main()
