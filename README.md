# DICOM画像複製ソフト

## Description

デモにDICOM画像を用いる際に同一の画像を複製する必要がある。
その際に以下のDICOM tagを変更する必要がある
- StudyInstanceUID
- PatientID
- PatientName
- AccessionNumber
等

DICOM編集ツールで手作業で修正も可能だがめんどうなので自動化するツールを作成する

## Specification

- config.jsonで各フォルダの格納先を設定する
- originalフォルダ内に複製したいDICOMファイルを置く
    - ただしDICOMファイルは一意のStudyInstanceUIDとする
    - 複数のStudyInstanceUIDを持つファイルは置けない
        - 正確には置けるが、すべて上書きしてしまうので意味がない
- csvフォルダ内のcopy_config.csvに変更後の値を記載する
    - csvファイルのヘッダーには変更したいDICOM_tagの名前を記載する
        - tagの番号ではなく『名称』なことに注意
    - 任意のDICOM_tagの書き換えが可能
    - ただし指定できるDICOM_tagは４つまで
- copy_dicom.exeを実行
- copiedフォルダ内に複製されたDICOMファイルが生成される

## Environment

### Module

- pip           23.3.1
- pydicom       2.4.3
- pyinstaller   6.1.0
