import wmi as wmi
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL, POINTER, cast


def speakers_mute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "chrome.exe":
            volume.SetMute(0, None)
        else:
            volume.SetMute(1, None)


def speakers_change_volume_level(mode):
    if mode == 1:
        changeLevel = 0.1
    else:
        changeLevel = -0.1

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "chrome.exe":
            volume.SetMasterVolume(volume.GetMasterVolume() + changeLevel, None)


def change_brightness(brightness_level):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness_level, 0)
