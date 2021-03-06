import sys
sys.path.insert(0, "/usr/local/lib/python3.5/dist-packages")
print(sys.path)
from pocketsphinx.pocketsphinx import *
import pyaudio


class SpeechRecognition:
    parent = None

    def __init__(self):
        self.command = 0
        self.config = Decoder.default_config()
        self.config.set_string('-hmm',
                               './pocketsphinx-master/model/en-us/en-us/')
        self.config.set_string('-lm', './6465.lm')
        self.config.set_string('-dict', './6465.dic')
        self.decoder = Decoder(self.config)

        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    # Speech recognition
    def speech_rec(self):
        self.stream.start_stream()
        in_speech_bf = False
        self.decoder.start_utt()
        while True:
            if self.parent.speech_enable:
                buf = self.stream.read(1024, exception_on_overflow=False)
                if buf:
                    self.decoder.process_raw(buf, False, False)
                    if self.decoder.get_in_speech() != in_speech_bf:
                        in_speech_bf = self.decoder.get_in_speech()
                        if not in_speech_bf:
                            self.decoder.end_utt()
                            self.command = self.emun(self.decoder.hyp().hypstr)
                            self.decoder.start_utt()
                else:
                    break
        self.decoder.end_utt()

    # Run command from speech recognition
    def do_speech_rec(self):
        if self.command == 1:
            self.parent.parent.blur1_callback()
        elif self.command == 2:
            self.parent.parent.zoom1_callback()
        elif self.command == 3:
            self.parent.parent.gain.set(self.parent.parent.gain.get() + 10)
        elif self.command == 5:
            self.parent.parent.blur2_callback()
        elif self.command == 6:
            self.parent.parent.gain.set(self.parent.parent.gain.get() - 10)
        elif self.command == 7:
            self.parent.parent.zoom2_callback()
        elif self.command == 4:
            self.parent.parent.snap_call()
        elif self.command == 11:
            self.parent.parent.default_callback()
        elif self.command == 12:
            self.parent.parent.country_callback()
        elif self.command == 13:
            self.parent.parent.desert_callback()
        elif self.command == 14:
            self.parent.parent.lumo_callback()
        elif self.command == 15:
            self.parent.parent.nashville_callback()
        if self.command != 0:
            print('*************{}'.format(self.command))
        self.command = 0

    def emun(self, x):
        return {
            'BLUR': 1,
            'BIGGER': 2,
            'BRIGHTER': 3,
            'CLEAR': 5,
            'DARKER': 6,
            'CHEESE': 4,
            'SMALLER': 7,
            'ONE': 11,
            'TWO': 12,
            'THREE': 13,
            'FOUR': 14,
            'FIVE': 15
        }.get(x, 0)
