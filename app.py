from flask import Flask, request, jsonify
import requests
import my_pb2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

app = Flask(__name__)

AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

@app.route('/change-logo/<int:uid>', methods=['GET'])
def change_logo(uid):
    token = request.args.get('token', '')  # خيار تمرير التوكن عبر الرابط

    message = my_pb2.UserProfile()
    message.uid = uid
    message.bio = "BOT MOD V1"
    message.field3 = "BOT MOD V1"
    message.field4 = 1
    message.field5 = 499999
    message.avatar = 3  # تغيير اللوغو إلى رقم 3
    message.frame = 3   # تغيير إطار اللوغو أيضًا

    serialized_message = message.SerializeToString()
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_message)

    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "100-continue",
        'Authorization': f"Bearer {token}",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB48"
    }

    try:
        response = requests.post(
            "https://clientbp.ggblueshark.com/ModifyClanInfo",
            data=encrypted_data,
            headers=headers
        )
        return jsonify({
            'status': 'logo changed to 3',
            'response_hex': response.content.hex()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()