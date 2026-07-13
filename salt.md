**Storing a Password 101**

1. User submits password
2. A random salt is added
3. The salted password is hashed
4. <u><wbr>Only the hash and the salt are stored</u>
5. Login re-hashes and compares

**Salt - *the hidden spice* **

Salt is used so that hashing the same input more than once will never give the same result. What happens when two users have the same password? That's where salt comes in to save the day. By saving just the salt and regenerating the salt on every login, attackers are less likely to crack the hidden spice!
