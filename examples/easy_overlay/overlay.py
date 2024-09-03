import glfw
from OpenGL.GL import (
    glClear,
    glUseProgram,
    glBindVertexArray,
    glDrawElements,
    GL_TRIANGLES,
    GL_UNSIGNED_INT,
    glGenTextures,
    glBindTexture,
    glTexImage2D,
    glGenerateMipmap,
    GL_TEXTURE_2D,
    GL_RGBA,
    GL_UNSIGNED_BYTE,
    glEnableVertexAttribArray,
    glVertexAttribPointer,
    glGenVertexArrays,
    glBindBuffer,
    glGenBuffers,
    glBufferData,
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    GL_FALSE,
    GL_TRUE,
    GL_FLOAT,
    glTexParameteri,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    GL_CLAMP_TO_EDGE,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    glGetAttribLocation,
    glDrawArrays,
    GL_TRIANGLE_FAN,
    glClearColor,
    GL_BLEND,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    glBlendFunc,
    glEnable,
)


from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image
import numpy as np

import ctypes
from ctypes import wintypes

# Define necessary constants from the Windows API
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20

# Load User32.dll and define required functions
user32 = ctypes.WinDLL("user32", use_last_error=True)
SetWindowLongPtr = user32.SetWindowLongPtrW
SetWindowLongPtr.restype = ctypes.c_long
SetWindowLongPtr.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]


VERTEX_SHADER = """
#version 330
in vec2 position;
in vec2 texCoords;
out vec2 st;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    st = texCoords;
}
"""

FRAGMENT_SHADER = """
#version 330
in vec2 st;
out vec4 outColor;
uniform sampler2D texture1;
void main() {
    outColor = texture(texture1, st);
}
"""


# Function to modify window style
def set_window_transparent(hwnd):
    styles = user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    new_styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT
    SetWindowLongPtr(hwnd, GWL_EXSTYLE, new_styles)


# Updated to position the image specifically on the screen
def calculate_vertices(center_x, center_y, width, height, screen_width, screen_height):
    # Normalize the coordinates to the OpenGL coordinate system
    half_width = width / screen_width * 2
    half_height = height / screen_height * 2
    left = center_x / screen_width * 2 - 1 - half_width
    right = center_x / screen_width * 2 - 1 + half_width
    top = 1 - center_y / screen_height * 2 - half_height
    bottom = 1 - center_y / screen_height * 2 + half_height

    # Counter-clockwise starting from bottom-left corner
    return np.array(
        [
            left,
            bottom,
            0.0,
            0.0,  # Bottom-left
            right,
            bottom,
            1.0,
            0.0,  # Bottom-right
            right,
            top,
            1.0,
            1.0,  # Top-right
            left,
            top,
            0.0,
            1.0,  # Top-left
        ],
        dtype=np.float32,
    )


def load_texture(image_path="assets/cigs.png"):
    image = Image.open(image_path)

    image = image.resize((500, 500))

    image_data = image.convert("RGBA").tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
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
    glBindTexture(GL_TEXTURE_2D, 0)

    return texture


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.DECORATED, False)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.FLOATING, True)
    window = glfw.create_window(1920, 1080, "Overlay", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
    )

    vertices = calculate_vertices(
        960, 540, 500, 500, 1920, 1080
    )  # Example: center of screen, 500x500 size

    # vertices = np.array(
    #     [-1, -1, 0, 0, 1, -1, 1, 0, 1, 1, 1, 1, -1, 1, 0, 1], dtype=np.float32
    # )

    glClearColor(0, 0, 0, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))

    texCoords = glGetAttribLocation(shader, "texCoords")
    glEnableVertexAttribArray(texCoords)
    glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))

    texture = load_texture("assets/cigs.png")
    glBindTexture(GL_TEXTURE_2D, texture)

    # Get the native Win32 window handle
    hwnd = glfw.get_win32_window(window)

    # Set window styles for transparency and mouse passthrough
    set_window_transparent(hwnd)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
