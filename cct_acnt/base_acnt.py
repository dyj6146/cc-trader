# -*- coding: utf-8 -*-
'''
Created on 2018/2/5

@author: dyj6146
'''
import abc


class BaseAccount(object):
    '''
    Abstract base class of a trader account
    '''
    
    @abc.abstractmethod
    def __init__(self, params):
        '''
        Constructor
        '''
        
    @abc.abstractmethod
    def __