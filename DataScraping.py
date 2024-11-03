from time import sleep, time
from PIL import ImageGrab, Image
import keyboard
import numpy as np
import tkinter as tk
from keyboard import is_pressed

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

def mean_pool(image, pool_size):
    """
    Downsamples an image by taking the mean value of each pool_size x pool_size block.
    Args:
        image (numpy.ndarray): The image to be downsampled.
        pool_size (int): The size of the pooling window.
    Returns:
        numpy.ndarray: The downsampled image.
    """
    h, w, d = image.shape
    new_h = h // pool_size
    new_w = w // pool_size
    pooled_image = np.zeros((new_h, new_w, d), dtype = np.uint8)
    for i in range(d):
        for j in range(new_h):
            for k in range(new_w):
                pooled_image[j, k, i] = np.mean(image[j * pool_size:(j + 1) * pool_size, k * pool_size:(k + 1) * pool_size, i])

    return pooled_image


def save_data(data, filename):
    """
    Saves the data to a file.
    Args:
        data (numpy.ndarray): The data to be saved.
        filename (str): The name of the file to save the data to.
    """
    if len(data) > 1:
        data = data.reshape(1, -1)
    prev_data = load_data(filename)
    assert isinstance(prev_data, np.ndarray), "The data loaded from the file is not a numpy array."
    data_to_save = np.append(prev_data, data)
    np.save(filename, data_to_save)

def load_data(filename):
    """
    Loads the data from a file.
    Args:
        filename (str): The name of the file to load the data from.
    Returns:
        numpy.ndarray: The loaded data.
    """
    return np.load(filename)


def initialize_data(filename, data):
    """
    Initializes the data file.
    Args:
        filename (str): The name of the file to initialize.
    """
    np.save(filename, data)

def initialize_files():
    """
    Initializes the necessary data files for the application.

    This function creates two files, 'features.npy' and 'results.npy', 
    and initializes them with empty numpy arrays. The 'features.npy' 
    file is initialized with a 2D empty array, while the 'results.npy' 
    file is initialized with a 1D empty array.

    Note:
        This function assumes that the `initialize_data` function and 
        the `np` (numpy) module are already defined and imported in the 
        script.

    Raises:
        Any exceptions raised by the `initialize_data` function will 
        propagate through this function.
    """
    initialize_data('features.npy', np.array([[]]))
    initialize_data('results.npy', np.array([]))


def capture_and_save_data():
    screenshot = grab_second_screen() # Capture the entire second screen
    pix = np.array(screenshot) # Convert the image to a numpy array
    pooled_pix = pix.flatten() # mean_pool(pix, 3) # Downsample the image by taking the mean value of each 3x3 block
    save_data(pooled_pix, 'features.npy') # Save the downsampled image to a file

def launch_data_saver_window():
    """
    Opens a Tkinter window with buttons to save different types of data.
    The window contains three buttons:
    - "Empty": Saves an array with a single element [0] to 'results.npy' and closes the window.
    - "Golden Cookie": Saves an array with a single element [1] to 'results.npy' and closes the window.
    - "Effect": Saves an array with a single element [2] to 'results.npy' and closes the window.
    The function uses the `save_data` function to save the data and `numpy` for array creation.
    """
    root = tk.Tk()
    root.title("Golden Cookie Clicker")

    def on_empty():
        save_data(np.array([0]), 'results.npy')
        root.quit()

    def on_golden_cookie():
        save_data(np.array([1]), 'results.npy')
        root.quit()

    def on_effect():
        save_data(np.array([2]), 'results.npy')
        root.quit()

    save_button = tk.Button(root, text="Empty", command=on_empty)
    save_button.pack(pady=10)

    load_button = tk.Button(root, text="Golden Cookie", command=on_golden_cookie)
    load_button.pack(pady=10)

    exit_button = tk.Button(root, text="Effect", command=on_effect)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    #initialize_files()
    while True:
        if keyboard.read_key() == 'e':
            print("Capturing and saving data - Empty screen")
            capture_and_save_data()
            save_data(np.array([0]), 'results.npy')
            print("Data saved")
            sleep(1)
            print("Ready to capture more data")
        elif keyboard.read_key() == 'g':
            print("Capturing and saving data - Golden Cookie")
            capture_and_save_data()
            save_data(np.array([1]), 'results.npy')
            print("Data saved")
            sleep(1)
            print("Ready to capture more data")
        elif keyboard.read_key() == 'f':
            print("Capturing and saving data - Effect")
            capture_and_save_data()
            save_data(np.array([2]), 'results.npy')
            print("Data saved")
            sleep(1)
            print("Ready to capture more data")
        elif keyboard.read_key() == 'q':
            print("Quitting the application")
            break

