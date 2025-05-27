"""Soneium chain implementation for GM sending."""
import os
import asyncio
from web3 import Web3
from eth_account import Account

class Monad:
    """Monad chain implementation."""
    
    # Chain configuration
    NAME = "Monad"
    CHAIN_ID = 10143
    RPC_URL = os.getenv("MONAD_RPC_URL", "https://testnet-rpc.monad.xyz")
    GM_CONTRACT = "0x34287F1ceF9B009195B89801Ae4e2DFE708719aB"
    EXPLORER_URL = "https://testnet.monvision.io/tx/0x{tx_hash}"
    GM_FUNCTION = "0x5011b71c"  # GM function signature
    MIN_VALUE = 0.000029  # ETH value to send with transaction
    GAS_LIMIT = 300000
    
    def __init__(self):
        """Initialize the Monad chain handler."""
        self.web3 = Web3(Web3.HTTPProvider(self.RPC_URL))
        
    async def send_gm(self, private_key):
        """Send a GM transaction with the specified private key.
        
        Args:
            private_key: The private key to use for sending the transaction
            
        Returns:
            dict: Transaction result with success status and details
        """
        try:
            account = Account.from_key(private_key)
            wallet_address = account.address
            
            print(f"\nSending GM on {self.NAME} from {wallet_address[:6]}...{wallet_address[-4:]}")
            
            nonce = self.web3.eth.get_transaction_count(wallet_address)

            tx = {
                "from": wallet_address,
                "to": self.GM_CONTRACT,
                "data": self.GM_FUNCTION,
                "value": self.web3.to_wei(self.MIN_VALUE, "ether"),
                "gas": self.GAS_LIMIT,
                "gasPrice": self.web3.eth.gas_price,
                "nonce": nonce,
                "chainId": self.CHAIN_ID,
            }

            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash_hex = tx_hash.hex()
            tx_url = self.EXPLORER_URL.format(tx_hash=tx_hash_hex)
            print(f"Transaction sent: {tx_url}")

            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            result = {
                "chain": self.NAME,
                "wallet": wallet_address,
                "tx_hash": tx_hash_hex,
                "tx_url": tx_url,
                "success": receipt.status == 1
            }
            
            if result["success"]:
                print(f"✅ GM sent successfully on {self.NAME} from {wallet_address[:6]}...{wallet_address[-4:]}!")
            else:
                print(f"❌ GM sending error on {self.NAME} from {wallet_address[:6]}...{wallet_address[-4:]}, most likely 24 hours haven't still passed.")
                
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error sending GM on {self.NAME}: {error_msg}")
            return {
                "chain": self.NAME,
                "wallet": wallet_address if 'wallet_address' in locals() else "Unknown",
                "success": False,
                "error": error_msg
            } 