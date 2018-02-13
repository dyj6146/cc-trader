# -*- coding: utf-8 -*-
'''
Created on 2018/2/5

@author: dyj6146
'''
import abc


class BaseTrader(object):
    '''
    Abstract base class of a trader
    '''

    @abc.abstractmethod
    def __init__(self, params):
        '''
        Constructor
        '''
    
    @abc.abstractmethod
    def submit_buy_order(self):
        '''
        Submit a new buy order
        '''
        
    @abc.abstractmethod
    def submit_sell_order(self):
        '''
        Submit a new sell order
        '''
    
    @abc.abstractmethod
    def cancel_order(self):
        '''
        Cancel an existing order
        '''        
    
    @abc.abstractmethod
    def query_order(self):
        '''
        Get order status
        '''        