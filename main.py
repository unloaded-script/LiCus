#!/usr/bin/env python3

import os
import shutil
import time
import subprocess
import sys
import shlex
import requests
import json
from pathlib import Path
from pynput import keyboard
from rich import print
from rich.prompt import Prompt
from rich.progress import track

# data_dir = Path("../../..")

# array1 = os.listdir(data_dir)
# print(array1)

CURRENT_VERSION = "v0.1.0"

def padToCenter(l:list,w:int)->str:
    """Manual centering"""
    padding =  ' '*(w//2) # a 1 char line would need at most w/2 spaces in front
    parts = [ padding[0: (w-len(p))//2+1]+p for p in l]
    return '\n'.join(parts)

def padToCenter2(l:list,w:int)->str:
    return '\n'.join('-'+x.center(w)+'-' for x in l)

def check_for_update():
    try:
        response = requests.get(
            "https://api.github.com/repos/unloaded-script/LiCus/releases/latest",
            timeout=5
        )
        latest = response.json()["tag_name"]
        if latest != CURRENT_VERSION:
            print(f"[bold yellow]Update available: {latest} LiCus[/bold yellow] (You're currently using {CURRENT_VERSION} LiCus)")
            print(f"[bold] You can get it at: https://github.com/unloaded-script/LiCus/releases[/bold]")
    except Exception:
        pass

def startup():
    os.system('clear')
    title = """ 
    [bold green]   
    ██╗     ██╗ ██████╗██╗   ██╗███████╗
    ██║     ██║██╔════╝██║   ██║██╔════╝
    ██║     ██║██║     ██║   ██║███████╗
    ██║     ██║██║     ██║   ██║╚════██║
    ███████╗██║╚██████╗╚██████╔╝███████║
    ╚══════╝╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    [/bold green]                              
    """
    print(padToCenter(title.splitlines(),60))
    print(padToCenter("[bold green]Copyright (c) 2026 [Redacted][/bold green]".splitlines(), 90))
    check_for_update()

    print(padToCenter("[bold]An Arch Linux Custom Game Launcher. Made by Redacted.[/bold]".splitlines(), 38))
    print(padToCenter("Type 'help' for guides.".splitlines(), 60))

    input = Prompt.ask("\n[bold]Enter your game file's directory[/bold]")
    if input.lower() == "exit":
        print("[bold]Terminating...[/bold]")
        sys.exit()
    elif input.lower() == "help":

        instructions = """
        -      Type [bold red]exit[/bold red] to terminate LiCus    -
        -      [bold]Drag[/bold] your file into the prompt          -
        -      OR [bold]type[/bold] your directory into the prompt  -
        -      Press 'ALT + SHIFT + X' to force exit the games      -
        """

        print(padToCenter(instructions.splitlines(), 35))
    
        count = 9
        while count > 0:
            count -= 1
            text = f"Resetting in {count}"
    
            sys.stdout.write(f"\r\033[K{text}")
            sys.stdout.flush()
    
            time.sleep(1)
        startup()
    return input

def kill_wine():
    print("Terminating...")
    subprocess.run(["wineserver", "-k"])
    return False

hotkeys = keyboard.GlobalHotKeys({
    '<alt>+<shift>+x': kill_wine
})

input = startup()

file_dir = os.path.expanduser(input)
file_dir = file_dir.strip("'\"")

programs = ["wine", "gamemoderun"]

game_exe = Path(file_dir).expanduser()
if not game_exe.name.endswith(".exe"):
        print("[bold red]Your file is not a valid .exe files![/bold red]")
        sys.exit()

loading_desc = f"[bold green]Checking {game_exe.name}'s validity and packages...[/bold green]"
need_exit = False
for item in track(range(1), description=loading_desc):

    for program in programs:
        if shutil.which(program):
            print(f"[bold]{program} installed [/bold]")
        else:
            print(f"[bold red]{program} not installed yet[/bold red]")
            need_exit = True

if need_exit == True:
    kill_wine()

print(f"\nLaunching {game_exe.name}...")
wine_process = subprocess.Popen(["gamemoderun", "wine", file_dir])

hotkeys.start()

try:
    wine_process.wait()
finally:
    hotkeys.stop()
