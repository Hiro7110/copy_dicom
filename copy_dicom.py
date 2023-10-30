import os
import pydicom
import json
import csv

# config.jsonから設定を読み取る
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
original_dir = config.get('original_dir', '')
csv_dir = config.get('csv_dir', '')
copied_dir = config.get('copied_dir', '')

# csv_dirを基にconfig.csvのフルパスを作成
csv_path = os.path.join(csv_dir, 'copy_config.csv')

def is_dicom_file(file_path):
    try:
        dicom = pydicom.dcmread(file_path)
        # DICOMファイルであることが確認された場合
        return True
    except pydicom.errors.InvalidDicomError:
        # DICOMファイルでない場合
        return False

def read_dicom(dicom_dir, header):
    # ディレクトリ内のDICOMファイルを取得
    dicom_files = []
    for root, dirs, files in os.walk(dicom_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_dicom_file(file_path):
                dicom_files.append(file_path)
    # print(dicom_files)

        # 各DICOMファイルからStudyInstanceUIDを読み込む
    for dicom_path in dicom_files:
        dicom_data = pydicom.dcmread(dicom_path)
        header_1 = dicom_data.get(header[0], "UID not found")
        header_2 = dicom_data.get(header[1], "UID not found")
        header_3 = dicom_data.get(header[2], "UID not found")
        header_4 = dicom_data.get(header[3], "UID not found")
        print(f"File: {dicom_path}, {header[0]}: {header_1},  {header[1]}: {header_2}, {header[2]}: {header_3}, {header[3]}: {header_4},")

def read_csv_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # print(row)
            pass

def get_csv_headers(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # ヘッダー行を読み取る
        return headers
    
def main():
    read_csv_file(csv_path)
    headers = get_csv_headers(csv_path)
    print(headers)
    read_dicom(
        original_dir,
        headers
    )


if __name__ == "__main__":
    main()