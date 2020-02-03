import json
from base64 import b16encode,b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b16decode,b64decode
import random
import string
from Signature import Signature
from Crypto.Hash import SHA256

signature = Signature()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt(data):
  key = get_random_bytes(32)
  cipher = AES.new(key, AES.MODE_OFB)
  ct_bytes = cipher.encrypt(data)
  iv = b16encode(cipher.iv).decode('utf-8')
  ct = b16encode(ct_bytes).decode('utf-8')
  k =  b16encode(key).decode('utf-8')
  result = json.dumps({'iv':iv, 'ciphertext':ct, 'key':k})
  print(result)
  return result

def decrypt(json_input):
  # shared key
  try:
      b16 = json.loads(json_input)
      iv = b16decode(b16['iv'])
      ct = b16decode(b16['ciphertext'])
      key = b16decode(b16['key'])
      cipher = AES.new(key, AES.MODE_OFB, iv=iv)
      pt = cipher.decrypt(ct)
      print("The message was: ", pt)
  except ValueError:
      print("Incorrect decryption")

def modeText():
  path = input("Enter your .txt file path : ")
  file_ = open(path,"r")
  data = file_.read()
  # encrypt text
  cipher = encrypt(data.encode("utf-8"))
  b16 = json.loads(cipher)
  cipher = b16['ciphertext']
  hashed_msg = signature.hash(cipher.encode())
  sig = signature.sign(hashed_msg)
  # write to file
  file_encrypt = open("result/text_enctrypted.txt","wb")
  file_encrypt.write(b"=====     original text     ===== \n")
  file_encrypt.write(data.encode("utf-8"))
  file_encrypt.write(b"\n\n=====      AES cipher text      ===== \n")
  file_encrypt.write(b64encode(cipher.encode("utf-8")))
  file_encrypt.write(b"\n\n=====     hash SHA256 cipher text     ===== \n")
  file_encrypt.write(hashed_msg.hexdigest().encode())
  file_encrypt.write(b"\n\n=====  digital signature  ===== \n")
  file_encrypt.write(b64encode(sig))

def text_sig_verify(cipher,sig):
  signature.verify(cipher,sig)
  decrypt(cipher)

def modeFile():
  pass

def main():
  while True:
    print("============================================")
    print("MODE 1 = Encrypt text inside file")
    print("MODE 2 = Encrypt other file (entire file)")
    print("============================================")
    mode = input("Select your MODE : ")
    if(mode == "1"):
      modeText()
      break
    elif(mode == "2"):
      fileText()
      break
if __name__ == "__main__":
  main()
