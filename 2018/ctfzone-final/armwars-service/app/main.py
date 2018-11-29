import json
from os import system, environ

from flask import Flask, send_from_directory
app = Flask(__name__)

if environ.get("HOSTIP"):
    TEAM_ID =  int(environ["HOSTIP"].split(".")[2])
else:
    TEAM_ID = None
SHELLCODE = "AAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4AAAIOAAACDgAAAg4OL//+q+uv7K"

# Bots are encrypted using checker's public key (in order other teams won't steal yout bot). Don't change it!
@app.route("/get_shellcode")
def get_shellcode():
    # Encrypting bot with checker certificate
    with open("shellcode.enc", "wb") as f:
        if TEAM_ID == None:
            raise Exception("TEAM_ID is wrong")
        with open("shellcode", "w") as f:
            json.dump({
                "team": TEAM_ID,
                "shellcode": SHELLCODE
            }, f)

    system('openssl smime -encrypt -binary -aes-256-cbc -in shellcode -out shellcode.enc -outform DER certificate.pem')
    
    return send_from_directory('./', 'shellcode.enc')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=24311)

