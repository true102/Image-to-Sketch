import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time

# Function to load an image
def load_image():
    global image_path, original_image
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        original_image = cv2.imread(image_path)
        display_image(original_image, original_label)

# Function to convert the image to a sketch
def convert_to_sketch():
    if 'original_image' in globals():
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(invert, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        display_image(sketch, sketch_label)
        
        # Save the sketch with a unique name
        timestamp = int(time.time())  # Use a timestamp for uniqueness
        sketch_name = f"sketch_output_{timestamp}.jpg"
        cv2.imwrite(sketch_name, sketch)
        print(f"Sketch saved as {sketch_name}")

# Function to display an image in the Tkinter window
def display_image(image, label):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if len(image.shape) == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = Image.fromarray(image)
    image.thumbnail((400, 400))  # Resize image to fit in the window
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Initialize the Tkinter window
root = tk.Tk()
root.title("Image to Sketch Converter - Improved Version")

# Set the window size to medium (800x600)
root.geometry("800x600")

# Create buttons for loading and converting images
load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)

convert_button = tk.Button(root, text="Convert to Sketch", command=convert_to_sketch)
convert_button.pack(pady=10)

# Labels to display the original and sketch images
original_label = tk.Label(root)
original_label.pack(side=tk.LEFT, padx=10)

sketch_label = tk.Label(root)
sketch_label.pack(side=tk.RIGHT, padx=10)

# Run the Tkinter event loop
root.mainloop()