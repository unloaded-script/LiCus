
# LiCus
## A small and low-end compatible wine launcher.

This is just a simple wine launcher. The limitations are listed below:
- Cannot handle big games.
- No Wine's errors handling
- No crash logs

## How to install into Archlinux

### 1. Install Dependencies
If you didn't already install `wine` or `gamemode` or `git`, install them first since LiCus will be using them

```bash
sudo pacman -S git wine gamemode
```
**IMPORTANT**
To run LiCus smoothly, it needs two external python libraries.

```bash
sudo pacman -S python-rich
yay -S python-pynput
```

### 2. Clone this Repository
To install this CLI tool, we can use git for smoother installation.

```bash
git clone https://github.com/unloaded-script/LiCus.git
```

And then navigate into `LiCus`

```bash
cd LiCus
```

### 3. Turn this script into CLI tool
And here's the part where this simple script tool become simple launcher.

```bash
chmod +x main.py
```

Then, we will move the `main.py` into `usr/local/bin`

```bash
sudo ln -s main.py /usr/local/bin/licus
```

And that's it, your own LiCus inside your own Arch.

### 4. How to use
Simply, just type in your terminal

```bash
licus
```

And the title screen will appear.
