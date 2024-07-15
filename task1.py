from Crypto import Random
import hashlib
import time
import random
import string
import matplotlib.pyplot as plt


## PART A
def sha256_hash(input_string, truncate_bits=256):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    digest = sha256.digest()
    # Truncate the digest to the specified number of bits
    truncated_digest = digest[:truncate_bits // 8]  # get the first N bytes
    return truncated_digest.hex()


## PART B
def flip_bit(input_string, bit_position):
    byte_array = bytearray(input_string.encode('utf-8'))
    byte_index = bit_position // 8
    bit_index = bit_position % 8
    byte_array[byte_index] ^= 1 << bit_index
    return byte_array.decode('utf-8', errors='ignore')


original_string = "Hello, world!"
hashes = []

# Flip a bit and hash the new string a few times
for i in range(5):
    modified_string = flip_bit(original_string, i)
    hash_original = sha256_hash(original_string)
    hash_modified = sha256_hash(modified_string)
    hashes.append((original_string, hash_original, modified_string, hash_modified))

# Print the results
for original, hash_orig, modified, hash_mod in hashes:
    print(f"Original string: '{original}'")
    print(f"SHA-256: {hash_orig}")
    print(f"Modified string: '{modified}'")
    print(f"SHA-256: {hash_mod}")
    print("="*60)

## PART C

def random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def find_collision(bits):
    hash_dict = {}
    attempts = 0
    start_time = time.time()
    while True:
        attempts += 1
        input_string = random_string()
        truncated_hash = sha256_hash(input_string, bits)
        if truncated_hash in hash_dict:
            collision_time = time.time() - start_time
            return hash_dict[truncated_hash], input_string, attempts, collision_time
        else:
            hash_dict[truncated_hash] = input_string

digest_sizes = list(range(8, 52, 2))
results = []
for bits in digest_sizes:
    print(f"Finding collision for {bits}-bit digest...")
    m0, m1, num_attempts, time_taken = find_collision(bits)
    results.append((bits, num_attempts, time_taken))
    print(f"Collision found for {bits}-bit digest:")
    print(f"Message 1: {m0}")
    print(f"Message 2: {m1}")
    print(f"Number of attempts: {num_attempts}")
    print(f"Time taken: {time_taken:.2f} seconds")
    print("="*60)


bits, attempts, times = zip(*results)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(bits, attempts, marker='o')
plt.title('Number of Inputs vs Digest Size')
plt.xlabel('Digest Size (bits)')
plt.ylabel('Number of Inputs')

plt.subplot(1, 2, 2)
plt.plot(bits, times, marker='o')
plt.title('Time Taken vs Digest Size')
plt.xlabel('Digest Size (bits)')
plt.ylabel('Time Taken (seconds)')

plt.tight_layout()
plt.show()