#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from Crypto.PublicKey import RSA
from typing import Optional


class RSATool:
    """ RSA加密解密工具 """
    def __init__(self, public_key_path: Optional[str] = None, private_key_path: Optional[str] = None) -> None:
        if public_key_path:
            try:
                self.public_key = RSA.load_pub_key(public_key_path)
            except Exception as e:
                print(f'load pub key failed, path: [{public_key_path}], exception: [{e}]')
                self.public_key = None
        else:
            self.public_key = None

        if private_key_path:
            try:
                self.private_key = RSA.load_key(private_key_path)
            except Exception as e:
                print(f'load pub key failed, path: [{private_key_path}], exception: [{e}]')
                self.private_key = None
        else:
            self.private_key = None

    def encrypt_data(self, data: str) -> Optional[str]:
        try:
            data_encode = data.encode()
            public_encrypt_data = self.public_key.public_encrypt(data_encode, RSA.pkcs1_padding)
            b64encode_public_encrypt_data = base64.b64encode(public_encrypt_data)
            data_decode = b64encode_public_encrypt_data.decode()
            return data_decode
        except Exception as e:
            print(f'encrypt data failed, data: [{data}], exception: [{e}]')
            return None

    def decrypt_data(self, data: str) -> Optional[str]:
        try:
            data_encode = data.encode()
            b64decode_public_encrypt_data = base64.b64decode(data_encode)
            private_decrypt_data = self.private_key.private_decrypt(b64decode_public_encrypt_data, RSA.pkcs1_padding)
            data_decode = private_decrypt_data.decode()
            return data_decode
        except Exception as e:
            print(f'decrypt data failed, data: [{data}], exception: [{e}]')
            return None
