# AutoOverlay
overlay graphics with keybinds, a CLI, and python

## Install

```sh
python -m venv venv
./venv/Scripts/activate # Windows
pip install -r requirements


# Build .exe
pyinstaller --onefile --name ripper --distpath /dist main.py
```

## Usage

```sh
# Help
python .\examples\static_image\cli.py

# Info
python .\examples\static_image\cli.py start-overlay

# Set Bind
python .\examples\static_image\cli.py start-overlay
```

