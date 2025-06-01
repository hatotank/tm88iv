# TM88IV

このリポジトリは、もともと [WPT](https://github.com/hatotank/WPT) プロジェクトの一部であった `TM88IV` クラスを含みます。

`TM88IV` クラスは抽出され、単独のリポジトリとして管理・再利用しやすくなりました。

## 特徴
- TM88IV(日本語モデル)プリンタ向けの日本語および絵文字印刷対応
- JIS文字セット（JIS0212, JIS0213）対応
- 上記内容にて外字機能を使用

![印字サンプル](tm88iv_print_sample.jpg)

## 必要なPythonパッケージ

- python-escpos
- Pillow
- emoji

`requirements.txt` を用意しています。以下のコマンドで一括インストールできます。

```
pip install -r requirements.txt
```

## JISデータ・フォントの入手方法

本クラスの利用には、以下のJISデータファイルおよびフォントファイルが必要です。

### JISデータファイル
- JIS0201.TXT: http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0201.TXT
- JIS0208.TXT: http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT
- JIS0212.TXT: http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0212.TXT
- JIS0213-2004.TXT: https://raw.githubusercontent.com/hatotank/WPT/refs/heads/main/JIS0213-2004.TXT

### フォントファイル
- NotoSansJP-Medium.otf: https://github.com/notofonts/noto-cjk/releases
- OpenMoji-black-glyf.ttf: https://github.com/hfg-gmuend/openmoji/releases
- unifont_jp-16.0.03.otf: https://unifoundry.com/unifont/

各ファイルは、`tests/data/` および `tests/fonts/` ディレクトリ等、適切な場所に配置してください。

## サンプルコードについて

本リポジトリの `tests/test_tm88iv.py` には、TM88IVクラスの主要機能を網羅したテストコードが含まれています。
サンプルコードとしても利用可能ですので、実際の動作確認や使い方の参考にしてください。

また、テストコードにはJISデータファイルやフォントファイルを自動でダウンロード・展開する機能も含まれています。
初回実行時に必要なファイルが自動的に準備されるため、セットアップの手間を大幅に省略できます。

## ライセンス
本プロジェクトは、元の [WPT](https://github.com/hatotank/WPT) プロジェクトのライセンスを継承しています。
