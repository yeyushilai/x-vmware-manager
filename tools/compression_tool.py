#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import py7zr


class ZipExtractor:
    @classmethod
    def extract_zip(cls, zip_file_path, extract_folder):
        # 创建解压目录
        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)

        # 打开 ZIP 文件
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # 解压所有文件到指定目录
            zip_ref.extractall(extract_folder)


class SevenZipExtractor:

    filters = [
        {
            'id': py7zr.FILTER_LZMA2,
            'options': {'dict_size': 65536, 'lc': 3, 'lp': 0, 'pb': 2}
        },
    ]

    def __init__(self, archive_path, password=None):
        self.archive_path = archive_path
        self.password = password

    def extract_all(self, output_path=".", create_subfolder=True):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        with py7zr.SevenZipFile(self.archive_path, mode='r', password=self.password, filters=self.filters) as archive:
            if create_subfolder:
                base_name = archive.getnames()[0].split("/")[0]
                output_path = f"{output_path}/{base_name}"

            archive.extractall(output_path)
            return output_path



if __name__ == "__main__":
    # 创建SevenZipExtractor实例，传入7z文件的路径和解压密码（如果有的话）
    extractor = SevenZipExtractor("your_archive.7z", password="your_password")

    # 指定解压缩的目标路径，默认为当前工作目录
    output_directory = "output_folder"

    # 调用extract_all方法进行解压缩，并指定是否创建子文件夹
    extractor.extract_all(output_directory, create_subfolder=True)
