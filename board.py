from tkinter import Canvas, Tk, Button, Label
from PIL import Image, ImageDraw
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

class EditableWhiteboard:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.prev_x = None
        self.prev_y = None

        self.image = Image.new("L", (width, height), color=255)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = Canvas(root, width=width, height=height, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

        save_button = Button(root, text="Save", command=self.save_whiteboard)
        save_button.pack()

        clear_button = Button(root, text="Clear", command=self.clear_whiteboard)
        clear_button.pack()

        guess_button = Button(root, text="Guess", command=self.guess)
        guess_button.pack()

    def draw_on_canvas(self, event):
        if self.prev_x is not None and self.prev_y is not None:
            x1, y1 = self.prev_x, self.prev_y
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=9)
            self.draw.line([x1, y1, x2, y2], fill="black", width=9)

        self.prev_x = event.x
        self.prev_y = event.y

    def clear_whiteboard(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.width, self.height), color=255)
        self.draw = ImageDraw.Draw(self.image)

    def save_whiteboard(self):
        resized_image = self.image.resize((28, 28))

        resized_image.save("digit.png")

    def guess(self):
        model = tf.keras.models.load_model('handwritten.model')

        try:
            img = cv2.imread("digit.png")[:,:,0]
            img = np.invert(np.array([img]))
            prediction = model.predict(img)
            print(f"This digit is probably a {np.argmax(prediction)}")
            plt.imshow(img[0], cmap=plt.cm.binary)

            guess_label = Label(root, text="")
            guess_label.pack()

            guess_label.config(text=f"The number could be: {np.argmax(prediction)}")
            # plt.show()
        except:
            print("Error!")

if __name__ == "__main__":
    width, height = 400, 400

    root = Tk()
    root.title("Editable Whiteboard")

    whiteboard = EditableWhiteboard(root, width, height)

    root.mainloop()
