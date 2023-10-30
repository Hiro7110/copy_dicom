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

- originalフォルダ内に複製したいDICOMファイルを置く
    - ただしDICOMファイルは一意のStudyInstanceUIDとする
    - （複数のStudyInstanceUIDを持つファイルは置けない）
- csvフォルダ内に変更内容を記載したcsvを置く
    - csvファイルのヘッダーには変更したいDICOM_tagの名前またはtag_numberを記載する
    - 任意のDICOM_tagの書き換えが可能
    - ただし指定でいるDICOM_tagは４つまで
- copy_dicom.exeを実行
- copiedフォルダ内に複製されたDICOMファイルが生成される

## Environment

### Module

- pip           23.3.1
- pydicom       2.4.3
- pyinstaller   6.1.0
