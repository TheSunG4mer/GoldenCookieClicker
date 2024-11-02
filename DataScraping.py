from time import time
from PIL import ImageGrab, Image
import numpy as np

def grab_second_screen():
    """
    Captures a screenshot of the second screen and resizes it to the specified screen size.
    The function assumes a dual-monitor setup and captures the entire screen area, then crops 
    and resizes the image to match the dimensions of the second screen.
    Returns:
        PIL.Image.Image: A resized screenshot of the second screen.
    """

    screen_size = (1920, 1080)
    # Capture the second screen
    screenshot = ImageGrab.grab(bbox = None, include_layered_windows=False, all_screens=True)
    total_size = screenshot.size
    bbox = (0, total_size[1] - screen_size[1], screen_size[0], total_size[1])
    
    screenshot = screenshot.resize(size = screen_size, box = bbox)
    return screenshot


def save_data(data, filename):
    """
    Saves the data to a file.
    Args:
        data (numpy.ndarray): The data to be saved.
        filename (str): The name of the file to save the data to.
    """
    np.save(filename, data)

def load_data(filename):
    """
    Loads the data from a file.
    Args:
        filename (str): The name of the file to load the data from.
    Returns:
        numpy.ndarray: The loaded data.
    """
    return np.load(filename)

screenshot = grab_second_screen() # Capture the entire second screen

pix = np.array(screenshot).flatten() # Convert the image to a numpy array

save_data(pix, "screenshot.npy") # Save the screenshot to a file
save_data(pix, "screenshot.npy") # Save the size of the screenshot to a file

data = load_data("screenshot.npy") # Load the data from the file

print(data.shape)