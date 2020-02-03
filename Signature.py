from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class Signature:

  private_key = ""
  public_key = ""

  def __init__(self):
    key = RSA.generate(2048)
    self.private_key = key.export_key()
    file_out = open("temp/private_key.txt", "wb")
    file_out.write(self.private_key)

    self.public_key = key.publickey().export_key()
    file_out = open("temp/public_key.txt", "wb")
    file_out.write(self.public_key)

  def hash(self,message):
    return SHA256.new(message)

  def sign(self,hashed_msg):
    key = RSA.import_key(open('temp/private_key.txt').read())
    signature = pkcs1_15.new(key).sign(hashed_msg)
    return signature

  def verify(self,hashed_msg,signature):
    key = RSA.import_key(open('temp/public_key.txt').read())
    try:
        pkcs1_15.new(key).verify(hashed_msg, signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
      print("The signature is not valid.")