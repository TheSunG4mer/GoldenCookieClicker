from time import time
from PIL import ImageGrab, Image
import numpy as np
# Capture the entire screen

def grab_second_screen():
    screen_size = (1920, 1080)
    # Capture the second screen
    screenshot = ImageGrab.grab(bbox = None, include_layered_windows=False, all_screens=True)
    total_size = screenshot.size
    bbox = (0, total_size[1] - screen_size[1], screen_size[0], total_size[1])
    screenshot = screenshot.resize(size = screen_size, box = bbox)
    return screenshot

screenshot = grab_second_screen()
print(screenshot.size)
assert isinstance(screenshot, Image.Image)

pix = np.array(screenshot)

print(pix.shape)
print(pix.dtype)
print(pix[:10, :10, 0])

# Save the screenshot to a file
screenshot.save("screenshot.png")

# Close the screenshot
screenshot.close()
