import click
import yaml
import glfw
import os

from overlay import Overlay


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the configuration file
CONFIG_FILE = os.path.join(script_dir, "config.yaml")
DEFAULT_CONFIG = {"keybind": "space"}  # Default keybind set to 'space'


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A CLI tool to manage overlay configurations and operations."""
    if ctx.invoked_subcommand is None:
        click.echo("No command specified. Available commands are:")
        click.echo("1: Set Keybind")
        click.echo("2: Start Overlay")
        choice = click.prompt("Please choose an option (1 or 2)", type=int)

        if choice == 1:
            ctx.invoke(set_keybind)
        elif choice == 2:
            ctx.invoke(start_overlay)
        else:
            click.echo("Invalid option.")


def set_keybind():
    """Set the keybind by listening for the next key press."""
    if not glfw.init():
        click.echo("Failed to initialize GLFW.")
        return

    window = glfw.create_window(200, 200, "Press a Key", None, None)
    if not window:
        click.echo("Failed to create a window.")
        glfw.terminate()
        return

    glfw.set_window_attrib(window, glfw.FLOATING, True)
    glfw.make_context_current(window)

    def key_callback(window, key, scancode, action, mods):
        if action == glfw.PRESS:
            overlay = Overlay(CONFIG_FILE)
            overlay.save_keybind(key)  # Save key code directly
            click.echo(f"Keybind set to: {glfw.get_key_name(key, scancode)}")
            glfw.set_window_should_close(window, True)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


@cli.command()
def start_overlay():
    """Start the overlay with the current configuration."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = yaml.safe_load(file)  # Safe loading
            if not config:  # Check if the configuration is empty
                raise ValueError("Configuration is empty")
        overlay = Overlay(CONFIG_FILE)
        overlay.run()
    except FileNotFoundError:
        click.echo("No configuration found. Using default settings.")
        overlay = Overlay(DEFAULT_CONFIG)
        overlay.run()
    except ValueError as e:
        click.echo(f"Configuration error: {e}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")


if __name__ == "__main__":
    cli()
