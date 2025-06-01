import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

import pytest

# テストモジュールのパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tm88iv import TM88IV

def download(url: str, dest: Path):
    """
    指定されたURLからファイルをダウンロードし、指定されたパスに保存します。
    既にファイルが存在する場合はスキップします。
    :param url: ダウンロードするファイルのURL
    :param dest: 保存先のパス
    """
    if dest.exists():
        print(f"[SKIP] {dest.name} は既に存在します")
        return
    print(f"[GET] {dest.name} をダウンロード中...")
    urllib.request.urlretrieve(url, dest)


@pytest.fixture(scope="session", autouse=True)
def prepare_fonts_and_data_downlowd():
    """
    フォントとJISデータの準備を行います。
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    BASE_DIR = BASE_DIR / "tests"
    FONTS_DIR = BASE_DIR / "fonts"
    DATA_DIR = BASE_DIR / "data"
    TEMP_ZIP1 = FONTS_DIR / "_tmp_NotoSansJP.zip"
    TEMP_ZIP2 = FONTS_DIR / "_tmp_OpenMoji.zip"

    # フォルダが存在しない場合は作成
    FONTS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    print("\n=== フォントとJISデータを準備中 ===")
    # --- フォント ---
    # NotoSansJP (zip 展開)
    # https://github.com/notofonts/noto-cjk
    if not (FONTS_DIR / "NotoSansJP-Medium.otf").exists():
        download("https://github.com/notofonts/noto-cjk/releases/download/Sans2.004/16_NotoSansJP.zip", TEMP_ZIP1)
        with zipfile.ZipFile(TEMP_ZIP1, 'r') as zp:
            for name in zp.namelist():
                if name.endswith("NotoSansJP-Medium.otf"):
                    print("[UNZIP] NotoSansJP-Medium.otf を抽出")
                    zp.extract(name, FONTS_DIR)
                    (FONTS_DIR / name).rename(FONTS_DIR / "NotoSansJP-Medium.otf")
        TEMP_ZIP1.unlink(missing_ok=True)
    else:
        print("[SKIP] NotoSansJP-Medium.otf は既に存在します")

    # OpenMoji (zip 展開)
    # https://github.com/hfg-gmuend/openmoji
    if not (FONTS_DIR / "OpenMoji-black-glyf.ttf").exists():
        download("https://github.com/hfg-gmuend/openmoji/releases/download/15.1.0/openmoji-font.zip", TEMP_ZIP2)
        with zipfile.ZipFile(TEMP_ZIP2, 'r') as zp:
            for name in zp.namelist():
                if name.endswith("OpenMoji-black-glyf.ttf"):
                    print("[UNZIP] OpenMoji-black-glyf.ttf を抽出")
                    zp.extract(name, FONTS_DIR)
                    (FONTS_DIR / name).rename(FONTS_DIR / "OpenMoji-black-glyf.ttf")
                    subdir = FONTS_DIR / Path(name).parent
                    if subdir.exists() and subdir.is_dir():
                        shutil.rmtree(subdir)
        TEMP_ZIP2.unlink(missing_ok=True)
    else:
        print("[SKIP] OpenMoji-black-glyf.ttf は既に存在します")

    # Unifont (JP)
    # https://unifoundry.com/unifont/
    download(
        "https://unifoundry.com/pub/unifont/unifont-16.0.03/font-builds/unifont_jp-16.0.03.otf",
        FONTS_DIR / "unifont_jp-16.0.03.otf"
    )

    # --- JISデータ ---
    # https://www.unicode.org/ + https://github.com/hatotank/WPT
    jis_files = {
        "JIS0201.TXT": "http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0201.TXT",
        "JIS0208.TXT": "http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT",
        "JIS0212.TXT": "http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0212.TXT",
        "JIS0213-2004.TXT": "https://raw.githubusercontent.com/hatotank/WPT/refs/heads/main/JIS0213-2004.TXT",
    }

    for filename, url in jis_files.items():
        download(url, DATA_DIR / filename)

    print("[完了] すべてのファイルが準備されました。")


@pytest.mark.parametrize("ip_address", ["192.168.10.21"])
@pytest.mark.parametrize("emoji_font_type", ["font3"]) # font1 / font2 / font3
def test_print1(ip_address, emoji_font_type):
    """
    このテストは実際の印刷物を目視で確認してください。
    このテストでは、JIS0201、JIS0208、JIS0212、JIS0213-2004、絵文字、外字登録などの機能を確認します。
    """
    # Windows の絵文字フォントを使用する場合は、以下のように設定してください。
    if emoji_font_type == "font1":
        # Windows の絵文字フォント
        config = {
            "emoji_font_file": "C:/Windows/Fonts/SEGUIEMJ.TTF",  # Windows の絵文字フォント
            "emoji_font_size": 20,  # 絵文字フォントのサイズ
            "emoji_font_adjust_x": 0,  # 絵文字フォントのX軸調整
            "emoji_font_adjust_y": 4,  # 絵文字フォントのY軸調整
        }
    elif emoji_font_type == "font2":
        # NotoEmoji フォントを使用する場合
        config = {
            "emoji_font_file": "tests/fonts/NotoEmoji-Medium.ttf",  # NotoEmoji フォント
            "emoji_font_size": 20,  # 絵文字フォントのサイズ
            "emoji_font_adjust_x": 0,  # 絵文字フォントのX軸調整
            "emoji_font_adjust_y": 0,  # 絵文字フォントのY軸調整
        }
    elif emoji_font_type == "font3":
        # OpenMoji フォントを使用する場合
        config = {
            "emoji_font_file": "tests/fonts/OpenMoji-black-glyf.ttf",  # OpenMoji フォント
            "emoji_font_size": 20,  # 絵文字フォントのサイズ
            "emoji_font_adjust_x": 0,  # 絵文字フォントのX軸調整
            "emoji_font_adjust_y": 0,  # 絵文字フォントのY軸調整
        }
    config["jis0201_file"] = "tests/data/JIS0201.TXT"  # JIS0201 データファイル
    config["jis0208_file"] = "tests/data/JIS0208.TXT"  # JIS0208 データファイル
    config["jis0212_file"] = "tests/data/JIS0212.TXT"  # JIS0212 データファイル
    config["jis0213_file"] = "tests/data/JIS0213-2004.TXT"  # JIS0213-2004 データファイル
    config["kanji_font_file"] = "tests/fonts/NotoSansJP-Medium.otf"  # NotoSansJP フォント
    config["fallback_font_file"] = "tests/fonts/unifont_jp-16.0.03.otf"  # Unifont JP フォント

    # TM88IV インスタンスを作成
    p = TM88IV(ip_address,config=config)
    p.open()
    p.jptext2("=== 印刷テスト開始 ===\n")
    p.jptext2("abcABCあ*アｱ\\~|①②㍑〶㌧㌦\n")
    p.jptext2("絵文字 ：🅱♨🆖👍🐕🛰\n")
    p.jptext2("JIS0208：亜腕亞熙\n")
    p.jptext2("JIS0212：丂侄黸龥\n")
    p.jptext2("JIS0213-2004：俱剝瘦繫\n")
    p.jptext2("外字登録😁なので文字の途中👍👍で使えます🛰\n")
    p.jptext2("繁体字：鑑於對人類家庭所有成員的固有尊嚴及其平等的和不移的權利的承認，乃是世界自由、正義與和平的基礎\n")
    p.jptext2("簡体字：鉴于对人类家庭所有成员的固有尊严及其平等的和不移的权利的承认,乃是世界自由、正义与和平的基础\n")
    p.jptext2("ハングル：모든 인류 구성원의 천부의 존엄성과 동등하고 양도할 수 없는 권리를 인정하는\n")
    p.jptext2("ベンガル：যেহেতু মানব পরিবারের সকল সদস্যের সমান ও অবিচ্ছেদ্য অধিকারসমূহ\n")
    p.jptext2("=== 印刷テスト終了 ===\n")
    p.cut()
    p.close()


@pytest.mark.parametrize("ip_address", ["192.168.10.21"])
def test_print2(ip_address):
    """
    このテストは実際の印刷物を目視で確認してください。
    このテストでは、文字の拡大、アンダーライン、白黒反転印字などの機能を確認します。
    """
    config = {
        "jis0201_file": "tests/data/JIS0201.TXT",  # JIS0201 データファイル
        "jis0208_file": "tests/data/JIS0208.TXT",  # JIS0208 データファイル
        "jis0212_file": "tests/data/JIS0212.TXT",  # JIS0212 データファイル
        "jis0213_file": "tests/data/JIS0213-2004.TXT",  # JIS0213-2004 データファイル
        "emoji_font_file": "tests/fonts/OpenMoji-black-glyf.ttf",  # OpenMoji フォント
        "kanji_font_file": "tests/fonts/NotoSansJP-Medium.otf",  # NotoSansJP フォント
        "fallback_font_file": "tests/fonts/unifont_jp-16.0.03.otf"  # Unifont JP フォント
    }

    # TM88IV インスタンスを作成
    p = TM88IV(ip_address, config=config)
    p.open()
    p.jptext2("=== 印刷テスト２開始 ===\n")
    p.jptext2("横倍拡大👍亜丂俱যে\n",dw=True)
    p.jptext2("縦倍拡大👍亜丂俱যে\n",dh=True)
    p.jptext2("横倍拡大＋縦倍拡大\n",dw=True,dh=True)
    p.jptext2("ABCあア👍亜丂俱যে\n",dw=True,dh=True)
    p.jptext2("ABCあア👍亜丂俱যে\n",dw=True,dh=True,bflg=True)
    p.jptext2("アンダーライン👍亜丂俱যে\n",underline=True)
    p.jptext2("白黒反転印字👍亜丂俱যে\n",wbreverse=True)
    p.jptext2("ABC👍亜丂俱যে\n",dw=True,dh=True,underline=True,bflg=True)
    p.jptext2("\n")
    p.jptext2("ABC👍亜丂俱যে\n",dw=True,dh=True,wbreverse=True,bflg=True)
    p.jptext2("=== 印刷テスト2終了 ===\n")
    p.cut()
    p.close()


@pytest.mark.parametrize("ip_address", ["192.168.10.21"])
@pytest.mark.parametrize("missing_key", [
    "jis0201_file",
    "jis0208_file",
    "jis0212_file",
    "jis0213_file",
    "emoji_font_file",
    "kanji_font_file",
    "fallback_font_file",
])
def test_print_file_not_found_for_each_equired_file(ip_address,missing_key):
    """
    このテストはファイルが見つからない場合のエラーハンドリングを確認します。
    """
    config = {
        "jis0201_file": "JIS0201.TXT",
        "jis0208_file": "JIS0208.TXT",
        "jis0212_file": "JIS0212.TXT",
        "jis0213_file": "JIS0213-2004.TXT",
        "emoji_font_file": "OpenMoji-black-glyf.ttf",
        "kanji_font_file": "NotoSansJP-Medium.otf",
        "fallback_font_file": "unifont_jp-16.0.03.otf"
    }
    config[missing_key] = "not_exist_" + config[missing_key]
    with pytest.raises(FileNotFoundError):
        TM88IV(ip_address, config=config)
