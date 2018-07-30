# -*- coding: utf-8 -*-

import collections
import os

from bsddb3 import db

from .bc_data_stream import BCDataStream


class WalletParser:

    def __init__(self, filename):
        self.filename = filename
        self.addresses = collections.defaultdict(lambda: collections.defaultdict(list))
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

        wallet_data = collections.OrderedDict((k, d[k]) for k in d.keys())

        data = {}
        purpose = collections.defaultdict(list)
        for key, value in wallet_data.items():
            kds = BCDataStream(key)
            vds = BCDataStream(value)
            _type = kds.read_string().decode()

            if _type == 'name':
                label = vds.read_string().decode()
                address = kds.read_string().decode()
                data[address] = label
            elif _type == "purpose":
                category = vds.read_string().decode()
                address = kds.read_string().decode()
                purpose[category].append(address)

        for address, label in data.items():
            for category, addresses in purpose.items():
                if address in addresses:
                    self.addresses[category][label].append(address)

    def get_addresses(self):
        """获取所有地址"""

        return self.addresses

    def get_receiving_addresses(self):
        """获取收款地址"""

        return self.addresses.get("receive")

    def get_sending_addresses(self):
        """获取收款地址"""

        return self.addresses.get("send")
