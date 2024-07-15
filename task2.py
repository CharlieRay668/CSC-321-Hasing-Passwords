import nltk
from nltk.corpus import words
from bcrypt import *
import time
import threading

# Download and filter the word list
nltk.download('words')
word_list = words.words()
corpus = [word for word in word_list if 6 <= len(word) <= 10]

# Read the shadow file and extract salts
with open("shadow.txt", "r") as shadow_file:
    shadow_lines = shadow_file.readlines()

# Extract salts
salts = [password.split(":")[1].strip() for password in shadow_lines]

# Split corpus into chunks
chunk_size = 16384
corpi = [corpus[i:i + chunk_size] for i in range(0, len(corpus), chunk_size)]

# Create a threading event to signal when a password is found
password_found_event = threading.Event()

def check_passwords(corpus_chunk, salt, password_file, start_time):
    log_scale = 10
    for index, word in enumerate(corpus_chunk):
        if password_found_event.is_set():
            return  # Stop processing if the password is found in another thread
        if checkpw(word.encode(), salt.encode()):
            print(f"Password for {password_file} is {word}")
            # Write to file once a password is found
            with open(password_file, "a") as file:  # Use "a" mode to append
                file.write(f"{word}\n")
            password_found_event.set()  # Signal other threads to stop
            break
        if index % log_scale == 0:
            elapsed_time = time.time() - start_time
            if index == 0:
                time_remaining = 0
            else:
                time_remaining = elapsed_time / index * (len(corpus_chunk) - index)
            print(f"Attempted {index} passwords, elapsed time: {elapsed_time:.2f}s, time remaining: {time_remaining:.2f}s")
            log_scale *= 2

# Use threading for parallel processing
threads = []
for password in shadow_lines:
    password_file = password.split(":")[0] + ".txt"
    first_salt = password.split(":")[1].strip()
    start_time = time.time()
    password_found_event.clear()  # Reset the event for each new password
    for corpus_chunk in corpi:
        thread = threading.Thread(target=check_passwords, args=(corpus_chunk, first_salt, password_file, start_time))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

print("Password checking complete.")
