""" Japanese + Emoji support for TM88IV(Japanese model)

Need fonts and something...

References
----------
python-escpos - Python library to manipulate ESC/POS Printers
    https://github.com/python-escpos/python-escpos
python-escpos for Japanese
    https://github.com/lrks/python-escpos
python-escpos japenese wrapper
    https://github.com/iakyi/python-escpos-jp
"""
from escpos.printer import Network
from escpos.constants import *
from PIL import Image, ImageDraw, ImageFont
import collections
import emoji
import os

class TM88IV(Network):
    """ TM88IV

    Inherits from python-escpos Network class.
    """

    USER_AREAS_ASCII = [
        b'\x20',b'\x21',b'\x22',b'\x23',b'\x24',b'\x25',b'\x26',b'\x27',b'\x28',b'\x29',b'\x2a',b'\x2b',b'\x2c',b'\x2d',b'\x2e',b'\x2f',
        b'\x30',b'\x31',b'\x32',b'\x33',b'\x34',b'\x35',b'\x36',b'\x37',b'\x38',b'\x39',b'\x3a',b'\x3b',b'\x3c',b'\x3d',b'\x3e',b'\x3f',
        b'\x40',b'\x41',b'\x42',b'\x43',b'\x44',b'\x45',b'\x46',b'\x47',b'\x48',b'\x49',b'\x4a',b'\x4b',b'\x4c',b'\x4d',b'\x4e',b'\x4f',
        b'\x50',b'\x51',b'\x52',b'\x53',b'\x54',b'\x55',b'\x56',b'\x57',b'\x58',b'\x59',b'\x5a',b'\x5b',b'\x5c',b'\x5d',b'\x5e',b'\x5f',
        b'\x60',b'\x61',b'\x62',b'\x63',b'\x64',b'\x65',b'\x66',b'\x67',b'\x68',b'\x69',b'\x6a',b'\x6b',b'\x6c',b'\x6d',b'\x6e',b'\x6f',
        b'\x70',b'\x71',b'\x72',b'\x73',b'\x74',b'\x75',b'\x76',b'\x77',b'\x78',b'\x79',b'\x7a',b'\x7b',b'\x7c',b'\x7d',b'\x7e',
    ]

    USER_KANJI_AREAS_SJIS = [
        b'\x40',b'\x41',b'\x42',b'\x43',b'\x44',b'\x45',b'\x46',b'\x47',b'\x48',b'\x49',b'\x4a',b'\x4b',b'\x4c',b'\x4d',b'\x4e',b'\x4f',
        b'\x50',b'\x51',b'\x52',b'\x53',b'\x54',b'\x55',b'\x56',b'\x57',b'\x58',b'\x59',b'\x5a',b'\x5b',b'\x5c',b'\x5d',b'\x5e',b'\x5f',
        b'\x60',b'\x61',b'\x62',b'\x63',b'\x64',b'\x65',b'\x66',b'\x67',b'\x68',b'\x69',b'\x6a',b'\x6b',b'\x6c',b'\x6d',b'\x6e',b'\x6f',
        b'\x70',b'\x71',b'\x72',b'\x73',b'\x74',b'\x75',b'\x76',b'\x77',b'\x78',b'\x79',b'\x7a',b'\x7b',b'\x7c',b'\x7d',b'\x7e',
        b'\x80',b'\x81',b'\x82',b'\x83',b'\x84',b'\x85',b'\x86',b'\x87',b'\x88',b'\x89',b'\x8a',b'\x8b',b'\x8c',b'\x8d',b'\x8e',b'\x8f',
        b'\x90',b'\x91',b'\x92',b'\x93',b'\x94',b'\x95',b'\x96',b'\x97',b'\x98',b'\x99',b'\x9a',b'\x9b',b'\x9c',b'\x9d',b'\x9e',
    ]

    def __init__(self, host, port=9100, timeout=60, config=None, *args, **kwargs):
        """

        Parameters
        ----------
        host : str
            Printer's hostname or IP address
        port : int
            Port to write to
        timeout : int
            timeout in seconds for the socket-library
        config : dict
            Configuration dictionary for paths and font settings
            - jis0201_file: Path to JIS0201 character set file
            - jis0208_file: Path to JIS0208 character set file
            - jis0212_file: Path to JIS0212 character set file
            - jis0213_file: Path to JIS0213-2004 character set file
            - emoji_font_file: Path to emoji font file
            - emoji_font_size: Size of the emoji font
            - emoji_font_adjust_x: X-axis adjustment for emoji font rendering
            - emoji_font_adjust_y: Y-axis adjustment for emoji font rendering
            - kanji_font_file: Path to kanji font file
            - kanji_font_size: Size of the kanji font
            - kanji_font_adjust_x: X-axis adjustment for kanji font rendering
            - kanji_font_adjust_y: Y-axis adjustment for kanji font rendering
            - fallback_font_file: Path to fallback font file
            - fallback_font_size: Size of the fallback font
            - fallback_font_adjust_x: X-axis adjustment for fallback font rendering
            - fallback_font_adjust_y: Y-axis adjustment for fallback font rendering
        """
        config = config or {}
        # Default configuration values
        # http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0201.TXT
        self.jis0201_file = config.get('jis0201_file', "JIS0201.TXT")
        # http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT
        self.jis0208_file = config.get('jis0208_file', "JIS0208.TXT")
        # http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0212.TXT
        self.jis0212_file = config.get('jis0212_file', "JIS0212.TXT")
        # https://raw.githubusercontent.com/hatotank/WPT/refs/heads/main/JIS0213-2004.TXT
        self.jis0213_file = config.get('jis0213_file', "JIS0213-2004.TXT")
        # Recommended emoji font1: Segoe UI Emoji font (emoji_font_adjust_y: 4) *Windows only
        # https://docs.microsoft.com/en-us/typography/font-list/segoe-ui-emoji
        # Recommended emoji font2: Noto Emoji font
        # https://fonts.google.com/noto/specimen/Noto+Emoji *Manual download required
        # Recommended emoji font3: OpenMoji font
        # https://openmoji.org/
        # https://github.com/hfg-gmuend/openmoji/releases/download/15.1.0/openmoji-font.zip
        self.emoji_font_file = config.get('emoji_font_file', "OpenMoji-black-glyf.ttf")
        self.emoji_font_size = config.get('emoji_font_size', 20)
        self.emoji_font_adjust_x = config.get('emoji_font_adjust_x', 0)
        self.emoji_font_adjust_y = config.get('emoji_font_adjust_y', 0)
        # Recommended kanji font for Japanese characters: Noto CJK fonts
        # https://github.com/notofonts/noto-cjk
        # https://github.com/notofonts/noto-cjk/releases/download/Sans2.004/16_NotoSansJP.zip
        self.kanji_font_file = config.get('kanji_font_file', "NotoSansJP-Medium.otf")
        self.kanji_font_size = config.get('kanji_font_size', 24)
        self.kanji_font_adjust_x = config.get('kanji_font_adjust_x', 0)
        self.kanji_font_adjust_y = config.get('kanji_font_adjust_y', -8)
        # Fallback font for characters not covered by the above fonts
        # Recommended fallback font: Unifont
        # https://unifoundry.com/pub/unifont/unifont-16.0.03/font-builds/unifont_jp-16.0.03.otf
        self.fallback_font_file = config.get('fallback_font_file', "unifont_jp-16.0.03.otf")
        self.fallback_font_size = config.get('fallback_font_size', 24)
        self.fallback_font_adjust_x = config.get('fallback_font_adjust_x', 2)
        self.fallback_font_adjust_y = config.get('fallback_font_adjust_y', 0)

        # Check if required files exist
        required_files = [
            self.jis0201_file,
            self.jis0208_file,
            self.jis0212_file,
            self.jis0213_file,
            self.emoji_font_file,
            self.kanji_font_file,
            self.fallback_font_file
        ]
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file not found: {file}")

        super().__init__(host, port, timeout, *args, **kwargs)

        self.user_areas  = collections.OrderedDict()
        self.gaiji_areas = collections.OrderedDict()

        for area in self.USER_AREAS_ASCII:
            self.user_areas[area] = ''

        for area in self.USER_KANJI_AREAS_SJIS:
            self.gaiji_areas[area] = ''
        
        self._font_cache = {}
        self.c1 = b'\xec' # 外字の文字コードの第1バイト(Shift JIS)

        self._raw(ESC + b't' + b'\x01') # ESC t 文字コードテーブルの選択(Page1 カタカナ)
        self._raw(FS + b'&')            # FS & 漢字モード指定
        self._raw(FS + b'C' + b'\x01')  # FS C 漢字コード体系の選択(Shitf JIS)

        self._load_jis_character_set()


    # https://github.com/nakamura001/JIS_CharacterSet ※チルダがオーバーラインになっている
    def _load_jis_character_set(self):
        """ JIS漢字コードをロード """
        self.jis_x_0201 = []
        self.jis_x_0208 = []
        self.jis_x_0212 = []
        self.jis_x_0213 = []
    
        # JIS X 0201
        with open(self.jis0201_file,"r") as f:
          for row in f:
            if row[0] != '#':
              c = row.split("\t")[1]
              self.jis_x_0201.append(chr(int(c, 16)))

        # JIS X 0208
        with open(self.jis0208_file,"r") as f:
          for row in f:
            if row[0] != '#':
              c = row.split("\t")[2]
              self.jis_x_0208.append(chr(int(c, 16)))

        # JIS X 0212
        with open(self.jis0212_file,"r") as f:
          for row in f:
            if row[0] != '#':
              c = row.split("\t")[1]
              self.jis_x_0212.append(chr(int(c, 16)))

        # JIS X 0213-2004
        with open(self.jis0213_file,"r") as f:
          for row in f:
            if row[0] != '#':
              c = row.split("\t")[1]
              self.jis_x_0213.append(chr(int(c, 16)))


    def _get_font(self, font_path, size, encoding='unic'):
        """ フォントオブジェクトをキャッシュから取得、または新規作成して返却
        
        パラメータ
        ----------
        font_path : str
            フォントファイルのパス
        size : int
            フォントサイズ
        encoding : str
            フォントのエンコーディング（デフォルトは'unic'）
        戻り値
        -------
        font : ImageFont
            フォントオブジェクト
        """
        key = (font_path, size, encoding)
        if key not in self._font_cache:
            self._font_cache[key] = ImageFont.truetype(font_path, size, encoding=encoding)
        return self._font_cache[key]


    def _escpos_register_gaiji(self, c2, gaiji, font, size, adjustX, adjustY, asciiflg):
        """ 外字登録(ESC/POS)

        Parameters
        ----------
        c2 : byte
            外字の文字コードの第2バイト
        gaiji : str
            外字
        font : str
            外字フォント
        size : int
            フォントサイズ
        adjustX : int
            フォント描画位置調節x軸(ピクセル)
        adjustY : int
            フォント描画位置調節x軸(ピクセル)
        asciiflg : int
            ダウンロード文字定義フラグ
        """
        if asciiflg:
            img = Image.new('RGB', (12,24), (255,255,255))
        else:
            img = Image.new('RGB', (24,24), (255,255,255))
        draw = ImageDraw.Draw(img)
        f = self._get_font(font, size, encoding='unic')
        draw.text((adjustX,adjustY), gaiji, fill=(0,0,0), font=f)
        img = img.convert('1')

        byte_array = []
        bit_str = ''
        for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x,y))
                if pixel == 255:
                    bit_str += '0'
                else:
                    bit_str += '1'

                if not (y + 1) % 8:
                    byte_array.append(int(bit_str, 2).to_bytes(1, 'big'))
                    bit_str = ''

        if asciiflg:
            self._raw(ESC + b'&' + b'\x03' + c2 + c2) # ESC & ダウンロード文字の定義
            self._raw(b'\x0c')
        else:
            self._raw(FS + b'2' + self.c1 + c2) # FS 2 外字の定義

        for byte in byte_array:
            self._raw(byte)


    def _define_gaiji(self, gaiji, font, size=18, adjustX=0, adjustY=0, asciiflg=False):
        """ 外字登録

        Parameters
        ----------
        gaiji : str
            外字文字
        font : str
            外字フォント
        size : int
            フォントサイズ
        adjustX : int
            フォント描画位置調節x軸(ピクセル)
        adjustY : int
            フォント描画位置調節y軸(ピクセル)
        asciiflg : bool
            ダウンロード文字定義フラグ
        Returns
        -------
        out : byte
            外字文字
        """
        # ダウンロード文字
        if asciiflg:
            for k, v in self.user_areas.items():
                if v == gaiji:
                    self.user_areas[k] = self.user_areas.pop(k) # 削除して追加
                    return ESC + b'%' +' \x01' + k + ESC + b'%' + b'\x00' # ダウンロード文字セットの指定・解除

            for k, v in self.user_areas.items():
                self.user_areas.pop(k)
                self.user_areas[k] = gaiji

                self._escpos_register_gaiji(k,gaiji,font,size,adjustX,adjustY,asciiflg) # 定義または再定義
                return ESC + b'%' + b'\x01' + k + ESC + b'%' + b'\x00'    # ダウンロード文字セットの指定・解除

        # 外字
        else:
            for k, v in self.gaiji_areas.items():
                if v == gaiji:
                    self.gaiji_areas[k] = self.gaiji_areas.pop(k) # 削除して追加
                    return self.c1 + k

            for k, v in self.gaiji_areas.items():
                self.gaiji_areas.pop(k)
                self.gaiji_areas[k] = gaiji

                self._escpos_register_gaiji(k,gaiji,font,size,adjustX,adjustY,asciiflg) # 定義または再定義
                return self.c1 + k

        return b''


    def jptext2(self, text, dw=False, dh=False, underline=False, wbreverse=False, bflg=False):
        """ 絵文字対応日本語出力

        Parameters
        ----------
        text : str
            テキスト
        dw : bool
            横倍拡大
        dh : bool
            縦倍拡大
        underline : bool
            アンダーライン(1ドット幅)
        wbreverse : bool
            白黒反転印字
        bflg : bool
            1バイトコード文字にも適用(横倍拡大、縦倍拡大)
        """
        n = 0x00
        b = 0x00
        if dw:
            n += 0x04 # 横倍拡大
            b += 0x10 # 横倍拡大(1バイトコード文字)
        if dh:
            n += 0x08 # 縦倍拡大
            b += 0x20 # 縦倍拡大(1バイトコード文字)
        if underline:
            n += 0x80 # 漢字アンダーライン
            b += 0x80 # アンダーライン(1バイトコード文字)
        if n != 0x00:
            if bflg:
                self._raw(ESC + b'!' + b.to_bytes(1, byteorder='big')) # ESC ! 印字モードの一括指定(指定)
            self._raw(FS + b'!' + n.to_bytes(1, byteorder='big')) # FS ! 漢字の印字モードの一括指定(指定)
        if wbreverse:
            self._raw(GS + b'B' + b'\x01') # GS B 反転

        binary_str = b''
        call_define = False
        for c in text:
            if c.isascii() or c in self.jis_x_0201 or c in self.jis_x_0208:
                # Built-in Kanji Font
                binary_str = c.encode('cp932','ignore')
                call_define = False
            elif c in self.jis_x_0212 or c in self.jis_x_0213:
                # Kanji Font
                params = dict(
                    font=self.kanji_font_file,
                    size=self.kanji_font_size,
                    adjustX=self.kanji_font_adjust_x,
                    adjustY=self.kanji_font_adjust_y,
                    asciiflg=False)
                call_define = True
            elif emoji.is_emoji(c):
                # Emoji Font
                params = dict(
                    font=self.emoji_font_file,
                    size=self.emoji_font_size,
                    adjustX=self.emoji_font_adjust_x,
                    adjustY=self.emoji_font_adjust_y,
                    asciiflg=False)
                call_define = True
            else:
                # Fallback Font
                params = dict(
                    font=self.fallback_font_file,
                    size=self.fallback_font_size,
                    adjustX=self.fallback_font_adjust_x,
                    adjustY=self.fallback_font_adjust_y,
                    asciiflg=False)
                call_define = True

            if call_define:
                # Register gaiji
                binary_str = self._define_gaiji(gaiji=c, **params)

            self._raw(binary_str)

        if n != 0x00:
            if bflg:
                self._raw(ESC + b'!' + b'\x00') # ESC ! 印字モードの一括指定(解除)
            self._raw(FS + b'!' + b'\x00') # FS ! 漢字の印字モードの一括指定(解除)
        if wbreverse:
            self._raw(GS + b'B' + b'\x00') # GS B 反転解除
