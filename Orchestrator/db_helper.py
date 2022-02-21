from .mongo import store_new_user, client
from .auth import get_crypto_context
import os

def setup_default_account():
    print(os.environ)
    cc = get_crypto_context()
    pwd_hash = cc.hash(os.environ['DEFAULT_ADMIN_PASSWORD'])

    if store_new_user(client['caelus'], 'admin', pwd_hash):
        print(f'Successfully created admin account')
    else:
        print(f'Failed to create admin account')