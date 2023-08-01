import re
import customtkinter as ctk
from datetime import date
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# global variables
subtotal = 0
copies = 1


def validate_card_info(card_number, card_holder, expiration_date, cvv):
    todays_date = date.today()
    todays_date = todays_date.strftime("%m/%y")
    if not card_number or not card_holder or not expiration_date or not cvv or not card_holder:
        return "Please fill all fields"
    if len(card_number) != 16:
        return "Card number must be 16 digits."
    if not card_holder.replace(" ", "").isalpha():
        return "Card holder name should only contain letters."
    if not len(cvv) in [3, 4]:
        return "CVV must be 3 digits on VISA®, MasterCard® and Discover® or 4 On your American Express®"
    if str(expiration_date) <= str(todays_date):
        return "Your card is expired"
    if not re.match(r'^[a-zA-Z\s]+$', card_holder):
        return "Card holder name should only contain letters."
    return ''


# Function to handle the checkout process
def checkout():
    # Retrieve the entered debit card information
    card_number = card_number_entry.get()
    card_holder = card_holder_entry.get()
    expiration_date = expiration_date_entry.get()
    cvv = cvv_entry.get()

    validation_message = validate_card_info(card_number, card_holder, expiration_date, cvv)
    if validation_message:
        message_label.configure(text=validation_message, text_color="red")
    else:
        message_label.configure(text="Payment successful!", font=("Helvetica", 12), text_color="green")
        message_label.after(700, lambda: message_label.destroy())
        checkout_button.after(700, lambda: checkout_button.destroy())

        download_button = ctk.CTkButton(right_frame, text='Download', command=download)
        download_button.after(700, lambda: download_button.pack(pady=10))


def download():
    global copies
    image = Image.open("edited_image.png")

    for i in range(1, copies + 1):
        image_name = f"edited_image{i}.png"
        save_filename = filedialog.asksaveasfilename(defaultextension=".png", initialfile=image_name)
        if save_filename:
            image.save(save_filename)
    if copies > 0:
        new_message_label = ctk.CTkLabel(right_frame, text="Image downloaded and saved successfully!",
                                         text_color="green")
    else:
        new_message_label = ctk.CTkLabel(right_frame, text="No images downloaded.", text_color="red")
    new_message_label.pack(pady=10)
    new_message_label.after(2000, lambda: new_message_label.destroy())


def get_subtotal(event=None):
    global subtotal, copies
    try:
        copies = int(quantity_box.get())
        subtotal = round((copies * 4.99), 2)
        subtotal_label.configure(text=f'SubTotal: {subtotal}')
        total_label.configure(text=f'SubTotal: {round(subtotal + (subtotal * .07), 2)}')
    except ValueError:
        subtotal_label.configure(text='SubTotal: 0.00')
        total_label.configure(text='SubTotal: 0.00')


root = ctk.CTk()
root.title('CheckOut')
root.geometry("1000x600")

# Create a frame for the left half
left_frame = ctk.CTkFrame(root, width=500, height=600)
left_frame.pack(side='left', fill='both', expand=True)

# Create a frame for the right half
right_frame = ctk.CTkFrame(root, width=500, height=600)
right_frame.pack(side='left', fill='both', expand=True)

card_holder_label = ctk.CTkLabel(right_frame, text="Card Holder:")
card_holder_label.pack()
card_holder_entry = ctk.CTkEntry(right_frame, placeholder_text='First MI Last')
card_holder_entry.pack(pady=5)

card_number_label = ctk.CTkLabel(right_frame, text="Card Number:")
card_number_label.pack()
card_number_entry = ctk.CTkEntry(right_frame, placeholder_text='16 digits')
card_number_entry.pack(pady=5)

# Create and pack the expiration date entry
expiration_date_label = ctk.CTkLabel(right_frame, text="Expiration Date:")
expiration_date_label.pack()
expiration_date_entry = ctk.CTkEntry(right_frame, placeholder_text='MMYY')
expiration_date_entry.pack(pady=5)

# Create and pack the CVV entry
cvv_label = ctk.CTkLabel(right_frame, text="CVV:")
cvv_label.pack()
cvv_entry = ctk.CTkEntry(right_frame, placeholder_text='3-4 digits')
cvv_entry.pack(pady=5)

# Create the label to display the message
message_label = ctk.CTkLabel(right_frame, text="")
message_label.pack(pady=10)

# Create the checkout button
checkout_button = ctk.CTkButton(right_frame, text="Checkout", command=checkout)
checkout_button.pack(pady=10)

# image
# edited_image = ImageTk.PhotoImage(Image.open("edited_image.png"))
edited_image = Image.open("edited_image.png")
resized = edited_image.resize((100, 100))
edited_image2 = ImageTk.PhotoImage(resized)

# holds the image label, and sits in our left frame
image_frame = ctk.CTkFrame(left_frame, width=100, height=100)
image_frame.grid(row=0, column=0, sticky='nw', pady=10, padx=10)

# holds our image
image_label = tk.Label(image_frame, width=96, height=80, image=edited_image2)
image_label.pack(fill=tk.BOTH)

# text
images_text_label = ctk.CTkLabel(left_frame, text='Cropped Image', height=5)
images_text_label.grid(row=0, column=1, sticky='nw', pady=10, padx=10)

quantity_label = ctk.CTkLabel(left_frame, text='Quantity: ')
quantity_label.grid(row=0, column=1, sticky='nw', pady=30, padx=10)

quantity_box = ctk.CTkEntry(left_frame, placeholder_text='1', width=35, justify='center')
quantity_box.grid(row=0, column=1, sticky='nw', pady=30, padx=65)
quantity_box.bind("<KeyRelease>", get_subtotal)

subtotal_label = ctk.CTkLabel(left_frame, text='SubTotal: 4.99')
subtotal_label.grid()

total_label = ctk.CTkLabel(left_frame, text=f'Total: {round(4.99 + (4.99 * .07), 2)}')
total_label.grid()

root.mainloop()
