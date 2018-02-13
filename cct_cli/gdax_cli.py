# -*- coding: utf-8 -*-
'''
Created on 2018/2/5

@author: dyj6146
'''

import gdax

from shared_log.logger import logger


_gdax_cli_inst = None

def get_client():
    pass

def init_client(key, b64secret, passphrase, sandbox=True):
    _gdax_cli_inst = 