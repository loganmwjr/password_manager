from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(5, 8))]

    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters

    random.shuffle(password_list)

    password = ''.join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get()
    password = password_entry.get()
    email = email_username_entry.get()
    data_dict = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(password) < 1 or len(website) < 1 or len(email) < 1:
        messagebox.askretrycancel(title='retry', message='please leave no boxes empty')

    try:

        with open('data.json', 'r') as data_file:

            data = json.load(data_file)

    except(FileNotFoundError, json.decoder.JSONDecodeError):

        with open('data.json', 'w') as data_file:

            json.dump(data_dict, data_file, indent=4)

    else:

        data.update(data_dict)

        with open('data.json', 'w') as data_file:

            json.dump(data, data_file, indent=4)

    finally:

        website_entry.delete(0, END)

        password_entry.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #


def search_passwords():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title='error', message="please enter a website")
    else:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            messagebox.askretrycancel(title="error", message='There is no data.')

        else:
            if website in data:
                email = data[website]['email']
                password = data[website]['password']
                messagebox.showinfo(title=website, message=f'email: {email} \n password: {password}')

            else:
                messagebox.showinfo(title="error", message=f'there is no data on {website}')





# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

email_username_label = Label(text='Email/Username:')
email_username_label.grid(column=0, row=2)

password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1,sticky='ew')
website_entry.focus()

email_username_entry = Entry(width=21)
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_username_entry.insert(0, 'loganmwjr@outlook.com')

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky='EW')

# buttons
search_button = Button(text="Search", command=search_passwords)
search_button.grid(column=2, row=1, sticky="EW")
generate_button = Button(text='generate password', command=password_gen)
generate_button.grid(column=2, row=3)

add_button = Button(text='add', width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
