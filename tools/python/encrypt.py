import requests
from cryptography.fernet import Fernet
import base64

# 生成对称加密密钥
key = Fernet.generate_key()
cipher_suite = Fernet(key)

print('生成对称加密密钥：', key)

# b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01' 是字节串
# 字节串和普通字符串（Unicode字符串）是不同的数据类型。字节串中的每个元素都是一个字节（整数），而字符串中的每个元素都是一个字符（字符串）

# Base64编码后的数据是可打印的ASCII字符串，便于通过HTTP传输或存储在文本格式的文件中
fingerprint_data = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01')
print('等待加密的字节码是：', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01')
print('转化成字符串是：', fingerprint_data) #字符串
# 加密指纹数据
encrypted_data = cipher_suite.encrypt(fingerprint_data)
print('加密字符串是：',encrypted_data)

decrypted_data = cipher_suite.decrypt(encrypted_data)
print('解密字符串是：',decrypted_data)
# 解码指纹数据
fingerprint_data = base64.b64decode(decrypted_data)
print('解密字节码是：', fingerprint_data)