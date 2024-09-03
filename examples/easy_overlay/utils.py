import yaml


def keycode_to_human(keycode):
    return keycode  # Replace with actual conversion logic


def load_keybind():
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        return config["keybind"]
    except FileNotFoundError:
        return "esc"  # Default key


def set_keybind(key):
    with open("config.yaml", "w") as f:
        yaml.safe_dump({"keybind": key}, f)
