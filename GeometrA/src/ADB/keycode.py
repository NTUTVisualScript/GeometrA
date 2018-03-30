class AndroidKeycode:
    mapping = {}

    SOFT_LEFT = 1
    SOFT_RIGHT = 2
    ENDCALL = 6
    HOME = 3
    BACK = 4
    CALL = 5
    DPAD_UP = 19
    DPAD_DOWN = 20
    DPAD_LEFT = 21
    DPAD_RIGHT = 22
    DPAD_CENTER = 23
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    POWER = 26
    CAMERA = 27
    CLEAR = 28
    ALT_LEFT = 57
    ALT_RIGHT = 58
    SHIFT_LEFT = 59
    SHIFT_RIGHT = 60
    TAB = 61
    ENTER = 66
    SYM = 63
    EXPLORER = 64
    ENVELOPE = 65
    DEL = 67
    NUM = 78
    HEADSETHOOK = 79
    FOCUS = 80
    MENU = 82
    NOTIFICATION = 83
    SEARCH = 84
    MEDIA_PLAY_PAUSE = 85
    MEDIA_STOP = 86
    MEDIA_NEXT = 87
    MEDIA_PREVIOUS = 88
    MEDIA_REWIND = 89
    MEDIA_FAST_FORWARD = 90
    MUTE = 91

    def __init__(self):
        # 0 ~ 9
        keycode_0 = 7
        for index in range(0, 10):
            self.mapping[str(index)] = keycode_0 + index

        # a ~ z
        keycode_a = 29
        ascii_a = ord('a')
        for code in range(ord('a'), ord('z') + 1):
            self.mapping[chr(code)] = code - ascii_a + keycode_a

        self.mapping['*'] = 17
        self.mapping['#'] = 18
        self.mapping[','] = 55
        self.mapping['.'] = 56
        self.mapping[' '] = 62
        self.mapping['`'] = 68
        self.mapping['-'] = 69
        self.mapping['='] = 70
        self.mapping['['] = 71
        self.mapping[']'] = 72
        self.mapping['\\'] = 73
        self.mapping[';'] = 74
        self.mapping['"'] = 75
        self.mapping['/'] = 76
        self.mapping['@'] = 77
        self.mapping['+'] = 81
        self.mapping['('] = 162
        self.mapping[')'] = 163

    def __getattr__(self, name):
        return self.mapping.get(name, None)

ANDROID_KEYCODE = AndroidKeycode()
