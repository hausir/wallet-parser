# -*- coding: utf-8 -*-

import collections
import os

from bsddb3 import db

from .bc_data_stream import BCDataStream


class WalletParser:

    def __init__(self, filename):
        self.filename = filename
        self.data = collections.defaultdict(list)
        self.init()

    def init(self):
        """初始化"""

        filename = os.path.realpath(self.filename)
        env = db.DBEnv()
        env.set_lk_detect(db.DB_LOCK_DEFAULT)
        env.open(
            os.path.dirname(filename),
            db.DB_PRIVATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL | db.DB_CREATE,
        )
        d = db.DB(env)
        d.open(filename, 'main', db.DB_BTREE, db.DB_THREAD | db.DB_RDONLY)

        self.wallet_data = collections.OrderedDict((k, d[k]) for k in d.keys())

    def get_receiving_addresses(self):
        """解析标签和地址"""

        for key, value in self.wallet_data.items():
            kds = BCDataStream(key)
            vds = BCDataStream(value)
            _type = kds.read_string().decode()

            if _type == 'name':
                label = vds.read_string().decode()
                address = kds.read_string().decode()
                self.data[label].append(address)

        return self.data
