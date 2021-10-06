from playsound import playsound
import wx.adv
import wx
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play
import os
from time import sleep
from audioplayer import AudioPlayer
import simpleaudio as sa
import pyaudio
import wave

soundpath = "good_1.wav"

def test_playsound():
    playsound(soundpath)

def test_pydub():
    song = AudioSegment.from_wav(soundpath)
    play(song)

def test_mpg123():
    os.system("mpg123 " + soundpath)

def test_audioplayer():
    AudioPlayer(soundpath).play(block=True)

def test_simpleaudio():
    wave_obj = sa.WaveObject.from_wave_file(soundpath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def test_pyaudio():
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  
    # Open the sound file 
    wf = wave.open(soundpath, 'rb')
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()
    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    # Read data in chunks
    data = wf.readframes(chunk)
    # Play the sound by writing the audio data to the stream
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    # Close and terminate the stream
    stream.close()
    p.terminate()

def test_pygame():
    # Starting the mixer
    mixer.init()
    # Loading the song
    mixer.music.load(soundpath)
    # Setting the volume
    mixer.music.set_volume(1)
    # Start playing the song
    mixer.music.play()

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="wx.Sound",size=(500,100))
        p = wx.Panel(self)
        self.sound = wx.adv.Sound(soundpath)
        if self.sound.IsOk():
            self.sound.Play(wx.adv.SOUND_ASYNC)

def test_wxpyton():
    app = wx.App()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
    

def test_func(func):
    print("-------------------------------------------")
    print("Test: " + func.__name__)
    func()
    sleep(1)

# test_func(test_playsound)
test_func(test_pydub)
# test_func(test_mpg123)
# test_func(test_audioplayer)
test_func(test_simpleaudio)
test_func(test_pygame)
# test_func(test_wxpyton)
# test_func(test_pyaudio)