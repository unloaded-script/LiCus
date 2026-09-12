
# LiCus
## A small and low-end compatible wine launcher.

This is just a simple wine launcher. The limitations are listed below:
- Cannot handle big games.
- No Wine's errors handling
- No crash logs

## How to install into Archlinux

### 1. Download the ZIP file
Click the '<> Code' button. Once you click, find the text "Download ZIP". Click it

### 2. Download the needed packages
If you didn't install `wine` or `gamemode` or `unzip` yet, follow these steps below

Wine:
```bash
sudo pacman -S wine
```

GameMode:
```bash
sudo pacman -S gamemode
```

Unzip:
```bash
sudo pacman -S unzip
```

### 3. Set LiCus as CLI tool
Navigate to your `LiCus-main.zip`. Usually, it will be in your `Downloads`.

```bash
cd Downloads
```

Unzip it

```bash
unzip LiCus-main.zip
```

Now, you will see a folder called `LiCus-main`. Navigate to it.

```bash
cd LiCus-main
```

We will make `main.py` executable.

```bash
chmod +x main.py
```

Then, we will move the script into `/usr/local/bin` to turn this simple script into CLI tool

```bash
sudo ln -s main.py /usr/local/bin/licus
```

And there you have it, your own LiCus inside your Arch. Type

```bash
licus
```

to activate it.
