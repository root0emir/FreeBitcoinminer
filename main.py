import signal
from miner import ExitedThread, CoinMinerThread, NewSubscribeThread
import context as ctx
from utils import logg, timer
from colorama import Fore

yellow_ascii_art2 = """
\033[93m   
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣶⣶⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⡿⠿⠛⠛⠛⠛⠛⠛⠻⢿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣼⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣷⣄⠀⠀⠀⠀
⠀⠀⠀⣰⣿⡿⠋⠀⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀⠀⠈⢿⣿⣦⡀⠀⠀
⠀⠀⣸⣿⡿⠀⠀⠀⠸⠿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣶⣄⠀⠀⠀⠀⢹⣿⣷⠀⠀
⠀⢠⣿⡿⠁⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⢹⣿⣧⠀
⠀⣾⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⢀⣠⣿⣿⠟⠀⠀⠀⠀⠀⠈⣿⣿⠀
⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⠿⠿⠿⣿⣿⣥⣄⠀⠀⠀⠀⠀⠀⣿⣿⠀
⠀⢿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣧⠀⠀⠀⠀⢀⣿⣿⠀
⠀⠘⣿⣷⡀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⣼⣿⣿⡿⠀⠀⠀⠀⣸⣿⡟⠀
⠀⠀⢹⣿⣷⡀⠀⠀⢰⣶⣿⣿⣿⣷⣶⣶⣾⣿⣿⠿⠛⠁⠀⠀⠀⣸⣿⡿⠀⠀
⠀⠀⠀⠹⣿⣷⣄⠀⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀⠀⢀⣾⣿⠟⠁⠀⠀
⠀⠀⠀⠀⠘⢻⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣷⣶⣤⣤⣤⣤⣤⣤⣴⣾⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀

\033[0m
"""
print(yellow_ascii_art2)


green_ascii_art = """
\033[92m   
 ⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀
⠸⠿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣶⣄⠀
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠈⣿⣿⣿⠀
⠀⠀⢸⣿⣿⡇⠀⠀⢀⣠⣿⣿⠟⠀
⠀⠀⢸⣿⣿⡿⠿⠿⠿⣿⣿⣥⣄⠀
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣧
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⣼⣿⣿⣿
⢰⣶⣿⣿⣿⣷⣶⣶⣾⣿⣿⠿⠛⠁
⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀
\033[0m
"""



red_ascii_art = """
\033[91m

DEVELOPED BY

                 _    ___                 _      
 _ __ ___   ___ | |_ / _ \  ___ _ __ ___ (_)_ __ 
| '__/ _ \ / _ \| __| | | |/ _ \ '_ ` _ \| | '__|
| | | (_) | (_) | |_| |_| |  __/ | | | | | | |   
|_|  \___/ \___/ \__|\___/ \___|_| |_| |_|_|_|   
                                                 

\033[0m
"""
print(red_ascii_art)



def handler(signal_received, frame):
    ctx.fShutdown = True
    print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, 'Terminating Miner, Please Wait..')

def show_menu():
    print(green_ascii_art)
    print("Bitcoin Miner Configuration")
    print("1. Update Context Settings")
    print("2. Set Wallet Address")
    print("3. Start Mining")
    print("4. Exit")

def update_context_settings():
    nbits = input("Enter nbits: ")
    extranonce1 = input("Enter extranonce1: ")
    extranonce2_size = input("Enter extranonce2_size: ")
    coinb1 = input("Enter coinb1: ")
    coinb2 = input("Enter coinb2: ")
    merkle_branch = input("Enter merkle_branch (comma-separated): ").split(',')
    version = input("Enter version: ")
    ntime = input("Enter ntime: ")
    prevhash = input("Enter prevhash: ")
    ctx.update_context(nbits, extranonce1, extranonce2_size, coinb1, coinb2, merkle_branch, version, ntime, prevhash)
    print("Context settings updated.")

def set_wallet_address():
    address = input("Enter your Bitcoin wallet address: ")
    ctx.set_wallet_address(address)
    print("Wallet address set to:", address)

def StartMining():
    address = ctx.wallet_address
    if not address:
        print(Fore.RED, "Wallet address is not set. Please set it first.")
        return

    subscribe_t = NewSubscribeThread(None)
    subscribe_t.start()
    logg("[*] Subscribe thread started.")
    print(Fore.MAGENTA, "[", timer(), "]", Fore.GREEN, "[*] Subscribe thread started.")

    time.sleep(4)

    miner_t = CoinMinerThread(None)
    miner_t.start()
    logg("[*] Bitcoin Miner Thread Started")
    print(Fore.MAGENTA, "[", timer(), "]", Fore.GREEN, "[*] Bitcoin Miner Thread Started")
    print(Fore.BLUE, '*( ', Fore.YELLOW, 'Developer: root0emir', Fore.BLUE, ' )*')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            update_context_settings()
        elif choice == '2':
            set_wallet_address()
        elif choice == '3':
            StartMining()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")