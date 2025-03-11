# context.py
fShutdown = False
listfThreadRunning = [False, False]
nbits = ''
extranonce1 = ''
extranonce2_size = 0
coinb1 = ''
coinb2 = ''
merkle_branch = []
version = ''
ntime = ''
prevhash = ''
updatedPrevHash = ''
job_id = ''
clean_jobs = False
nHeightDiff = {}
wallet_address = ''

def update_context(new_nbits, new_extranonce1, new_extranonce2_size, new_coinb1, new_coinb2, new_merkle_branch, new_version, new_ntime, new_prevhash):
    global nbits, extranonce1, extranonce2_size, coinb1, coinb2, merkle_branch, version, ntime, prevhash
    nbits = new_nbits
    extranonce1 = new_extranonce1
    extranonce2_size = new_extranonce2_size
    coinb1 = new_coinb1
    coinb2 = new_coinb2
    merkle_branch = new_merkle_branch
    version = new_version
    ntime = new_ntime
    prevhash = new_prevhash

def set_wallet_address(address):
    global wallet_address
    wallet_address = address