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

  def sign(self,message):
    # message = 'To be signed'
    # key = RSA.import_key(open('private_key.der').read())
    key = RSA.import_key(self.private_key)
    h = SHA256.new(message)
    signature = pkcs1_15.new(key).sign(h)
    return signature

  def verify(self,message,signature):
    key = RSA.import_key(open('temp/public_key.txt').read())
    h = SHA256.new(message)
    try:
        pkcs1_15.new(key).verify(h, signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
      print("The signature is not valid.")