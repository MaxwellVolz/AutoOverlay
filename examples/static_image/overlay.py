import glfw
from OpenGL.GL import (
    glClear,
    glClearColor,
    glBegin,
    glEnd,
    glVertex2f,
    glTexCoord2f,
    glColor4f,
    GL_COLOR_BUFFER_BIT,
    GL_QUADS,
    glEnable,
    glBindTexture,
    glTexImage2D,
    glTexParameteri,
    glGenTextures,
    GL_TEXTURE_2D,
    GL_RGBA,
    GL_UNSIGNED_BYTE,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    glBlendFunc,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_BLEND,
)
from PIL import Image
import json


class Overlay:
    def __init__(self, config_file="config.json"):
        self.image_visibility = True
        self.texture_id = None
        self.config_file = config_file
        self.keybind = self.load_keybind()

    def load_keybind(self):
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
                return config.get("keybind", glfw.KEY_KP_6)  # Default to Numpad 6
        except FileNotFoundError:
            return glfw.KEY_KP_6

    def save_keybind(self, key):
        with open(self.config_file, "w") as f:
            json.dump({"keybind": key}, f)
        self.keybind = key

    def key_callback(self, window, key, scancode, action, mods):
        if key == self.keybind and action == glfw.PRESS:
            self.image_visibility = not self.image_visibility
            print(f"Image visibility toggled: {self.image_visibility}")

    def load_texture(self, path):
        image = Image.open(path)
        image = image.convert("RGBA")

        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.resize((500, 500))

        image_data = image.tobytes()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            image.width,
            image.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )

        return texture_id, image.width, image.height

    def run(self):
        if not glfw.init():
            raise Exception("GLFW can't be initialized")

        glfw.window_hint(glfw.DECORATED, False)  # No window header
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        window = glfw.create_window(800, 600, "Overlay", None, None)
        glfw.set_window_attrib(window, glfw.FLOATING, True)  # Always on top
        glfw.make_context_current(window)

        glClearColor(0, 0, 0, 0)  # Full transparency

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.texture_id, img_width, img_height = self.load_texture("assets/test.png")

        glfw.set_key_callback(window, self.key_callback)

        while not glfw.window_should_close(window):
            glClear(GL_COLOR_BUFFER_BIT)

            if self.image_visibility:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)

                glBegin(GL_QUADS)
                glColor4f(1, 1, 1, 1)

                glTexCoord2f(0, 0)
                glVertex2f(-0.5 * img_width / 800, -0.5 * img_height / 600)

                glTexCoord2f(1, 0)
                glVertex2f(0.5 * img_width / 800, -0.5 * img_height / 600)

                glTexCoord2f(1, 1)
                glVertex2f(0.5 * img_width / 800, 0.5 * img_height / 600)

                glTexCoord2f(0, 1)
                glVertex2f(-0.5 * img_width / 800, 0.5 * img_height / 600)

                glEnd()

            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()
