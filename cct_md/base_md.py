# -*- coding: utf-8 -*-
'''
Created on 2018/2/5

@author: dyj6146
'''
import abc


class BaseData(object):
    '''
    Abstract base class of data feeds
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        