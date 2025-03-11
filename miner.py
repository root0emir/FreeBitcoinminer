import binascii
import hashlib
import random
import socket
import requests
import threading
import time
import json
from colorama import Fore
import context as ctx
from utils import timer, logg

def get_current_block_height():
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])

def check_for_shutdown(t):
    n = t.n
    if ctx.fShutdown:
        if n != -1:
            ctx.listfThreadRunning[n] = False
            t.exit = True

class ExitedThread(threading.Thread):
    def __init__(self, arg, n):
        super(ExitedThread, self).__init__()
        self.exit = False
        self.arg = arg
        self.n = n

    def run(self):
        self.thread_handler(self.arg, self.n)
        pass

    def thread_handler(self, arg, n):
        while True:
            check_for_shutdown(self)
            if self.exit:
                break
            ctx.listfThreadRunning[n] = True
            try:
                self.thread_handler2(arg)
            except Exception as e:
                logg("ThreadHandler()")
                print(Fore.MAGENTA, '[', timer(), ']', Fore.WHITE, 'ThreadHandler()')
                logg(e)
                print(Fore.RED, e)
            ctx.listfThreadRunning[n] = False

            time.sleep(2)
            pass

    def thread_handler2(self, arg):
        raise NotImplementedError("must impl this func")

    def check_self_shutdown(self):
        check_for_shutdown(self)

    def try_exit(self):
        self.exit = True
        ctx.listfThreadRunning[self.n] = False
        pass

class CoinMinerThread(threading.Thread):
    def __init__(self, arg):
        super(CoinMinerThread, self).__init__()
        self.arg = arg
        self.exit = False

    def run(self):
        address = ctx.wallet_address
        bitcoin_miner(self, address)

    def stop(self):
        self.exit = True

class NewSubscribeThread(threading.Thread):
    def __init__(self, arg):
        super(NewSubscribeThread, self).__init__()
        self.arg = arg
        self.exit = False

    def run(self):
        address = ctx.wallet_address
        block_listener(self, address)

    def stop(self):
        self.exit = True

def bitcoin_miner(t, address, restarted=False):
    if restarted:
        logg('\n[*] Bitcoin Miner restarted')
        print(Fore.MAGENTA, '[', timer(), ']', Fore.BLUE, '[*] Bitcoin Miner Restarted')
        time.sleep(5)

    target = (ctx.nbits[2:] + '00' * (int(ctx.nbits[:2], 16) - 3)).zfill(64)
    extranonce2 = hex(random.randint(0, 2 ** 32 - 1))[2:].zfill(2 * ctx.extranonce2_size)

    coinbase = ctx.coinb1 + ctx.extranonce1 + extranonce2 + ctx.coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in ctx.merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()
    merkle_root = ''.join([merkle_root[i] + merkle_root[i + 1] for i in range(0, len(merkle_root), 2)][::-1])
    work_on = get_current_block_height()
    ctx.nHeightDiff[work_on + 1] = 0
    _diff = int("00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)

    logg('[*] Working to solve block with height {}'.format(work_on + 1))
    print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, '[*] Working to solve block with height {}'.format(work_on + 1))

    while True:
        t.check_self_shutdown()
        if t.exit:
            break

        if ctx.prevhash != ctx.updatedPrevHash:
            logg('[*] New block {} detected on network '.format(ctx.prevhash))
            print(Fore.YELLOW, '[', timer(), ']', Fore.MAGENTA, '[*] New block {} detected on network '.format(ctx.prevhash))
            logg('[*] Best difficulty while trying to solve block {} was {}'.format(work_on + 1, ctx.nHeightDiff[work_on + 1]))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.GREEN, '[*] Best difficulty while trying to solve block was {}'.format(work_on + 1, ctx.nHeightDiff[work_on + 1]))
            ctx.updatedPrevHash = ctx.prevhash
            bitcoin_miner(t, address, restarted=True)
            print(Fore.MAGENTA, '[', timer(), ']', Fore.BLUE, 'Bitcoin Miner Restart Now...')
            continue

        nonce = hex(random.randint(0, 2 ** 32 - 1))[2:].zfill(8)
        blockheader = ctx.version + ctx.prevhash + merkle_root + ctx.ntime + ctx.nbits + nonce + \
                      '000000800000000000000000000000000000000000000000000000000000000000000000000000000080020000'
        hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
        hash = binascii.hexlify(hash).decode()

        if hash.startswith('0000000'):
            logg('[*] New hash: {} for block {}'.format(hash, work_on + 1))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, '[*] New hash: {} for block {}'.format(hash, work_on + 1))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.BLUE, 'Hash:', str(hash))
        this_hash = int(hash, 16)
        difficulty = _diff / this_hash

        if ctx.nHeightDiff[work_on + 1] < difficulty:
            ctx.nHeightDiff[work_on + 1] = difficulty

        if hash < target:
            logg('[*] Block {} solved.'.format(work_on + 1))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, '[*] Block {} solved.'.format(work_on + 1))
            logg('[*] Block hash: {}'.format(hash))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, '[*] Block hash: {}'.format(hash))
            logg('[*] Blockheader: {}'.format(blockheader))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, '[*] Blockheader: {}'.format(blockheader))
            payload = bytes('{"params": ["' + address + '", "' + ctx.job_id + '", "' + ctx.extranonce2
                            + '", "' + ctx.ntime + '", "' + nonce + '"], "id": 1, "method": "mining.submit"}\n', 'utf-8')
            logg('[*] Payload: {}'.format(payload))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.BLUE, '[*] Payload:', Fore.GREEN, ' {}'.format(payload))
            sock.sendall(payload)
            ret = sock.recv(1024)
            logg('[*] Pool response: {}'.format(ret))
            print(Fore.MAGENTA, '[', timer(), ']', Fore.GREEN, '[*] Pool Response:', Fore.CYAN, ' {}'.format(ret))
            return True

def block_listener(t, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('solo.ckpool.org', 3333))
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    ctx.sub_details, ctx.extranonce1, ctx.extranonce2_size = response['result']
    sock.sendall(b'{"params": ["' + address.encode() + b'", "password"], "id": 2, "method": "mining.authorize"}\n')
    response = b''
    while response.count(b'\n') < 4 and not (b'mining.notify' in response): response += sock.recv(1024)

    responses = [json.loads(res) for res in response.decode().split('\n') if
                 len(res.strip()) > 0 and 'mining.notify' in res]
    ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = \
        responses[0]['params']
    ctx.updatedPrevHash = ctx.prevhash

    while True:
        t.check_self_shutdown()
        if t.exit:
            break

        response = b''
        while response.count(b'\n') < 4 and not (b'mining.notify' in response): response += sock.recv(1024)
        responses = [json.loads(res) for res in response.decode().split('\n') if
                     len(res.strip()) > 0 and 'mining.notify' in res]

        if responses[0]['params'][1] != ctx.prevhash:
            ctx.job_id, ctx.prevhash, ctx.coinb1, ctx.coinb2, ctx.merkle_branch, ctx.version, ctx.nbits, ctx.ntime, ctx.clean_jobs = \
                responses[0]['params']