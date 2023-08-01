import tkinter as tk
from tkinter import filedialog  # is tk_file
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess
import sys

# Global variables
opened_image = ''
image_path = ''
edited_image = ''
original_image = ''
image_height = 0
image_width = 0
edited_image_width = 0
edited_image_height = 0
save_edited_image = ''


def add_image():
    global image_width, image_height, image_path, opened_image, edited_image_width, edited_image_height

    # allow user to select image and stores it in image path
    image_path = filedialog.askopenfilename()

    if image_path:
        # opened_image is updated with the image
        # which allows it to be displayed in the application.
        opened_image = ImageTk.PhotoImage(Image.open(image_path))

        # this is configured to display the opened image
        image_lb.config(image=opened_image)

    # these are updated with the height and width of the opened_image
    image_height = opened_image.height()
    image_width = opened_image.width()
    edited_image_width = opened_image.width()
    edited_image_height = opened_image.height()


def open_checkout():
    if in_cart.cget('text') == 'Cart Was Updated':
        subprocess.Popen(['python', 'checkout.py'])
        sys.exit()  # Exit the script after opening the cropping script
    else:
        in_cart.configure(text='Cart is empty', text_color='red')
        in_cart.after(500, lambda: in_cart.configure(text='Currently in cart: 0', text_color='white'))


def crop_image(left, top, right, bottom):
    global edited_image, opened_image, edited_image_width, edited_image_height

    edit_img = Image.open(image_path)

    edited_image = edit_img.crop((left, top, image_width - right, image_height - bottom))

    opened_image = ImageTk.PhotoImage(edited_image)
    image_lb.config(image=opened_image)

    edited_image_width = edited_image.width
    edited_image_height = edited_image.height

    # checkout_image.save(edited_image)


def sliders(w, h):
    global opened_image
    if opened_image != '':

        controls = tk.Toplevel(root)
        controls.geometry('400x300')

        left_lb = tk.Label(controls, text="Left")
        left_lb.pack(anchor=tk.W, pady=5)

        left_scale = tk.Scale(controls, from_=0, to=w, orient=tk.HORIZONTAL,
                              command=lambda x: crop_image(
                                  left_scale.get(), top_scale.get(),
                                  right_scale.get(), bottom_scale.get()
                              ))
        left_scale.pack(anchor=tk.W, fill=tk.X)

        right_lb = tk.Label(controls, text="Right")
        right_lb.pack(anchor=tk.W, pady=5)

        right_scale = tk.Scale(controls, from_=0, to=w, orient=tk.HORIZONTAL,
                               command=lambda x: crop_image(
                                   left_scale.get(), top_scale.get(),
                                   right_scale.get(), bottom_scale.get()
                               ))
        right_scale.pack(anchor=tk.W, fill=tk.X)

        top_lb = tk.Label(controls, text='Top')
        top_lb.pack(anchor=tk.W, pady=5)

        top_scale = tk.Scale(controls, from_=0, to=h, orient=tk.HORIZONTAL,
                             command=lambda x: crop_image(
                                 left_scale.get(), top_scale.get(),
                                 right_scale.get(), bottom_scale.get()
                             ))
        top_scale.pack(anchor=tk.W, fill=tk.X)

        bottom_lb = tk.Label(controls, text='Bottom')
        bottom_lb.pack(anchor=tk.W, pady=5)

        bottom_scale = tk.Scale(controls, from_=0, to=h, orient=tk.HORIZONTAL,
                                command=lambda x: crop_image(
                                    left_scale.get(), top_scale.get(),
                                    right_scale.get(), bottom_scale.get()
                                ))
        bottom_scale.pack(anchor=tk.W, fill=tk.X)

        controls.mainloop()
    else:
        sliders_button.configure(text_color='red', text='Nothing to crop')
        sliders_button.after(500, lambda: sliders_button.configure(text_color='white', text='Crop'))


def reset_image():
    global edited_image, image_lb, image_height, image_width, image_path, original_image
    if edited_image != '':
        original_image = ImageTk.PhotoImage(Image.open(image_path))
        image_lb.config(image=original_image)
        image_height = original_image.height()
        image_width = original_image.width()
    else:
        reset_button.configure(text_color='red', text='Nothing to Reset')
        reset_button.after(500, lambda: reset_button.configure(text='Reset', text_color='white'))


def add_cart():
    global save_edited_image
    # if opened image is not blank do this
    if (image_width != edited_image_width) or (image_height != edited_image_height):
        # saved_images.append(edited_image)
        in_cart.configure(text=f"Cart Was Updated", text_color='green')
        in_cart.after(500, lambda: in_cart.configure(text='Cart Was Updated', text_color='white'))
        cost_label.configure(text=f"Cost: {round(4.99 * 1, 2):.2f}")
        save_edited_image = edited_image.save('edited_image.png')

    elif (image_width == edited_image_width) and (image_height == edited_image_height):
        in_cart.configure(text='No Changes Made', text_color='red')
        in_cart.after(500, lambda: in_cart.configure(text='Currently in cart: 0', text_color='white'))
    # otherwise if no image was added this happens
    else:
        add_to_cart_button.configure(text_color='red', text='Add a Image')
        add_to_cart_button.after(500, lambda: add_to_cart_button.configure(text_color='white', text='+ Cart'))


# def save_image():
#     if image_path:
#         file_name = filedialog.asksaveasfilename()
#         if file_name:
#             # Check if the file name has an extension
#             if not file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#                 file_name += '.png'  # Default to PNG format if no extension is provided
#
#             edited_image.save(file_name)


root = ctk.CTk()
root.geometry("1000x600")
root.title("Image Drawing Tool")
root.config(bg='white')

padY = 10

# frame 1
left_frame = ctk.CTkFrame(root, width=200, height=600)
left_frame.pack(side="left", fill="y")

image_lb = tk.Label(root, bg='white', width=750, height=600)
image_lb.pack(fill=tk.BOTH)

image_button = ctk.CTkButton(left_frame, width=50, text="Add Image", command=add_image)
image_button.pack(pady=padY)

sliders_button = ctk.CTkButton(left_frame, width=50, text="Crop",
                               command=lambda: sliders(w=image_width, h=image_height))
sliders_button.pack(pady=padY, padx=50)

reset_button = ctk.CTkButton(left_frame, width=50, text='Reset Image', command=reset_image)
reset_button.pack(pady=padY)

add_to_cart_button = ctk.CTkButton(left_frame, width=50, text='+ Cart', command=add_cart)
add_to_cart_button.pack(pady=padY)

go_to_checkout_button = ctk.CTkButton(left_frame, width=50, text='CheckOut', command=open_checkout)
go_to_checkout_button.pack(pady=padY)

in_cart = ctk.CTkLabel(left_frame, text=f'Currently in cart: 0')
in_cart.pack(pady=padY)

cost_label = ctk.CTkLabel(left_frame, text='Cost: 0.00')
cost_label.pack(pady=padY)

# download_button = ctk.CTkButton(left_frame, text='Download', command=save_image)
# download_button.pack(pady=10)

root.mainloop()
