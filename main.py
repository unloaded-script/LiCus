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
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding

# data_dir = Path("../../..")

# array1 = os.listdir(data_dir)
# print(array1)

CURRENT_VERSION = "v0.2.0"

console = Console()

config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
config_dir = config_home / "licus"

recentjson_file = config_dir / "recent_exe.json"
config_dir.mkdir(parents=True, exist_ok=True)

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
            print(f"[bold]Exit LiCus and run this to update:[/bold] cd ~/LiCus && git pull")
    except Exception:
        pass

data_template = {
    "recent_games": [
    ]
}

passed = True

try:
    with recentjson_file.open("r") as file:
        data = json.load(file)
except FileNotFoundError:
    with recentjson_file.open("w") as file:
        json.dump(data_template, file, indent=4)
    
    passed = False

def kill_wine():
    print("Terminating...")
    subprocess.run(["wineserver", "-k"])
    return False

hotkeys = keyboard.GlobalHotKeys({
    '<alt>+<shift>+x': kill_wine
})

def launch(file_dir):
    wine_process = subprocess.Popen(["gamemoderun", "wine", file_dir])

    hotkeys.start()

    try:
        wine_process.wait()
    finally:
        hotkeys.stop()

def startup():
    os.system('clear')
    title = """ 
    [red]
    ██╗     ██╗ ██████╗██╗   ██╗███████╗
    ██║     ██║██╔════╝██║   ██║██╔════╝
    ██║     ██║██║     ██║   ██║███████╗
    ██║     ██║██║     ██║   ██║╚════██║
    ███████╗██║╚██████╗╚██████╔╝███████║
    ╚══════╝╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    [/red]
    """
    console.print(title, justify="center")
    console.print("[bold green]Copyright (c) 2026 [Redacted][/bold green]", justify="center")
    check_for_update()

    if passed == False:
        console.print("[bold yellow](Recent Data not found! Creating a new one...)[/bold yellow]", justify="center")
    console.print("[bold]An Arch Linux Custom Game Launcher. Made by Redacted.[/bold]", justify="center")
    console.print("Type 'help' for guides.", justify="center")

    user_input = input("̢»   ")
    if user_input.lower() == "exit":
        print("[bold]Terminating...[/bold]")
        sys.exit()
    elif user_input.lower() == "help":

        instructions = """
        ::  Type [bold red]exit[/bold red] to terminate LiCus
        ::  Type [bold green]recent[/bold green] to open recent games

        ::  [bold]Drag[/bold] your file into the prompt
        ::  OR [bold]type[/bold] your directory into the prompt
        ::  Press [bold]'ALT + SHIFT + X'[/bold] to force exit the games
        """

        console.print(Panel(
            Padding(instructions, (0, 7, 0, 0)),
            title="LiCus's Help Guide",
            expand=False,
            subtitle_align="right"
        ), justify="center")
    
        count = 9
        while count > 0:
            count -= 1
            text = f"Resetting in {count}"
    
            sys.stdout.write(f"\r\033[K{text}")
            sys.stdout.flush()
    
            time.sleep(1)
        startup()
    
    elif user_input.lower() == "recent":
        parent = data["recent_games"]
        index = 0
        for game in parent:
            print(f"\n[bold green]{index + 1}[/bold green]. [bold]{game}[/bold]")
            index += 1
        
        try:
            choice = int(Prompt.ask("\n[bold]Enter the game's number [/bold][bold green][1 - 5][/bold green]"))
        except ValueError:
            print("[bold red]Your choice is invalid![/bold red]")
            time.sleep(1)
            startup()
        
        if not isinstance(choice, int):
            print("[bold red]Your choice is invalid![/bold red]")
            time.sleep(1)
            startup()
        else:
            try:
                print(f"\nGame Selected:{data["recent_games"][choice - 1]}")
            except IndexError:
                print("[bold red]Your choice is invalid![/bold red]")
                time.sleep(1)
                startup()
        
            file_dir = os.path.expanduser(data["recent_games"][choice - 1])
            file_dir = file_dir.strip("'\"")

            programs = ["wine", "gamemoderun"]

            game_exe = Path(file_dir).expanduser()
            if not game_exe.name.endswith(".exe"):
                    print("[bold red]Your file is not a valid .exe files![/bold red]")
                    time.sleep(1)
                    startup()

            loading_desc = f"[bold green]Checking {game_exe.name}'s validity and packages...[/bold green]"
            need_exit = False
            for item in track(range(1), description=loading_desc):

                for program in programs:
                    if shutil.which(program):
                        print(f"[bold]{program} installed [/bold]")
                    else:
                        print(f"[bold red]{program} not installed yet[/bold red]")
                        need_exit = True
    
                with open(game_exe, "rb") as file:
                    load_data = file.read(64)
    
                if (load_data[:2] == b"MZ") == False:
                    print("[bold red]Your file is not a valid .exe files![/bold red]")
                    need_exit = True
    
                time.sleep(1)

            if need_exit == True:
                startup()

            print(f"\nLaunching {game_exe.name}...")
            data["recent_games"].insert(0, file_dir)
            data["recent_games"] = data["recent_games"][:5]

            with open("recent_exe.json", "w") as file:
                json.dump(data, file, indent=4)
    
            launch(file_dir)
    
    else:
        file_dir = os.path.expanduser(user_input)
        file_dir = file_dir.strip("'\"")

        programs = ["wine", "gamemoderun"]

        game_exe = Path(file_dir).expanduser()
        if not game_exe.name.endswith(".exe"):
                print("[bold red]Your file is not a valid .exe files![/bold red]")
                time.sleep(1)
                startup()

        loading_desc = f"[bold green]Checking {game_exe.name}'s validity and packages...[/bold green]"
        need_exit = False
        for item in track(range(1), description=loading_desc):

            for program in programs:
                if shutil.which(program):
                    print(f"[bold]{program} installed [/bold]")
                else:
                    print(f"[bold red]{program} not installed yet[/bold red]")
                    need_exit = True
    
            with open(game_exe, "rb") as file:
                load_data = file.read(64)
    
            if (load_data[:2] == b"MZ") == False:
                print("[bold red]Your file is not a valid .exe files![/bold red]")
                need_exit = True
    
            time.sleep(1)

        if need_exit == True:
            startup()

        print(f"\nLaunching {game_exe.name}...")
        data["recent_games"].insert(0, file_dir)
        data["recent_games"] = data["recent_games"][:5]

        with recentjson_file.open("w") as file:
            json.dump(data, file, indent=4)
    
        launch(file_dir)

user_input = startup()
