import MyGraphics as mg

# to get all the audio volumes from windows
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# for windows media control
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

#for async functions
import asyncio

import threading

def clamp(current, min, max):
    if current > max:
        return max
    elif current < min:
      return min
    else:
        return current  
                
def changeVolume(changeTo):
    # gets basically all open apps
    sessions = AudioUtilities.GetAllSessions()

    # iterate through all sessions
    for session in sessions:
        
        # a process is a python object that shows it
        process = session.Process
        if process:
            if "amazon" in process.name().lower() or "spotify" in process.name().lower():
                
                # assign volume as what controlls the app volume
                # query interface will ask windows for control of the parameter, in this case the volume
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                
                current_volume = volume.GetMasterVolume()
                
                volumeToSet = (float(changeTo)/100)
                
                volumeToSet = clamp(volumeToSet, 0.0, 1.0)
                
                # the volume to set  is a normalized value between 0 and 1, so you have to normalize change_volume
                volume.SetMasterVolume(volumeToSet, None)
      
      
async def toggle_play_pause():


    # get windows media manager
    manager = await MediaManager.request_async()
    
    # get the current app playing audio
    
    currentApp = manager.get_current_session()
    
    # null check
    if currentApp:
        # toggle play  or poss
        
        await currentApp.try_toggle_play_pause_async()
        
        await currentApp.add
        
async def skip_song(amountToSkip: int):


    # get windows media manager
    manager = await MediaManager.request_async()
    
    # get the current app playing audio
    
    currentApp = manager.get_current_session()
    
    # null check
    if currentApp:
        
        if amountToSkip > 0:
            await currentApp.try_skip_next_async()
        elif amountToSkip < 0:
            await currentApp.try_skip_previous_async()
        
    else:
        print("Nothing is playing")
        
def run_play_toggle():
    asyncio.run(toggle_play_pause())
    
def run_skip_song(amountToSkip: int):
    asyncio.run(skip_song(amountToSkip=amountToSkip))

    
keybindVal = ''

# Set to hold currently pressed keys
pressed_keys = set()
    
keybind = 'm'
    
asciiKeys = {
    
    'a' : 1,
    'b' : 2,
    'c' : 3,
    'd' : 4,
    'e' : 5,
    'f' : 6,
    'g' : 7,
    'h' : 8,
    'i' : 9,
    'j' : 10,
    'k' : 11,
    'l' : 12,
    'm' : 13,
    'n' : 14,
    'o' : 15,
    'p' : 16,
    'q' : 17,
    'r' : 18,
    's' : 19,
    't' : 20,
    'u' : 21,
    'v' : 22,
    'w' : 23,
    'x' : 24,
    'y' : 25,
    'z' : 26,
}
def on_key_press(key):
    keybind = controlInput.getFieldContents()
    
    pressed_keys.add(key)
    
    ctrHeld = mg.keyboard.Key.ctrl_l in pressed_keys
    shiftHeld = mg.keyboard.Key.shitext_vartext_vartext_vartext_vartext_vartext_vartext_vartext_varMft in pressed_keys
    key_held = mg.keyboard.KeyCode.from_char(keybind) in pressed_keys or mg.keyboard.KeyCode.from_char(chr(asciiKeys[keybind])) in pressed_keys
    
    if ctrHeld and shiftHeld and key_held:
        toggle_alpha()
        
    print(keybind)
        
def on_key_release(key):
    # Remove the released key
    pressed_keys.discard(key)
    
      
window = mg.Window([
    mg.Attribute('-topmost', True),
    mg.Attribute('-toolwindow', True),
    mg.Attribute('-fullscreen', True),
    mg.Attribute('-transparentcolor', 'black'),
    mg.Attribute('-backgroundcolor', 'black'),
    ],
    on_key_press=on_key_press,
    on_key_release=on_key_release
)

window.root.title("My App Name")

async def monitor_song_changes():
    manager = await MediaManager.request_async()

    previous_title = ''
    
    while True:
        session = manager.get_current_session()
        if session:
            info = await session.try_get_media_properties_async()
            title = info.title
            
            if previous_title:
                if title != previous_title and previous_title != '':
                    previous_title = title
                    print(f"🔄 Song changed: {title}")
                    print("Song Changed")
                    previous_title = title
                    
                    print(volumeSlider.get())
                    changeVolume(volumeSlider.get())
            else:
                previous_title = title

        await asyncio.sleep(0.1)  # Light polling every 1 second

def run_monitor():
    asyncio.run(monitor_song_changes())

threading.Thread(target=run_monitor, daemon=True).start()

volumeSlider = mg.Slider(window, 2, 3, startVal=100, endVal=0, orient="horizontal", command=changeVolume)

# to make sure when the song changes the volume doesn't reset
def reset_volume():
    # Your function that sets volume back using slider
    print("Amazon session changed — re-applying volume")
    changeVolume(volumeSlider.get())  # assuming you have this from your UI
                

# on start change to current volume

# gets basically all open apps
sessions = AudioUtilities.GetAllSessions()

# iterate through all sessions
for session in sessions:
        
    process = session.Process
    
    if process:
        if "amazon" in process.name().lower():
                
            # assign volume as what controlls the app volume
            # query interface will ask windows for control of the parameter, in this case the volume
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                
            current_volume = volume.GetMasterVolume()
            
            # the volume to set  is a normalized value between 0 and 1, so you have to normalize change_volume
            volume.SetMasterVolume(current_volume, None)

            # adjust for normalization
            volumeSlider.set(current_volume * 100)
                
def changeVolumeBy(changeAmount):
    # gets basically all open apps
    sessions = AudioUtilities.GetAllSessions()

    # iterate through all sessions
    for session in sessions:
        
        # a process is a python object that shows it
        process = session.Process
        if process:
            if "amazon" in process.name().lower() or "spotify" in process.name().lower():
                
                # assign volume as what controlls the app volume
                # query interface will ask windows for control of the parameter, in this case the volume
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                
                current_volume = volume.GetMasterVolume()
                volumeToSet = (current_volume + (changeAmount/100))
                
                volumeToSet = clamp(volumeToSet, 0.0, 1.0)
                
                # the volume to set  is a normalized value between 0 and 1, so you have to normalize change_volume
                volume.SetMasterVolume(volumeToSet, None)
                
                volumeSlider.set(volumeToSet * 100)
                print(current_volume)


    
upVolumeBtn = mg.Button(window, 3, 3, '+', command=lambda: changeVolumeBy(+2))
downVolumeBtn = mg.Button(window, 1, 3, '-', command=lambda: changeVolumeBy(-2))


previousSongBtn = mg.Button(window, 1, 4, '<', lambda: {
    run_skip_song(-1)
})
pauseBtn = mg.Button(window, 2, 4, '▶️/⏸️', run_play_toggle)
nextSongBtn = mg.Button(window, 3, 4, '>', lambda: {
    run_skip_song(1)
})



titleLabel = mg.Label(window, 0, 1, "Enter Your Keybind To Open, Ctrl + Shift + :")
controlInput = mg.InputField(window, 0, 2, maxCharacters=1, textvalue=keybind)




def toggle_alpha():
    current_alpha = window.attributes("-alpha")
    
    if current_alpha == 1.0:
        window.set_attribute("-alpha", 0)
    elif current_alpha == 0:
        window.set_attribute("-alpha", 1)


window.run()