#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import string
import random


def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])

print(id_generator())