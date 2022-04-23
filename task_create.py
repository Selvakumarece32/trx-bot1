import random
from main import mydb, bot

from tronpy import T
from tronpy.keys import PrivateKey

# integers representing half & one Tron
HALF_TRON = 500000
ONE_TRON = 1000000

# your wallet information
WALLET_ADDRESS = "TEo84EXz7ZmaQkLXPwmkLnEhQd1DqH2DNU"
PRIVATE_KEY = "009faab68456edf92132cc74a580316d159bdc10a544bda7f82a52175968a323"

# connect to the Tron blockchain
client = Tron()


# send some 'amount' of Tron to the 'wallet' address
def send_tron(amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(WALLET_ADDRESS, str(wallet), int(amount))
                .memo("Transaction Description")
                .build()
                .inspect()
                .sign(priv_key)
                .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        return txn.wait()

    # return the exception
    except Exception as ex:
        return ex
