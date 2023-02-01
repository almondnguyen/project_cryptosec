import time
import threading
import pprint 

from phe import paillier

"""
The homomorphic properties of the Paillier crypto system are:

Encrypted numbers can be multiplied by a non encrypted scalar.
Encrypted numbers can be added together.
Encrypted numbers can be added to non encrypted scalars.

https://python-paillier.readthedocs.io/en/develop/
"""

def generate_keypair(n_length=2048):

    def animate():
        animations=['.  ', '.. ', '...', '.. ']

        animations_len = len(animations)
        i = 0

        start_time = time.time()
        while not done_generate_keys:
            print(f'Generating keys{animations[i]}\tTime elapsed: {time.time()-start_time:.3f} (s)', end='\r')
            i = (i + 1) % animations_len
            time.sleep(0.2)
    
    done_generate_keys = False
    threading.Thread(target=animate, daemon=True).start()

    public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)
    done_generate_keys = True
    
    print()
    print('Keys generated successfully:')
    print(f'\t Public key: {public_key}')
    print(f'\tPrivate key: {private_key}')

    return public_key, private_key

def print_numbers(message, a, b, prefix=''):
    print(message)
    print(f'\t{prefix}a = {a}')
    print(f'\t{prefix}b = {b}')
    print()

if __name__ == '__main__':
    public_key, private_key = generate_keypair(2048)  # default is 2048
    print()

    secret_a, secret_b = 3.1416, 20.02
    print_numbers('Secret numbers:', secret_a, secret_b, 'secret_')

    encrypted_a, encrypted_b = (public_key.encrypt(x) for x in (secret_a, secret_b))
    print_numbers('Encrypted numbers:', encrypted_a, encrypted_b, 'encrypted_')

    print('- Encrypted numbers can be multiplied by a non encrypted scalar')
    encrypted_a_mul_100_1 = encrypted_a * 100.1
    print(f'\tencrypted_a * 100.1 = {encrypted_a_mul_100_1}')
    print(f'\tdecrypt it ---------> {private_key.decrypt(encrypted_a_mul_100_1)}')
    print()

    print('- Encrypted numbers can be added together')
    encrypted_a_add_encrypted_b = encrypted_a + encrypted_b
    print(f'\tencrypted_a + encrypted_b = {encrypted_a_add_encrypted_b}')
    print(f'\tdecrypt it ---------------> {private_key.decrypt(encrypted_a_add_encrypted_b)}')
    print()

    print('- Encrypted numbers can be added to non encrypted scalars')
    encrypted_a_add_123_4 = encrypted_a + 123.4
    print(f'\tencrypted_a + 123.4 = {encrypted_a_add_123_4}')
    print(f'\tdecrypt it ---------> {private_key.decrypt(encrypted_a_add_123_4)}')
    print()