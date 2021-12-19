import tkinter
from tkinter import *
import sqlite3  # this imports SQL light

root = Tk()
root.title("Database Project")
root.geometry("650x400")


# CREATE TABLE but only want to create it once
# create a database or connect to one
# connection1 = sqlite3.connect('address_book.db')  # will save database in directory if doesn't exist
# cursor1 = connection1.cursor()  # create a cursor
# cursor1.execute("""CREATE TABLE addresses(
#                     first_name text,
#                   last_name text,
#                 address text,
#               city text,
#             state text,
#           zipcode integer
#         )""")


# CREATE A SUBMIT FUNCTION
def AddRecord():
    connection1 = sqlite3.connect('address_book.db')  # will save database in directory if doesn't exist
    cursor1 = connection1.cursor()  # create a cursor

    # INSERT INTO TABLE NOTICE THE SEMICOLON BEFORE LIST BEGINS this is some SQL code
    cursor1.execute("INSERT INTO addresses VALUES (:first_name,:last_name,:address,:city,:state,:zipcode)",
                    # USING PYTHON DICTIONARY TO SET PAIRS
                    {'first_name': user_name_first.get(),
                     'last_name': user_name_last.get(),
                     'address': user_address.get(),
                     'city': user_city.get(),
                     'state': user_USstate.get(),
                     'zipcode': user_zipcode.get()
                     }
                    )

    connection1.commit()  # commit changes
    connection1.close()  # ALWAYS CLOSE THE CONNECTION TO DATABASE

    # clear the text box
    user_name_first.delete(0, END)
    user_name_last.delete(0, END)
    user_address.delete(0, END)
    user_USstate.delete(0, END)
    user_zipcode.delete(0, END)
    user_city.delete(0, END)


def Query():
    connection1 = sqlite3.connect('address_book.db')  # connect
    cursor1 = connection1.cursor()  # create a cursor
    # QUERY THE DATABASE
    # * = all, oid is the original id SQL doesnt automatically display
    cursor1.execute("SELECT *, oid FROM addresses")
    records = cursor1.fetchall()  # can alter this command to return specific groups
    # print(records)
    print_records = ''
    for record in records:
        # DONT WANT TO PRINT OUT SENSITIVE INFORMATION, NOTICE STR[RECORD[INFO NUMBER IN LIST])
        print_records += str(record[0]) + " " + str(record[1]) + "  " + str(record[6]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=10, column=1, pady=20)
    connection1.commit()  # commit changes
    connection1.close()  # ALWAYS CLOSE THE CONNECTION TO DATABASE


def DeleteRecord():
    # want to search by oid to delete things, some may share a name or characteristics.
    connection1 = sqlite3.connect('address_book.db')  # connect
    cursor1 = connection1.cursor()  # create a cursor
    cursor1.execute(
        "DELETE from addresses WHERE oid= " + update_box.get())  # .get doesnt work in SQL, you have to concatanate it to the id field
    connection1.commit()  # commit changes
    connection1.close()  # ALWAYS CLOSE THE CONNECTION TO DATABASE


def UpdateRecord():
    # want this to open in new window
    global editor
    editor = Tk()
    editor.title("Edit user details here")
    editor.geometry("650x100")
    connection1 = sqlite3.connect('address_book.db')  # connect
    cursor1 = connection1.cursor()  # create a cursor

    # CREATE TEXT BOX these need to be global so save button can access
    global editorFirst
    global editorLast
    global editorAddress
    global editorCity
    global editorState
    global editorZip
    editorFirst = Entry(editor, width=10)
    editorFirst.grid(row=1, column=0, padx=20, pady=10)
    editorLast = Entry(editor, width=10)
    editorLast.grid(row=1, column=1, padx=20, pady=10)
    editorAddress = Entry(editor, width=10)
    editorAddress.grid(row=1, column=2, padx=20, pady=10)
    editorCity = Entry(editor, width=10)
    editorCity.grid(row=1, column=3, padx=20, pady=10)
    editorState = Entry(editor, width=10)
    editorState.grid(row=1, column=4, padx=20, pady=10)
    editorZip = Entry(editor, width=10)
    editorZip.grid(row=1, column=5, padx=20, pady=10)

    # CREATE TEXT BOX LABELS
    editorFirstLabel = Label(editor, text="First Name")
    editorFirstLabel.grid(row=0, column=0)
    editorLastLabel = Label(editor, text="Last Name")
    editorLastLabel.grid(row=0, column=1)
    editorAddressLabel = Label(editor, text="Address")
    editorAddressLabel.grid(row=0, column=2)
    editorCityLabel = Label(editor, text="City")
    editorCityLabel.grid(row=0, column=3)
    editorStateLabel = Label(editor, text="State")
    editorStateLabel.grid(row=0, column=4)
    editorZipLabel = Label(editor, text="Zipcode")
    editorZipLabel.grid(row=0, column=5)

    record_id = update_box.get()  # get the oid from the update box
    cursor1.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    # .get doesnt work in SQL, you have to concatanate it to the id field
    # MAKE LOOP TO FILL IN DATA BOXES
    records = cursor1.fetchall()
    for record in records:
        editorFirst.insert(0, record[0])
        editorLast.insert(0, record[1])
        editorAddress.insert(0, record[2])
        editorCity.insert(0, record[3])
        editorState.insert(0, record[4])
        editorZip.insert(0, record[5])

    connection1.commit()  # commit changes
    connection1.close()  # ALWAYS CLOSE THE CONNECTION TO DATABASE
    # add save button
    buttonSaveRecord = Button(editor, text="Save Record", command=SaveUpdate)
    buttonSaveRecord.grid(row=2, column=0, columnspan=5)

def SaveUpdate():
    record_id = update_box.get()
    connection1 = sqlite3.connect('address_book.db')  # connect
    cursor1 = connection1.cursor()  # create a cursor
       # this is SQL code, also see curly brackets is a Python dictionary to set the values in the DB again
    cursor1.execute("""
       UPDATE addresses SET
       first_name = :first, 
       last_name = :last, 
       address = :address, 
       city = :city,
       state = :state, 
        zipcode = :zipcode

        WHERE oid = :oid
        """,
                        {'first': editorFirst.get(),
                         'last': editorLast.get(),
                         'address': editorAddress.get(),
                         'city': editorCity.get(),
                         'state': editorState.get(),
                         'zipcode': editorZip.get(),
                         'oid': record_id
                         }
                        )
    connection1.commit()  # commit changes
    connection1.close()  # ALWAYS CLOSE THE CONNECTION TO DATABASE
    editor.destroy()


# GUI SECTION OF THE DATABASE

background_image = tkinter.PhotoImage(file='techThumb.png')
backgroundLabel = Label(root, image=background_image)
backgroundLabel.place(relwidth=1, relheight=1)

# CREATE TEXT BOX
user_name_first = Entry(root, width=10)
user_name_first.grid(row=1, column=0, padx=20, pady=10)
user_name_last = Entry(root, width=10)
user_name_last.grid(row=1, column=1, padx=20, pady=10)
user_address = Entry(root, width=10)
user_address.grid(row=1, column=2, padx=20, pady=10)
user_city = Entry(root, width=10)
user_city.grid(row=1, column=3, padx=20, pady=10)
user_USstate = Entry(root, width=10)
user_USstate.grid(row=1, column=4, padx=20, pady=10)
user_zipcode = Entry(root, width=10)
user_zipcode.grid(row=1, column=5, padx=20, pady=10)
update_box = Entry(root, width=10)
update_box.grid(row=3, column=1, padx=20, pady=10)

# CREATE TEXT BOX LABELS
user_name_first_label = Label(root, text="First Name")
user_name_first_label.grid(row=0, column=0)
user_name_last_label = Label(root, text="Last Name")
user_name_last_label.grid(row=0, column=1)
user_address_label = Label(root, text="Address")
user_address_label.grid(row=0, column=2)
user_city_label = Label(root, text="City")
user_city_label.grid(row=0, column=3)
user_USstate_label = Label(root, text="State")
user_USstate_label.grid(row=0, column=4)
user_zipcode_label = Label(root, text="Zipcode")
user_zipcode_label.grid(row=0, column=5)
user_select_box = Label(root, text="Enter OID")
user_select_box.grid(row=3, column=0)

# BUTTONS FOR FUNCTIONALITY
buttonSubmit = Button(root, text="Add Record", command=AddRecord)
buttonSubmit.grid(row=2, column=5, pady=10)
buttonQuery = Button(root, text="Show Record", command=Query)
buttonQuery.grid(row=6, column=0, pady=10)
buttonDelete = Button(root, text="Delete Record", command=DeleteRecord)
buttonDelete.grid(row=4, column=0)
buttonUpdate = Button(root, text="Update Record", command=UpdateRecord)
buttonUpdate.grid(row=4, column=1)



root.mainloop()
