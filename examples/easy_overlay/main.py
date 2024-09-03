import click
import keyboard
from overlay import Overlay
from utils import load_keybind, set_keybind, keycode_to_human


@click.group()
def cli():
    pass


@click.command()
def set_keybind():
    current_key = load_keybind()
    print(
        f"Current keybind: {keycode_to_human(current_key)} - Press a key to set a new keybind"
    )
    new_key = keyboard.read_event()
    set_keybind(new_key.name)


@click.command()
def display_overlay():
    ov = Overlay()
    print("Press 'Esc' to exit overlay display")
    keyboard.add_hotkey("esc", lambda: ov.toggle_visibility())
    ov.display()
    keyboard.wait("esc")
    keyboard.remove_hotkey("esc")
    print("Returning to menu...")


cli.add_command(set_keybind)
cli.add_command(display_overlay)

if __name__ == "__main__":
    cli()
