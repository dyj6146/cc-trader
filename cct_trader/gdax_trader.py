# -*- coding: utf-8 -*-
'''
Created on 2018/2/5

@author: dyj6146
'''

import time
import mmap
import gdax
import multiprocessing as mp

from .base_trader import BaseTrader
from cct_md.gdax_order_book import OrderBook

from shared_log.logger import logger


class GdaxTrader(BaseTrader):
    def __init__(self, params):
        # Constructor
        self.cli_auth = params['cli_auth']
        self.signal_src = params['signal_src']
        self.auth_client = None
        self.products = params['products']
        self.account_ids = {}
        self.order_books = {}
        self.algo = params['algo']
        self.algo_config = self._parse_algo_code(params['algo_code'])
        '''@TODO: Allocated capital on each products'''
        self.alloc_cap = params['alloc_cap']
        
    def initialize(self):
        # Initialize GDAX client
        logger.info('Initializing authenticated client...')
        self.auth_client = gdax.AuthenticatedClient(
            key=self.cli_auth['key'], 
            b64secret=self.cli_auth['b64secret'], 
            passphrase=self.cli_auth['passphrase'],
            api_url=self.cli_auth['api_url'])
        
        # Cancel all open orders
        logger.info('Cancelling all open orders...')
        is_cancelled = self.cancel_all_orders()
        if not is_cancelled:
            logger.error('Timeout reached, failed to cancel all orders')
            return 1
        
        # Get account ids
        acnts = self.get_accounts()
        logger.info(acnts)
        self.account_ids = dict([[acnt['currency'], acnt['id']] for acnt in acnts])

        '''
        {
            "id": "71452118-efc7-4cc4-8780-a5e22d4baa53",
            "currency": "BTC",
            "balance": "0.0000000000000000",
            "available": "0.0000000000000000",
            "hold": "0.0000000000000000",
            "profile_id": "75da88c5-05bf-4f54-bc85-5c775bd68254"
        },
        '''
        
        # Initialize order books
        self._init_order_book(self.products)
        
        return 0
    
    def run(self):
        # listen to the signal file
        for prod_id, src in self.signal_src:
            self.run_product(prod_id, src)
        logger.info('Trader ready, waiting for signals...')
    
    def run_product(self, prod_id, src):
        logger.info('Registering signal file for {0}: {1}'.format(prod_id, src))        
        m = mmap(-1, 1024, tagname=src, )
        
    def cancel_all_orders(self, product_id=None, timeout=60):
        is_cancelled = False
        s_time = time.time()
        self.auth_client.cancel_all(product=product_id)
        while time.time() - s_time < timeout:
            open_orders = self.get_open_orders(product_id=product_id)
            if len(open_orders) == 0:
                is_cancelled = True
                break
            time.sleep(0.5)
            logger.info('Cancelling {0} orders... {1:.2f} secs elapsed'\
                        .format(product_id if product_id is not None else 'all',
                                time.time() - s_time))
        return is_cancelled
    
    def cancel_order(self, order):
        logger.info('Cancelling order: {}'.format(order))
        resp = self.auth_client.cancel_order(order['id'])
        if 'message' in resp:
            logger.error('{0}: {1}'.format(order['id'], resp['message']))
            return 1
        return 0
    
    def rebalance(self, product_id, target_value, target_type):
        # Cancel all open orders for product if any
        open_orders = self.get_open_orders(product_id)
        if len(open_orders) > 0:        
            is_cancelled = self.cancel_all(product_id=product_id)
            if not is_cancelled: 
                return 1
        
        '''@TODO'''         
#         trade_func = self.auth_client.buy if bs_flag == 0 \
#             else self.auth_client.sell
#         # get price
#         order_px = self.order_books[product_id]
#         order_resp = trade_func(product_id=product_id, size=size)
        
    def get_open_orders(self, product_id=None):
        open_orders = self.auth_client.get_orders()
        if product_id is not None:
            open_orders = [order for order in open_orders 
                           if order["product_id"] == product_id]
        return open_orders
    
    def get_accounts(self):
        accounts = self.auth_client.get_accounts()
        accounts = dict([[acc['currency'], acc] for acc in accounts])        
        return accounts
    
    def get_account(self, currency):
        account = self.auth_client.get_account(self.account_ids[currency])
        return account

    def _init_order_book(self, products):
        # Initialize live order books
        for product_id in products:
            self.order_books[product_id] = OrderBook(product_id=product_id)
    
    @staticmethod
    def _parse_algo_code(algo_code_str):
        '''
        Example: P1|W5000|A0|W5000|A1|W5000|C
            - Passive: +1 tick
            - Wait 5000ms
            - Aggressive +0 tick
            - Wait 5000ms
            - Aggressive +1 tick
            - Wait 5000ms
            - Cancel all open orders
        '''
        res = []
        algo_code_seq = algo_code_str.split('|')
        for step in algo_code_seq:
            res.append({step[0]: int(step[1:])})
        return res
            
        
