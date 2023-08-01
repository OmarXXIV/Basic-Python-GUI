# The three files work together
# In order from login.py, cropping.py, then checkout.py
# Each file must be within the same directory in order to work


# login.py
# This file consist of the code need for the user login,
# if the user does not have an account the will make a username and password
# then clock click create.
# this will then tell them they have successfully created the account and move them over to the
# cropping window
# This file consist of the following imports

# import tkinter as tk
# from tkinter import filedialog  # is tk_file
# from PIL import Image, ImageTk
# import customtkinter as ctk
# import subprocess
# import sys

# cropping.py
# this file allows the user to crop the image they insert.
# if the image is not to their liking, they may reset.
# once to their liking they can add it to their cart then click "CheckOut"
# which will bring them to the checkout file
# This file consist of the following imports

# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# import customtkinter as ctk
# import subprocess
# import sys

# checkout.py
# The checkout file shows the user of the image they edited inthe left frame,
# the in the right frame they will see text boxes where they will be prompted to
# insert the card name, card number, expiration date, and cvv
# but this will not work if the quantity in the left frame is zero because then
# there would be nothing to purchase. but one all requirements are met, and they hit checkout,
# a download button will appear, then their purchase will be successful and they can download their cropped images.
