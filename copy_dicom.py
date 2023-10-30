import os
import pydicom
import json

# config.jsonから設定を読み取る
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
original_dir = config.get('original_dir', '')
csv_dir = config.get('csv_dir', '')
copied_dir = config.get('copied_dir', '')

def is_dicom_file(file_path):
    try:
        dicom = pydicom.dcmread(file_path)
        # DICOMファイルであることが確認された場合
        return True
    except pydicom.errors.InvalidDicomError:
        # DICOMファイルでない場合
        return False

def read_dicom(dicom_dir):
    # ディレクトリ内のDICOMファイルを取得
    dicom_files = []
    for root, dirs, files in os.walk(dicom_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_dicom_file(file_path):
                dicom_files.append(file_path)
    
    print(dicom_files)

def main():
    read_dicom(
        original_dir
    )

if __name__ == "__main__":
    main()