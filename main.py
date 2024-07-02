import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import cv2


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("800x600")

        self.image = None
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Upload Image", command=self.upload_image).pack()
        tk.Button(self.root, text="Capture from Webcam", command=self.capture_image).pack()

        self.channel_var = tk.StringVar(value="None")
        tk.OptionMenu(self.root, self.channel_var, "Red", "Green", "Blue").pack()
        tk.Button(self.root, text="Show Channel", command=self.show_channel).pack()

        tk.Button(self.root, text="Crop Image", command=self.crop_image).pack()
        tk.Button(self.root, text="Enhance Brightness", command=self.enhance_brightness).pack()
        tk.Button(self.root, text="Draw Line", command=self.draw_line).pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        ret, frame = cap.read()
        cap.release()
        if ret:
            self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.display_image(self.image)
        else:
            messagebox.showerror("Error", "Failed to capture image from webcam.")

    def display_image(self, image):
        img_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def show_channel(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        channel = self.channel_var.get()
        channels = self.image.split()
        if channel == "Red":
            self.display_image(channels[0])
        elif channel == "Green":
            self.display_image(channels[1])
        elif channel == "Blue":
            self.display_image(channels[2])
        else:
            messagebox.showerror("Error", "No channel selected.")

    def crop_image(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        coords = simpledialog.askstring("Input", "Enter crop coordinates (x1,y1,x2,y2):")
        if coords:
            try:
                x1, y1, x2, y2 = map(int, coords.split(','))
                cropped = self.image.crop((x1, y1, x2, y2))
                self.display_image(cropped)
            except ValueError:
                messagebox.showerror("Error", "Invalid coordinates.")

    def enhance_brightness(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        value = simpledialog.askfloat("Input", "Enter brightness enhancement value:")
        if value is not None:
            enhancer = ImageEnhance.Brightness(self.image)
            enhanced = enhancer.enhance(value)
            self.display_image(enhanced)

    def draw_line(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        line_params = simpledialog.askstring("Input", "Enter line parameters (x1,y1,x2,y2,width):")
        if line_params:
            try:
                x1, y1, x2, y2, width = map(int, line_params.split(','))
                img_draw = self.image.copy()
                draw = ImageDraw.Draw(img_draw)
                draw.line((x1, y1, x2, y2), fill="green", width=width)
                self.display_image(img_draw)
            except ValueError:
                messagebox.showerror("Error", "Invalid line parameters.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
