# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:05:35 2015

@author: dyj6146
"""

# import logging
import logging.config
import os

if not os.path.exists('logs'):
    os.mkdir('logs')
    
logging.config.fileConfig("config\\logger.ini")
logger = logging.getLogger()
