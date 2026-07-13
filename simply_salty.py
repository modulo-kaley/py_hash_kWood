"""
@author Kaley Wood
Southern Alberta Institute of Technology: ITSC-320-D
Assignment: Implement a Simple Hash Function in Python
Created: 07-13-2026

HashTable — builds a fixed-size bucket array and resolves collisions with
separate chaining (a linked list per bucket). 

Also covers a salted hash function that turns a key + random salt into a fixed-size hex digest,
so a password (or any sensitive value) never has to be stored as itself.
"""

import os


class Node:
    """One link in a bucket's chain -- holds a key/value pair and points
    to whatever collided into the same bucket after it."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None  # next Node in this bucket's chain, or None if we're the last one


class HashTable:
    """A hash table with a fixed number of buckets, using separate chaining
    (linked lists) so multiple keys can safely share the same bucket."""

    def __init__(self, size=10):
        self.buckets = [None] * size

    def _hash(self, key):
        """Turns any key into a valid bucket index.

        Converts the key to a string, sums the ASCII value of every
        character, then folds that down to fit the bucket array with %.

        key: the value being hashed -- doesn't need to already be a string
        returns: an index guaranteed to fall inside self.buckets
        """
        return sum(ord(c) for c in str(key)) % len(self.buckets)

    def insert(self, key, value):
        """Stores a key/value pair, chaining onto the bucket if it's
        already occupied instead of overwriting whatever's there.

        key: the value to hash and store
        value: length of the word
        """
        index = self._hash(key)

        # bucket's untouched -- we're the first entry here
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
            print(f"Inserted key: {key} at index: {index}")
            return

        # bucket's already got a chain -- log who we're colliding with
        current = self.buckets[index]
        chain_preview = [current.key]
        while current.next is not None:
            current = current.next
            chain_preview.append(current.key)
        print(f"Collision at bucket index: {index} for key: {key}. Collides with: {chain_preview}")

        # Go through the chain and update in place if the key already exists,
        # otherwise tack a new Node onto the end
        current = self.buckets[index]
        while True:
            if current.key == key:
                print(f"Key: {key} already exists. Updating value.")
                current.value = value
                return
            if current.next is None:
                current.next = Node(key, value)
                print(f"Chained '{key}' after '{current.key}' at index: {index}")
                return
            current = current.next

    def search(self, key):
        """Looks a key up by walking its bucket's chain.

        key: the key to look for
        returns: the stored value, or None if the key was never inserted
        """
        index = self._hash(key)
        current = self.buckets[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def display(self):
        """Displays every bucket and its full chain to demonstrate
         linked-list structure and collision resolution."""
        print("Bucket | Chain")
        for bucket_index, node in enumerate(self.buckets):
            if node is None:
                print(f"{bucket_index:6} | (empty)")
                continue


            chain_parts = []
            current = node
            while current is not None:
                chain_parts.append(f"('{current.key}', {current.value})")
                current = current.next
            print(f"{bucket_index:6} | {' -> '.join(chain_parts)}")


def simple_hash(key):
    """The plain, un-chained version of the hash
    sums the ASCII values of the key's characters and folds it into a single digit.

    key: the value to hash
    returns: an int from 0-9
    """
    return sum(ord(c) for c in str(key)) % 10


def salted_hash(key, salt):
    """Combines an existing salt with a key and reduces the result to a
    fixed-size hex digest.

    Using a rolling multiply-add over every byte
    so the output spreads across the full range instead of clustering
    near zero.

    key: the value being hashed
    salt: random bytes (e.g. from os.urandom()) mixed in ahead of the key
    returns: an 8-character lowercase hex string
    """
    combined = salt + str(key).encode()

    MAGIC = 131        # small prime multiplier
    MASK = 0xFFFFFFFF  # keeps the running total inside 32 bits (8 hex digits)

    running_hash = 0
    for byte in combined:
        running_hash = (running_hash * MAGIC + byte) & MASK

    return f"{running_hash:08x}"


def generate_salted_hash(key):
    """Brand-new random salt and hashes the key with it.

    key: the value to hash
    returns: a (salt, hash) pair -- keep the salt, you'll need it again
    to reproduce this exact hash later
    """
    salt = os.urandom(8)
    return salt, salted_hash(key, salt)


def main():
    keys = ['apple', 'banana', 'orange', 'grape', 'kiwi',
            'melon', 'pear', 'peach', 'mango', 'plum']

    print("Hash values for keys:")
    for key in keys:
        print(f"Hash for {key}: {simple_hash(key)}")

    print("\nInserting values into the hash table:")
    table = HashTable()
    for key in keys:
        table.insert(key, len(key))

    print("\nSearching for values:")
    for key in keys:
        value = table.search(key)
        print(f"Value for {key}: {value}")

    print("\nFull table structure (proof of chaining):")
    table.display()

    # fresh random salt per key
    print("\nSalted hash for each key (fresh random salt per key):")
    for key in keys:
        salt, digest = generate_salted_hash(key)
        print(f"{key}: salt={salt.hex()}  hash={digest}")

    # Same key + saved salt should always reproduce the same hash
    print("\nConfirming a saved salt reproduces the same hash:")
    salt, digest = generate_salted_hash("apple")
    print(f"First hash of 'apple'  -> {digest}")
    replayed = salted_hash("apple", salt)
    print(f"Replayed with same salt -> {replayed}")
    print(f"Match: {digest == replayed}")


if __name__ == "__main__":
    main()