import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import cv2


class ImageApp:
    """
    A class to represent the image processing application.

    Attributes:
    root : tk.Tk
        The root window of the Tkinter application.
    image : PIL.Image
        The currently loaded image.
    canvas_frame : tk.Frame
        The frame containing the canvas and scrollbars.
    canvas : tk.Canvas
        The canvas widget for displaying images.
    v_scrollbar : tk.Scrollbar
        The vertical scrollbar for the canvas.
    h_scrollbar : tk.Scrollbar
        The horizontal scrollbar for the canvas.
    image_container : int
        The ID of the image container on the canvas.
    channel_var : tk.StringVar
        The variable to store the selected color channel.
    """

    def __init__(self, root):
        """
        Constructs all the necessary attributes for the ImageApp object.

        Parameters:
        root : tk.Tk
            The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("800x600")

        self.image = None

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg='gray')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=self.h_scrollbar.set)

        self.image_container = self.canvas.create_image(0, 0, anchor=tk.NW)

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and places the widgets on the main window.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(control_frame, text="Upload Image", command=self.upload_image).pack(pady=5)
        tk.Button(control_frame, text="Capture from Webcam", command=self.capture_image).pack(pady=5)

        self.channel_var = tk.StringVar(value="None")
        tk.OptionMenu(control_frame, self.channel_var, "Red", "Green", "Blue").pack(pady=5)
        tk.Button(control_frame, text="Show Channel", command=self.show_channel).pack(pady=5)

        tk.Button(control_frame, text="Crop Image", command=self.crop_image).pack(pady=5)
        tk.Button(control_frame, text="Enhance Brightness", command=self.enhance_brightness).pack(pady=5)
        tk.Button(control_frame, text="Draw Line", command=self.draw_line).pack(pady=5)

    def upload_image(self):
        """
        Uploads an image from the file system and displays it on the canvas.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def capture_image(self):
        """
        Captures an image from the webcam and displays it on the canvas.
        """
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
        """
        Displays the given image on the canvas.

        Parameters:
        image : PIL.Image
            The image to be displayed.
        """
        self.img_tk = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.image_container, image=self.img_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def show_channel(self):
        """
        Displays the selected color channel of the image.
        """
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
        """
        Crops the image based on user input coordinates and displays the cropped image.

        The user is prompted to enter the coordinates (x1, y1, x2, y2).
        """
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        coords = simpledialog.askstring("Input", "Enter crop coordinates (x1,y1,x2,y2):")
        if coords:
            try:
                x1, y1, x2, y2 = map(int, coords.split(','))
                self.image = self.image.crop((x1, y1, x2, y2))
                self.display_image(self.image)
            except ValueError:
                messagebox.showerror("Error", "Invalid coordinates.")

    def enhance_brightness(self):
        """
        Enhances the brightness of the image based on user input value and displays the result.

        The user is prompted to enter the brightness enhancement value.
        """
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        value = simpledialog.askfloat("Input", "Enter brightness enhancement value:")
        if value is not None:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(value)
            self.display_image(self.image)

    def draw_line(self):
        """
        Draws a line on the image based on user input parameters and displays the result.

        The user is prompted to enter the line parameters (x1, y1, x2, y2, width).
        """
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        line_params = simpledialog.askstring("Input", "Enter line parameters (x1,y1,x2,y2,width):")
        if line_params:
            try:
                x1, y1, x2, y2, width = map(int, line_params.split(','))
                draw = ImageDraw.Draw(self.image)
                draw.line((x1, y1, x2, y2), fill="green", width=width)
                self.display_image(self.image)
            except ValueError:
                messagebox.showerror("Error", "Invalid line parameters.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
