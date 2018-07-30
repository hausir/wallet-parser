# -*- coding: utf-8 -*-

import argparse

from .wallet_parser import WalletParser


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dat', help='wallet.dat path', required=True, dest='filename')
    args = ap.parse_args()

    wp = WalletParser(args.filename)
    receiving_addresses = wp.get_receiving_addresses()

    print('| %12s | %34s |' % ('label', 'address'))
    print('-' * 53)
    for label, addresses in receiving_addresses.items():
        if label == '':
            label = '(no label)'
        for address in addresses:
            print('| %12s | %34s |' % (label, address))


if __name__ == '__main__':
    main()
