#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Andre Augusto Giannotti Scota (https://sites.google.com/view/a2gs/)

import sys, os
from bitcoinlib.wallets import HDWallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic

def main(argv):
	if (len(argv) == 2 and argv[1] == '-h') or (len(argv) == 1):
		print('Usage:')
		print(f'{argv[0]} -h\n\tHelp')
		print(f'{argv[0]} -w <TYPE>\n\tWitness type. One of: \'p2sh-segwit\', \'segwit\' or \'legacy\' (default if -w not defined)')
		print(f'{argv[0]} -k <SIZE>\n\tKey size. One of: \'128\' (default if -k not defined. 12 words), \'256\' (24 words), \'512\' or \'1024\'')
		sys.exit(0)

	if '-w' in argv:
		try:
			witnesstype = argv[argv.index('-w') + 1]
		except IndexError:
			print(f'Witness value error: -w without value defined')
			sys.exit(0)

		if witnesstype not in ['p2sh-segwit', 'segwit', 'legacy']:
			print(f'Witness tpye error: Unknow {witnesstype}')
			sys.exit(0)

	else:
		witnesstype = 'p2sh-segwit'

	if '-k' in argv:
		try:
			keysize = int(argv[argv.index('-k') + 1])
		except IndexError:
			print(f'Key size error: -k without value defined')
			sys.exit(0)

		if keysize not in [128, 256, 512, 1024]:
			print(f'Key size error: Unknow {keysize}')
			sys.exit(0)

	else:
		keysize = 256

	walletname = "Wallet_Test"
	print(f'Configuration: witness type: [{witnesstype}] and key size: [{keysize}] (wallet name: {walletname})')

	passphrase = Mnemonic().generate(strength=keysize)
	w = HDWallet.create(walletname, keys=passphrase, witness_type=witnesstype, network='bitcoin')
	w.scan()
	balance = w.balance_update_from_serviceprovider()

	print(f'Passphrase: [{passphrase}] Balance: [{balance}]')

	if(balance == 0):
		wallet_delete(walletname)
	else:
		print(f'Wallet [{walletname}] NOT DELETED from DATABASE!')

if __name__ == '__main__':
	main(sys.argv)
	sys.exit(0)
