from tkinter import ttk
from tkinter import *

import sqlite3


class Product:
    db_name = 'crud.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        frame = LabelFrame(self.wind, text="Register a New Product")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        Label(frame, text="Price: ").grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        ttk.Button(frame, text='Save Product', command=self.add_product).grid(row=3, columnspan=2, sticky=W + E)

        self.message = Label(text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor=CENTER)

        ttk.Button(text='Delete', command=self.delete_product).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='Edit', command=self.show_edit_product).grid(row=5, column=1, sticky=W + E)

        self.get_products()

    def show_message(self, text, color):
        self.message = Label(text='', fg=color)
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
        self.message['text'] = text

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = "SELECT * FROM product ORDER BY name DESC"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = "INSERT INTO product (name, price) VALUES (?,?)"
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.show_message('Product {} added Successfully'.format(self.name.get()), 'green')
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.show_message('Name and Price are required', 'red')
        self.get_products()

    def delete_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            print(e)
            self.show_message('Please select a Product', 'red')
            return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.show_message('Procduct {} deleted Successfully'.format(name), 'green')
        self.get_products()

    def show_edit_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.show_message('Please select a Product', 'red')

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Product"

        # Old Name
        Label(self.edit_wind, text='Old Name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly') \
            .grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='New Name: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        # Old Price
        Label(self.edit_wind, text='Old Price: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly') \
            .grid(row=2, column=2)

        # New Price
        Label(self.edit_wind, text='New Price: ').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_product(new_name.get(), name, new_price.get(),
                                                                                old_price)).grid(row=4, column=2,
                                                                                                 sticky=W)

    def edit_product(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.show_message('Product {} updated Successfully'.format(new_name), 'green')
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
