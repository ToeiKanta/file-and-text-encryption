import json
from base64 import b16encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b16decode
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt(data):
  # data = b"secret"
  key = get_random_bytes(32)
  # key = randomString(32).encode()
  # print(key.decode())
  cipher = AES.new(key, AES.MODE_OFB)
  ct_bytes = cipher.encrypt(data)
  iv = b16encode(cipher.iv).decode('utf-8')
  ct = b16encode(ct_bytes).decode('utf-8')
  k =  b16encode(key).decode('utf-8')
  result = json.dumps({'iv':iv, 'ciphertext':ct, 'key':k})
  print(result)
  return result

def decrypt(json_input):
  # We assume that the key was securely shared beforehand
  try:
      b64 = json.loads(json_input)
      iv = b16decode(b64['iv'])
      ct = b16decode(b64['ciphertext'])
      key = b16decode(b64['key'])
      cipher = AES.new(key, AES.MODE_OFB, iv=iv)
      pt = cipher.decrypt(ct)
      print("The message was: ", pt)
  except ValueError:
      print("Incorrect decryption")

def main():
  print("==================")
  data = input("Please enter message:")
  result = encrypt(data.encode())
  decrypt(result)

if __name__ == "__main__":
  main()