# -*- coding: utf-8 -*-
"""
开发相关常量

本模块定义了开发过程中常用的常量，包括：
- HTTP 内容类型
- 加密算法
- 工作模式
- 填充方式
- 编码方式
"""

# HTTP 内容类型
JSON_CONTENT_TYPE = "application/json"
FILE_CONTENT_TYPE = "application/octet-stream"
FORM_URL_ENCODED_CONTENT_TYPE = "application/x-www-form-urlencoded"
MULTIPART_FORM_DATA_CONTENT_TYPE = "multipart/form-data"

# 加密算法

# 单向加密算法（哈希算法）
MD5 = "MD5"
SHA1 = "SHA1"
SHA256 = "SHA256"
SHA512 = "SHA512"
SM3 = "SM3"

# 对称加密算法
AES = "AES"
SM4 = "SM4"
DES = "DES"
THREE_DES = "3DES"
CHACHA20 = "ChaCha20"
RC4 = "RC4"

# 非对称加密算法
RSA = "RSA"
ECC = "ECC"
DSA = "DSA"
SM2 = "SM2"

# 工作模式常量
MODE_ECB = "ECB"
MODE_CBC = "CBC"
MODE_GCM = "GCM"

# 填充方式常量

# 对称加密中的块加密填充方式
PKCS7_PADDING = "PKCS7"
ISO10126_PADDING = "ISO10126"
NO_PADDING = "NoPadding"
ZERO_PADDING = "ZeroPadding"

# 非对称加密填充方式
PKCS1V15 = "PKCS1v15"
OAEP = "OAEP"

# 编码方式常量
ENCODING_BASE64 = "base64"
ENCODING_HEX = "hex"
