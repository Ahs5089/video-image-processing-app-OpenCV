import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk

# Function to apply convolution effects
def apply_convolution(image, kernel):
    return cv2.filter2D(image, -1, kernel)

# GUI for selecting image and applying effects
def main():
    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            img = cv2.imread(file_path)
            display_image(img, original=True)
            global current_image, processed_image
            current_image = img
            processed_image = None  # Reset processed image

    def display_image(img, original=False):
        # Resize image to larger dimensions
        fixed_width, fixed_height = 600, 450  # Updated size
        height, width = img.shape[:2]
        scaling_factor = min(fixed_width / width, fixed_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Convert to RGB for display
        img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        if original:
            original_panel.configure(image=img)
            original_panel.image = img
        else:
            processed_panel.configure(image=img)
            processed_panel.image = img

    def process_image(effect):
        global processed_image
        if current_image is not None:
            if effect == "Box Blur":
                kernel = np.ones((5, 5), np.float32) / 25
            elif effect == "Gaussian Blur":
                processed_image = cv2.GaussianBlur(current_image, (15, 15), 0)
                display_image(processed_image)
                return
            elif effect == "Edge Detection":
                processed_image = cv2.Canny(current_image, 100, 200)
                display_image(processed_image)
                return
            elif effect == "Sharpen":
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            else:
                return
            processed_image = apply_convolution(current_image, kernel)
            display_image(processed_image)

    def save_image():
        if processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG files", "*.jpg"),
                                                                ("PNG files", "*.png"),
                                                                ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, processed_image)
                messagebox.showinfo("Image Saved", "The processed image has been saved successfully!")
        else:
            messagebox.showwarning("No Processed Image", "Please process an image before saving.")

    root = Tk()
    root.title("Image Processing")
    root.geometry("1200x700")  # Increased window size for larger images

    # Layout
    control_frame = tk.Frame(root)
    control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    btn_open = tk.Button(control_frame, text="Open Image", command=open_file)
    btn_open.grid(row=0, column=0, padx=5, pady=5)

    btn_box_blur = tk.Button(control_frame, text="Box Blur", command=lambda: process_image("Box Blur"))
    btn_box_blur.grid(row=1, column=0, padx=5, pady=5)

    btn_gaussian_blur = tk.Button(control_frame, text="Gaussian Blur", command=lambda: process_image("Gaussian Blur"))
    btn_gaussian_blur.grid(row=2, column=0, padx=5, pady=5)

    btn_edge = tk.Button(control_frame, text="Edge Detection", command=lambda: process_image("Edge Detection"))
    btn_edge.grid(row=3, column=0, padx=5, pady=5)

    btn_sharpen = tk.Button(control_frame, text="Sharpen", command=lambda: process_image("Sharpen"))
    btn_sharpen.grid(row=4, column=0, padx=5, pady=5)

    btn_save = tk.Button(control_frame, text="Save Processed Image", command=save_image)
    btn_save.grid(row=5, column=0, padx=5, pady=5)

    # Panels for displaying images
    image_frame = tk.Frame(root)
    image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    original_label = tk.Label(image_frame, text="Original Image")
    original_label.grid(row=0, column=0, padx=10, pady=10)

    original_panel = tk.Label(image_frame, width=600, height=450, relief="groove")
    original_panel.grid(row=1, column=0, padx=10, pady=10)

    processed_label = tk.Label(image_frame, text="Processed Image")
    processed_label.grid(row=0, column=1, padx=10, pady=10)

    processed_panel = tk.Label(image_frame, width=600, height=450, relief="groove")
    processed_panel.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    current_image = None
    processed_image = None
    main()
