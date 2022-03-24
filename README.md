## netdev-unittestについて

### 概要
- netdev-unittestは、シリアルコンソール接続したネットワーク機器に対する単体試験を実施するPythonツールです。

### 仕組み
- シリアルコンソール接続したネットワーク機器に対する単体試験を実施するためには、以下の三点が必要です。
    1. ログから必要な情報取得するための**テンプレートファイル**
    2. 接続する機器の情報を取得した**インベントリファイル**
    3. 実行する単体試験の内容を記述した**コマンドファイル**
- インベントリファイルを用いてシリアルコンソール接続を用いて機器に接続し、コマンドファイルに基づいて単体試験を実行後、
テンプレートファイルを用いて状態判定を行う事で単体試験を実施します。


## netdev-unittestのインストール方法
### Pythonインタープリタで実行する場合
1. ```git clone```により、本リポジトリをコピーする。
```
C:\>git clone https://github.com/TomoyaKamei/netdev-unittest.git
```
2. ```python -m venv (仮想環境名)```により、pythonの仮想環境を作成する。
```
C:\>cd netdev-unittest
C:\netdev-unittest>python -m venv venv
```
3. 仮想環境を起動する。
```
C:\netdev-unittest>./venv/Script/activate
(venv)C:\netdev-unittest>
```

4. ```pip install -r requirements.txt```により、pythonの仮想環境に必要なパッケージをインストールする。
```
(venv)C:\netdev-unittest>pip install -r requirements.txt
```

### .exeファイル形式で実行する場合
- ※前節のPythonインタープリタで実行する方法を事前に実行して下さい。
1. pyinstallerを使用して.exeファイル化する。作成されたファイルは、/dist配下に存在する。
```
(venv)C:\netdev-unittest>make build
```
2. 必要な場合、環境変数を通す。
```
(venv)C:\netdev-unittest>SET PATH=%PATH%;C:\netdev-unittest\dist
```

## netdev-unittestの使用方法

### パラメータシートからコンフィグの作成
- 以下の書式で実行する。
    - ```-cf, --command_file```は、コマンドファイルが存在するパスを指定する。
    - ```-i, --inventory_file```は、インベントリファイルが存在するパスを指定する。
    - ```-op, --output```は、出力するコンフィグを格納するパスを指定する。
- Pythonでの実行例
    ```
    (venv)C:\netdev-unittest>python netdev-unittest.py unittest -cf ./data/input/command/command_file.log -i ./data/input/inventory/inventory_file.ini -op ./data/output/result
    ```
- exeファイルでの実行例
    ```
    (venv)C:\netdev-unittest\dist>netdev-unittest unittest -cf ./data/input/command/command_file.log -i ./data/input/inventory/inventory_file.ini -op ./data/output/result
    ```

### コンフィグからパラメーターシートの更新
- ※未実装


## netdev-unittestの簡易リファレンス

### Commandsファイル
#### 概要
- Ruleファイルは、主にパラメータシートのどこからパラメータを取得するのかを記述したファイルになります。
#### パラメータ解説
- unittest
    - (Required)単体試験の内容を記述したセクションです。
        - procedures
            - (Required)単体試験の手順を記述したセクションです。
                - description
                    - (Required)単体試験の概要を記述する場所です。
                - operation
                    - (Required)単体試験の試験内容を記述場所です。
                    - 現在設定可能な値は、```"CheckStatus", "InterfaceCheck", "ConfigDiff"```のみです。
                - operation_number
                    - (Required)単体試験の手順番号を記述する場所です。
                - expectation_key
                    - (Required)状態を比較するキーを記述する場所です。
                    - Expectationセクションと同一の```expectation_key```を記述して下さい。
                - command
                    - (Required)実行するコマンドを記述する場所です。
- expectation
    - (Required)期待値の状態を記述するセクションです。

#### 記述例
```yml
unittest:
    procedures:
        - description: "状態比較"
          operation: "CheckStatus"
          operation_number: "1-1"
          expectation_key: "expc_display_device_manuinfo"
          command: "display device manuinfo"
expectation:
    expc_display_device_manuinfo:
        - DEVICE_NAME: QX-S3828TP
          DEVICE_SERIAL_NUMBER: 210234A0UY920AQ0001B
          MAC_ADDRESS: 3CD2-E5D8-9C27
          MANUFACTURING_DATE: "2020-10-16"
          SLOT_NUMBER: '1'
          VENDOR_NAME: "NEC"
```


### Templateファイル

#### 概要
- Templateファイルは、構造化されたファイルから一定の情報を取得するために必要なファイルです。
- 詳細に関しては、[networktocode/ntc-templates](https://github.com/networktocode/ntc-templates)等を参照して下さい。

#### 記述例
```log
Value Interface_Name ([\w/]+)
Value Transceiver_Type ([\w_]+)
Value Connector_Type (\w+)
Value Wavelength (\d+)
Value Transfer_Distance (\w+)
Value Digital_Diagnostic_Monitoring (\w+)
Value Vendor_Name (\w+)
Value Serial_Number (\w+)

Start
  ^${Interface_Name}\s*transceiver\s*information:
  ^  Transceiver Type              : ${Transceiver_Type}
  ^  Connector Type                : ${Connector_Type}
  ^  Wavelength(nm)                : ${Wavelength}
  ^  Transfer Distance(km)         : ${Transfer_Distance}
  ^  Digital Diagnostic Monitoring : ${Digital_Diagnostic_Monitoring}
  ^  Vendor Name                   : ${Vendor_Name}
  ^  Serial Number                 : ${Serial_Number} -> Record
```


### Inventoryファイル

#### 概要
- Inventoryファイルは、接続する機器の情報を記述するためのファイルである。

#### パラメータ解説
- [デバイス名]
    - (Required)デバイス名を記述して下さい。
        - ip_address
            - (Required)デバイスのIPアドレスを記述する箇所です。
        - manufacturer_name
            - (Required)デバイスの製造会社を記述する箇所です。
        - device_name
            - (Required)デバイス機種を記述する箇所です。
        - version
            - (Required)デバイスのバージョンを記述する箇所です。
        - port_name
            - (Required)接続するコンソールを記述する箇所です。
        - baudrate
            - (Optional)接続するコンソールの速度を記述する箇所です。
        - login_id
             - (Required)デバイスのログインIDを記述する箇所です。
        - login_password
            - (Required)デバイスのパスワードを記述する箇所です。
        - admin_password
            - (Required)デバイスのAdminパスワードを記述する箇所です。

#### 記述例
```log
[TEST-DEVICE]
ip_address=192.168.0.1
manufacturer_name=NEC
device_name=QX-S3828TP
version=1.0.0
port_name=tty0
baudrate=10000
login_id=operator
login_password=password
admin_password=admin_password

``` 

## その他
### 今後の追加機能
- v1.1.1
    - pydanticの導入
### バグなど発見した場合
