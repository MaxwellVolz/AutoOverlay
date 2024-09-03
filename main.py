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

# Constants
TOGGLE_KEY = glfw.KEY_KP_6  # Numpad 6 key

# Global variables
image_visibility = True
texture_id = None


# Key callback
def key_callback(window, key, scancode, action, mods):
    global image_visibility
    if key == TOGGLE_KEY and action == glfw.PRESS:
        image_visibility = not image_visibility
        print(f"Image visibility toggled: {image_visibility}")


# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a windowed mode window with OpenGL context, no window header
glfw.window_hint(glfw.DECORATED, False)  # No window header
glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
window = glfw.create_window(800, 600, "Overlay", None, None)
glfw.set_window_attrib(window, glfw.FLOATING, True)  # Always on top
glfw.make_context_current(window)

# Set clear color to fully transparent
glClearColor(0, 0, 0, 0)  # Full transparency

# Enable alpha blending
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# Load image using Pillow and create texture
def load_texture(path):
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


texture_id, img_width, img_height = load_texture("assets/test.png")

# Set the key callback
glfw.set_key_callback(window, key_callback)

# Main loop
while not glfw.window_should_close(window):
    # Clear only the color buffer (with transparent background)
    glClear(GL_COLOR_BUFFER_BIT)

    if image_visibility:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBegin(GL_QUADS)
        glColor4f(1, 1, 1, 1)  # Set color to white (no tinting)

        # Map the texture coordinates and vertices
        glTexCoord2f(0, 0)
        glVertex2f(-0.5 * img_width / 800, -0.5 * img_height / 600)  # Bottom-left

        glTexCoord2f(1, 0)
        glVertex2f(0.5 * img_width / 800, -0.5 * img_height / 600)  # Bottom-right

        glTexCoord2f(1, 1)
        glVertex2f(0.5 * img_width / 800, 0.5 * img_height / 600)  # Top-right

        glTexCoord2f(0, 1)
        glVertex2f(-0.5 * img_width / 800, 0.5 * img_height / 600)  # Top-left

        glEnd()

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

glfw.terminate()
