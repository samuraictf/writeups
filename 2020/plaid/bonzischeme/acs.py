# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Acs(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._root.AcsFileHeader(self._io, self, self._root)

    class Localizedinfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.langid = self._io.read_u2le()
            self.name = self._root.String(self._io, self, self._root)
            self.desc = self._root.String(self._io, self, self._root)
            self.extra = self._root.String(self._io, self, self._root)


    class Voiceinfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.tts_engine_id = self._root.Guid(self._io, self, self._root)
            self.tts_mode_id = self._root.Guid(self._io, self, self._root)
            self.speed = self._io.read_u4le()
            self.pitch = self._io.read_u2le()
            self.extra_data = self._io.read_u1()
            if self.extra_data == 1:
                self.lang_id = self._io.read_u2le()

            if self.extra_data == 1:
                self.lang_dialect = self._root.String(self._io, self, self._root)

            if self.extra_data == 1:
                self.gender = self._io.read_u2le()

            if self.extra_data == 1:
                self.age = self._io.read_u2le()

            if self.extra_data == 1:
                self.style = self._root.String(self._io, self, self._root)



    class Guid(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data1 = self._io.read_u4le()
            self.data2 = self._io.read_u2le()
            self.data3 = self._io.read_u2le()
            self.data4 = [None] * (8)
            for i in range(8):
                self.data4[i] = self._io.read_u1()



    class AcsFileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\xC3\xAB\xCD\xAB")
            self.character_info_loc = self._root.Acslocator(self._io, self, self._root)
            self.animation_info_loc = self._root.Acslocator(self._io, self, self._root)
            self.image_info_loc = self._root.Acslocator(self._io, self, self._root)
            self.audio_info_loc = self._root.Acslocator(self._io, self, self._root)

        @property
        def character_info(self):
            if hasattr(self, '_m_character_info'):
                return self._m_character_info if hasattr(self, '_m_character_info') else None

            _pos = self._io.pos()
            self._io.seek(self.character_info_loc.offset)
            self._m_character_info = self._root.Acscharacterinfo(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_character_info if hasattr(self, '_m_character_info') else None

        @property
        def image_info(self):
            if hasattr(self, '_m_image_info'):
                return self._m_image_info if hasattr(self, '_m_image_info') else None

            _pos = self._io.pos()
            self._io.seek(self.image_info_loc.offset)
            self._m_image_info = self._root.AcsImageInfoArr(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_image_info if hasattr(self, '_m_image_info') else None


    class String(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            if self.size > 0:
                self.data = (self._io.read_bytes(((self.size + 1) * 2))).decode(u"UTF-16LE")



    class Acslocator(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.length = self._io.read_u4le()


    class ImageInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk = self._io.read_u1()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.compressed = self._io.read_u1()
            self.data = self._root.DataBlock(self._io, self, self._root)
            self.sz_compressed = self._io.read_u4le()
            self.sz_uncompressed = self._io.read_u4le()
            self.region_data = [None] * (self.sz_compressed)
            for i in range(self.sz_compressed):
                self.region_data[i] = self._io.read_u1()



    class AcsImageInfoArr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.arr = [None] * (self.count)
            for i in range(self.count):
                self.arr[i] = self._root.AcsImageInfo(self._io, self, self._root)



    class Localizedinfoarr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u2le()
            self.arr = [None] * (self.count)
            for i in range(self.count):
                self.arr[i] = self._root.Localizedinfo(self._io, self, self._root)



    class DataBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            self.data = [None] * (self.size)
            for i in range(self.size):
                self.data[i] = self._io.read_u1()



    class Ballooninfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_lines = self._io.read_u1()
            self.chars_per_line = self._io.read_u1()
            self.foreground = self._io.read_u4le()
            self.background = self._io.read_u4le()
            self.border = self._io.read_u4le()
            self.font_name = self._root.String(self._io, self, self._root)
            self.font_height = self._io.read_u4le()
            self.font_weight = self._io.read_u4le()
            self.italic_flag = self._io.read_u1()
            self.other_flag = self._io.read_u1()


    class AcsImageInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.loc = self._root.Acslocator(self._io, self, self._root)
            self.checksum = self._io.read_u4le()

        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body if hasattr(self, '_m_body') else None

            _pos = self._io.pos()
            self._io.seek(self.loc.offset)
            self._m_body = self._root.ImageInfo(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_body if hasattr(self, '_m_body') else None


    class Acscharacterinfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.minor = self._io.read_u2le()
            self.major = self._io.read_u2le()
            self.localized_info_loc = self._root.Acslocator(self._io, self, self._root)
            self.guid = self._root.Guid(self._io, self, self._root)
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.transparent_idx = self._io.read_u1()
            self.flags = self._io.read_u4le()
            self.animation_maj = self._io.read_u2le()
            self.animation_min = self._io.read_u2le()
            self.voiceinfo = self._root.Voiceinfo(self._io, self, self._root)
            self.ballooninfo = self._root.Ballooninfo(self._io, self, self._root)
            self.palette_len = self._io.read_u4le()
            self.palette = [None] * ((self.palette_len * 4))
            for i in range((self.palette_len * 4)):
                self.palette[i] = self._io.read_u1()


        @property
        def localized_info(self):
            if hasattr(self, '_m_localized_info'):
                return self._m_localized_info if hasattr(self, '_m_localized_info') else None

            _pos = self._io.pos()
            self._io.seek(self.localized_info_loc.offset)
            self._m_localized_info = self._root.Localizedinfoarr(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_localized_info if hasattr(self, '_m_localized_info') else None



