import requests 
from colorama import *

ETHERSCAN_API_KEY = 'YOUR_ETHERSCAN_API_KEY'
SNOWTRACE_API_KEY = 'YOUR_SNOWTRACE_API'

print(Fore.CYAN + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢯⠙⠩⠀⡇⠊⠽⢖⠆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠱⣠⠀⢀⣄⠔⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣷⣶⣾⣾⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡔⠙⠈⢱⡟⣧⠀⠀⠀⠀⠀⠀⠀                                    Wallet Transfer
⠀⠀⠀⠀⠀⡠⠊⠀⠀⣀⡀⠀⠘⠕⢄⠀              
⠀⠀⠀⢀⠞⠀⠀⢀⣠⣿⣧⣀⠀⠀⢄⠱⡀⠀⠀⠀        * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     
⠀⠀⡰⠃⠀⠀⢠⣿⠿⣿⡟⢿⣷⡄⠀⠑⢜⠀⠀         * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
⠀⢰⠁⠀⠀⠀⠸⣿⣦⣿⡇⠀⠛⠋⠀⠨⡐⢍⠀         * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
⠀⡇⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣦⡀⠀⢀⠨⡒⠙⡄        * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,    
⢠⠁⡀⠀⠀⠀⣤⡀⠀⣿⡇⢈⣿⡷⠀⠠⢕⠢⠁⡇        * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN  
⠸⠀⡕⠀⠀⠀⢻⣿⣶⣿⣷⣾⡿⠁⠀⠨⣐⠨⢀⠃        * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
⠀⠣⣩⠘⠀⠀⠀⠈⠙⣿⡏⠁⠀⢀⠠⢀⡂⢉⠎⠀
⠀⠀⠈⠓⠬⢀⣀⠀⠀⠈⠀⠀⠀⢐⣬⠴⠒⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀
""")

def show_transaction_details(transactions, blockchain):
    for i, tx in enumerate(transactions):
        print(f"\nTransaction {i + 1}:")
        
        if blockchain == "bitcoin":
            print(f"Hash: {tx['hash']}")
            print(f"Montant total: {sum(output['value'] for output in tx['out']) / 10**8} BTC")
            print("Envoyé vers:")
            for output in tx['out']:
                print(f" - {output.get('addr', 'Adresse non spécifiée')} : {output['value'] / 10**8} BTC")
            print(f"Nombre de confirmations: {tx.get('confirmations', 'Non spécifié')}")
            print(f"Date: {tx['time']}")  

        elif blockchain == "litecoin":
            tx_hash = tx['tx_hash']
            get_litecoin_transaction_details(tx_hash)

        else:
            print(f"Hash: {tx['hash']}")
            print(f"De: {tx['from']}")
            print(f"À: {tx['to']}")
            print(f"Montant: {int(tx['value']) / 10**18}")
            print(f"Confirmations: {tx.get('confirmations', 'Non spécifié')}")
            print(f"Date: {tx['timeStamp']}") 

def get_litecoin_transaction_details(tx_hash):
    url = f"https://api.blockcypher.com/v1/ltc/main/txs/{tx_hash}"
    response = requests.get(url)
    tx_details = response.json()
    
    print(f"Hash: {tx_details.get('hash', 'Non spécifié')}")
    print(f"Montant total: {sum(output.get('value', 0) for output in tx_details.get('outputs', [])) / 10**8} LTC")
    print("Envoyé vers:")
    for output in tx_details.get('outputs', []):
        print(f" - {output.get('addresses', ['Adresse non spécifiée'])[0]} : {output.get('value', 0) / 10**8} LTC")
    print(f"Confirmations: {tx_details.get('confirmations', 'Non spécifié')}")
    print(f"Bloc: {tx_details.get('block_height', 'Non spécifié')}")

def get_bitcoin_wallet_info(address):
    url = f"https://blockchain.info/rawaddr/{address}"
    response = requests.get(url)
    data = response.json()

    balance = data['final_balance'] / 10**8  
    transactions = data['txs']

    print(f"Bitcoin Wallet: {address}")
    print(f"Solde: {balance} BTC")
    print(f"Nombre de transactions: {len(transactions)}")

    input("\nAppuyez sur Entrée pour afficher plus d'informations sur les transactions...")
    show_transaction_details(transactions, "bitcoin")

def get_ethereum_wallet_info(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    balance = int(response.json()['result']) / 10**18  # Conversion en ETH

    url_tx = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response_tx = requests.get(url_tx)
    transactions = response_tx.json()['result']

    print(f"Ethereum Wallet: {address}")
    print(f"Solde: {balance} ETH")
    print(f"Nombre de transactions: {len(transactions)}")

    input("\nAppuyez sur Entrée pour afficher plus d'informations sur les transactions...")
    show_transaction_details(transactions, "ethereum")

def get_litecoin_wallet_info(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    response = requests.get(url)
    balance = response.json()['balance'] / 10**8  # Conversion en LTC

    url_tx = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}"
    response_tx = requests.get(url_tx)
    transactions = response_tx.json()['txrefs']

    print(f"Litecoin Wallet: {address}")
    print(f"Solde: {balance} LTC")
    print(f"Nombre de transactions: {len(transactions)}")

    input("\nAppuyez sur Entrée pour afficher plus d'informations sur les transactions...")
    show_transaction_details(transactions, "litecoin")

def get_avax_wallet_info(address):
    url = f"https://api.snowscan.xyz/api?module=account&action=balance&address={address}&tag=latest&apikey={SNOWTRACE_API_KEY}"
    response = requests.get(url)
    balance = int(response.json()['result']) / 10**18

    url_tx = f"https://api.snowscan.xyz/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={SNOWTRACE_API_KEY}"
    response_tx = requests.get(url_tx)
    transactions = response_tx.json()['result']

    print(f"Avalanche Wallet: {address}")
    print(f"Solde: {balance} AVAX")
    print(f"Nombre de transactions: {len(transactions)}")

    input("\nAppuyez sur Entrée pour afficher plus d'informations sur les transactions...")
    show_transaction_details(transactions, "avax")

def get_wallet_info(wallet_address, blockchain):
    if blockchain.lower() == 'bitcoin':
        get_bitcoin_wallet_info(wallet_address)
    elif blockchain.lower() == 'ethereum':
        get_ethereum_wallet_info(wallet_address)
    elif blockchain.lower() == 'litecoin':
        get_litecoin_wallet_info(wallet_address)
    elif blockchain.lower() == 'avax':
        get_avax_wallet_info(wallet_address)
    else:
        print("Blockchain non supportée. Choisissez entre 'bitcoin', 'ethereum', 'litecoin', 'avax'.")

wallet_address = input("Entrez l'adresse du wallet: ")
blockchain = input("Entrez la blockchain (bitcoin, ethereum, litecoin, avax): ")
get_wallet_info(wallet_address, blockchain)
