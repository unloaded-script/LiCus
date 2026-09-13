
# LiCus
## A small and low-end compatible wine launcher.

This is just a simple wine launcher. The limitations are listed below:
- Cannot handle big games.
- No Wine's errors handling
- No crash logs

## How to install into Archlinux

### 1. Clone this Repository
To install this CLI tool, we can use git for smoother installation

```bash
git clone https://github.com/unloaded-script/LiCus.git
```

And then navigate into `LiCus`

```bash
cd LiCus
```

### 2. Install Dependencies
We need dependencies for LiCus to work:

```bash
bash dependencies_intall.sh
```

If the above steps might not work, install `wine`, `gamemode`, `git`, and the needed Python libraries manually

```bash
sudo pacman -S git wine gamemode
```
Python libraries installation:

```bash
sudo pacman -S python-rich
yay -S python-pynput
```

### 3. Turn this script into CLI tool
And here's the part where this simple script tool become simple launcher.

```bash
chmod +x main.py
```

Then, we will move the `main.py` into `usr/local/bin`

```bash
sudo ln -s ~/LiCus/main.py /usr/local/bin/licus
```

And that's it, your own LiCus inside your own Arch.

### 4. How to use
Simply, just type in your terminal

```bash
licus
```

And the title screen will appear.

### 5. How to update
Easily, if the LiCus terminal shows any latest update, run this

```bash
cd ~/LiCus && git pull
```
