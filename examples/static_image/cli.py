import click
import json
import glfw
from overlay import Overlay

CONFIG_FILE = "config.json"


@click.group()
def cli():
    click.echo("Welcome to the Overlay CLI!")


@cli.command()
def set_keybind():
    """Set the keybind by listening for the next key press."""
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    def key_callback(window, key, scancode, action, mods):
        if action == glfw.PRESS:
            overlay.save_keybind(key)
            click.echo(f"Keybind set to: {key}")
            glfw.set_window_should_close(window, True)

    window = glfw.create_window(200, 200, "Press a Key", None, None)
    glfw.set_window_attrib(window, glfw.FLOATING, True)
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

    glfw.terminate()


@cli.command()
def start_overlay():
    """Start the overlay with the current configuration."""
    overlay = Overlay(CONFIG_FILE)
    overlay.run()


if __name__ == "__main__":
    cli()
