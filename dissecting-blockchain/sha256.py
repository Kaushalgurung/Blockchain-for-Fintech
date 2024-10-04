from hashlib import sha256

data = "COMP1830-Blockchain for Fintech!"

h = sha256()
h.update(data.encode())

print(h.hexdigest())