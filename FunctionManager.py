
from pycaw.pycaw import AudioUtilities
from comtypes import CLSCTX_ALL, POINTER, cast

def speakersMute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "chrome.exe":
            volume.SetMute(0, None)
        else:
            volume.SetMute(1, None)