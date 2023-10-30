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

def modify_dicom(dicom_dir, headers, config, output):
    # ディレクトリ内のDICOMファイルを取得
    dicom_files = []
    for root, dirs, files in os.walk(dicom_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_dicom_file(file_path):
                dicom_files.append(file_path)
    # print(dicom_files)

    # DICOMファイルからtag情報を読み込む
    for dicom_path in dicom_files:
        dicom_data = pydicom.dcmread(dicom_path)
        header_1 = dicom_data.get(headers[0], f"{headers[0]}not found")
        header_2 = dicom_data.get(headers[1], f"{headers[1]}not found")
        header_3 = dicom_data.get(headers[2], f"{headers[2]}not found")
        header_4 = dicom_data.get(headers[3], f"{headers[3]}not found")
        series = str(dicom_data.get("SeriesNumber", "series_num not found"))
        image = str(dicom_data.get("InstanceNumber", "instance_num not found"))
        print(f"File: {dicom_path}, {headers[0]}: {header_1},  {headers[1]}: {header_2}, {headers[2]}: {header_3}, {headers[3]}: {header_4},")

        # 現在のDICOMのheader情報を取得
        current_tags = []
        for header in headers:
            tag_value = dicom_data.get(header)
            if tag_value:
                current_tags.append(str(tag_value))
            else:
                current_tags.append(f"{header} not found")
        print(f"Original Tags for {file_path}: {current_tags}")

        # config.csvとの比較
        for config_row in config:
            for idx, header in enumerate(headers):
                dicom_data[header].value = config_row[idx]

                # 保存先のディレクトリ設定
                copy_directory = os.path.join(output, config_row[0], series)
                if not os.path.exists(copy_directory):
                    os.makedirs(copy_directory)

                file_name = os.path.join(copy_directory, f'dicom_file_{image}.dcm')
                dicom_data.save_as(file_name)
                print(f"Saved {file_name}")
    else:  # ループが完了しても一致する行がなかった場合の処理
        print("Matching header configuration not found in CSV.")
        return

def read_csv_file(file_path):
    copy_config = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # ヘッダー行をスキップする
        for row in csv_reader:
            # print(row)
            copy_config.append(row)
            pass
        return copy_config

def get_csv_headers(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # ヘッダー行を読み取る
        return headers

def main():
    copy_config = read_csv_file(csv_path)
    # print(copy_config)
    headers = get_csv_headers(csv_path)
    print(headers)
    modify_dicom(
        original_dir,
        headers,
        copy_config,
        copied_dir
    )


if __name__ == "__main__":
    main()