import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode
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
  iv = b64encode(cipher.iv).decode('utf-8')
  ct = b64encode(ct_bytes).decode('utf-8')
  k =  b64encode(key).decode('utf-8')
  result = json.dumps({'iv':iv, 'ciphertext':ct, 'key':k})
  print(result)
  return result

def decrypt(json_input):
  # shared key
  try:
      b64 = json.loads(json_input)
      iv = b64decode(b64['iv'])
      ct = b64decode(b64['ciphertext'])
      key = b64decode(b64['key'])
      cipher = AES.new(key, AES.MODE_OFB, iv=iv)
      pt = cipher.decrypt(ct)
      # print("The message was: ", pt)
      return pt
  except ValueError:
      print("Incorrect decryption")

def modeText():
  while True:
    print("""

███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║     ██║   ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██║╚██╗██║██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
███████╗██║ ╚████║╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                          
  """)
    print("Entering MODE Text")
    print("========================")
    print("ENTER 1 to Encrypt text file")
    print("ENTER 2 to Decrypt text file")
    print("ENTER 3 back to menu")
    print("========================")
    mode = input("What do you want ? : ")
    # Encryption
    if(mode == "1"):
      encrypt_text()
    # Decryption
    elif(mode == "2"):
      pass
    elif(mode == "3"):
      break

def encrypt_text():
  path = input("Enter your .txt file path : ")
  fileNameArr = path.split('/')
  fileName = fileNameArr[len(fileNameArr)-1]
  file_ = open(path,"r")
  data = file_.read()
  # encrypt text
  cipher = encrypt(data.encode("utf-8"))
  b64 = json.loads(cipher)
  cipher = b64['ciphertext']
  hashed_msg = signature.hash(cipher.encode())
  sig = signature.sign(hashed_msg)
  # write to file
  file_encrypt = open("encrypted/"+fileName,"wb")
  file_encrypt.write(b"=====     original text     ===== \n")
  file_encrypt.write(data.encode("utf-8"))
  file_encrypt.write(b"\n\n=====      AES cipher text      ===== \n")
  file_encrypt.write(b64encode(cipher.encode("utf-8")))
  file_encrypt.write(b"\n\n=====     hash SHA256 cipher text     ===== \n")
  file_encrypt.write(hashed_msg.hexdigest().encode())
  file_encrypt.write(b"\n\n=====  digital signature  ===== \n")
  file_encrypt.write(b64encode(sig))
  
  # decrypt
  file_encrypt.write(b"\n\n=====  decrypted text ===== \n")
  file_encrypt.write(decrypt(encrypt(data.encode("utf-8"))))
  file_encrypt.close()
  show_success()
  
def modeFile():
  while True:
    print("Entering Mode File")
    print("========================")
    print("ENTER 1 to Encrypt entire file")
    print("ENTER 2 to Decrypt entire file")
    print("ENTER 3 back to menu")
    print("========================")
    mode = input("What do you want ? : ")
    if(mode == "1"):
      encrypt_file()
      break
    elif(mode == "2"):
      decrypt_file()
      break
    elif(mode == "3"):
      break

def encrypt_file():
  path = input("Enter your file path : ")
  fileNameArr = path.split('/')
  fileName = fileNameArr[len(fileNameArr)-1]
  file_ = open(path,"rb")
  data = file_.read()
  cipher = encrypt(data)
  b64 = json.loads(cipher)
  # cipher = b64['ciphertext']
  # write to file
  file_encrypt = open("encrypted/"+fileName,"wb")
  file_encrypt.write(cipher.encode("utf-8"))
  file_encrypt.close()
  show_success()

def show_success():
  print("=========================")
  print("=========================")
  print("=========================")
  print("========SUCCESS==========")
  print("=========================")
  print("=========================")
  print("=========================")

def decrypt_file():
  # decrypt
  path = input("Enter your file path : ")
  fileNameArr = path.split('/')
  fileName = fileNameArr[len(fileNameArr)-1]
  file_ = open(path,"rb")
  data = file_.read()
  file_decrypt = open("decrypted/"+fileName,"wb")
  decrypted = decrypt(data.decode('utf-8'))
  file_decrypt.write(decrypted)
  file_decrypt.close()
  show_success()

def text_sig_verify(cipher,sig):
  signature.verify(cipher,sig)
  decrypt(cipher)
  
def main():
  while True:
    print("============================================")
    print("SELECT TYPE")
    print("MODE 1 = Text inside file")
    print("MODE 2 = Other file (entire file)")
    print("MODE 3 = Close program !!")
    print("============================================")
    mode = input("Select your MODE : ")
    if(mode == "1"):
      modeText()
    elif(mode == "2"):
      modeFile()
    elif(mode == "3"):
      break

if __name__ == "__main__":
  print("""

███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║     ██║   ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██║╚██╗██║██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
███████╗██║ ╚████║╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                          
  """)
  main()
