import wmi as wmi
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL, POINTER, cast

def speakersMute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "chrome.exe":
            volume.SetMute(0, None)
        else:
            volume.SetMute(1, None)




def speakersChangeVolumeLevel(mode):
    changeLevel = 0
    if(mode == 1):
        changeLevel=0.1
    else:
        changeLevel=-0.1

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "chrome.exe":
            volume.SetMasterVolume(volume.GetMasterVolume()+ changeLevel, None)


def changeBrightness(brightnessLevel):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightnessLevel, 0)
