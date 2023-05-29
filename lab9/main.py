import datetime
import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Selin.unal1408"
)

#creating db
cursorObject=dataBase.cursor()

#cursorObject.execute("CREATE DATABASE MyNewDatabase")

connection=mysql.connector.connect(
    host="localhost",
    user="root",
    database='MyNewDatabase',
    password="Selin.unal1408"
)
if connection.is_connected():
    db_info=connection.get_server_info()
    print("Connected to MySQL Server version", db_info)
    cursor=connection.cursor()
    cursor.execute("select database();")
    record=cursor.fetchone()
    print("You are connected to database:",record)


#building a table

    """
    connection=mysql.connector.connect(
        host='localhost',
        database='MyNewDatabase',
        user='root',
        password='Selin.unal1408')

  mySql_create_table_query=CREATE TABLE Movies(
                  ID int(11) ,
                  MOVIE  varchar(250) ,
                  DATE  date,
                  MCU_PHASE varchar(100)
                  )
    

    cursor=connection.cursor()
    result=cursor.execute(mySql_create_table_query)
    print("Movies table created")
"""
    cursor.execute("SHOW TABLES")
    for table_name in cursor:
        print(table_name)





#dosyadakileri aktarma
with open('Marvel.txt','r') as file:

     lines=file.readlines()

     for line in lines:
         data=line.strip().split()

         ID=int(data[0])
         MOVIE=data[1]
         DATE=datetime.datetime.strptime(data[2], '%B%d,%Y').date()
         PHASE=data[3]

         insert_query="INSERT INTO Movies(ID,MOVIE,DATE,MCU_PHASE) VALUES(%s,%s,%s,%s)"
         insert_data=(ID,MOVIE,DATE,PHASE)
         cursor.execute(insert_query,insert_data)

connection.commit()

#qui


window=tk.Tk()
window_width = 640
window_height = 640
window_size = f"{window_width}x{window_height}"
window.geometry(window_size)

window.title("Movie")

text_box = tk.Text(window, height=50, width=50)
text_box.place(x=100,y=220)



def populate_text_box(selected_value=None):
    text_box.delete(1.0, tk.END)

    try:
        if selected_value:
            cursor.execute("SELECT * FROM Movies WHERE ID = %s", (selected_value,))
        else:
            cursor.execute("SELECT * FROM Movies")

        results = cursor.fetchall()
        for result in results:
            text_box.insert(tk.END, "ID: {}\nMOVIE: {}\nDATE: {}\nMCU_PHASE: {}\n\n".format(result[0], result[1], result[2],
                                                                                            result[3]))
            break
    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to retrieve movie details: {}".format(error))

def dropdown_selected(event):
    selected_value = dropdown.get()
    print("Selected Value:", selected_value)
    populate_text_box(selected_value)




# Dropdown list
dropdown_label = tk.Label(window, text="Select the movie ID:")
dropdown_label.pack()

dropdown = ttk.Combobox(window, values=list(range(1, 23)))
dropdown.bind("<<ComboboxSelected>>", dropdown_selected)
dropdown.pack()



def add_button_clicked():
    # Create a pop-up box with a text box and two buttons
    def pop_up_ok():

        movie_id =entry_id.get()
        movie_name = entry_movie.get()
        release_date = entry_date.get()
        phase = entry_phase.get()
        try:
            cursor.execute("INSERT INTO Movies (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)",
                           (movie_id, movie_name, release_date, phase))
            connection.commit()
            messagebox.showinfo("Success", "Movie added to the database.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", "Failed to add movie to the database: {}".format(error))
        pop_up.destroy()

    def pop_up_cancel():
        pop_up.destroy()

    pop_up = tk.Toplevel(window)
    pop_up.title("Add Movie")

    label_id = tk.Label(pop_up, text="ID:")
    label_id.pack()
    entry_id = tk.Entry(pop_up)
    entry_id.pack()

    label_movie = tk.Label(pop_up, text="Movie:")
    label_movie.pack()
    entry_movie = tk.Entry(pop_up)
    entry_movie.pack()

    label_date = tk.Label(pop_up, text="Date:")
    label_date.pack()
    entry_date = tk.Entry(pop_up)
    entry_date.pack()


    label_phase = tk.Label(pop_up, text="MCU Phase:")
    label_phase.pack()
    entry_phase = tk.Entry(pop_up)
    entry_phase.pack()



    ok_button = tk.Button(pop_up, text="Ok", command=pop_up_ok)
    ok_button.pack()

    cancel_button = tk.Button(pop_up, text="Cancel", command=pop_up_cancel)
    cancel_button.pack()

def listAll_button_clicked():
    text_box = tk.Text()
    text_box = tk.Text(height=50,width=50)
    text_box.place(x=100,y=220)

    try:
        cursor.execute("SELECT * FROM Movies")
        results = cursor.fetchall()
        text_box.delete(1.0, tk.END)
        for result in results:
            text_box.insert(tk.END,
                            "ID: {}\nMOVIE: {}\nDATE: {}\nMCU_PHASE: {}\n\n".format(result[0], result[1], result[2],
                                                                                    result[3]))
    except mysql.connector.Error as error:
        messagebox.showerror("Error", "Failed to retrieve movie details: {}".format(error))


add_button = tk.Button(window, text="Add", command=add_button_clicked)
add_button.place(x=300,y=100)

listAll_button= tk.Button(window,text="List All" , command=listAll_button_clicked)
listAll_button.place(x=295,y=150)


#queries

#a List all Movies
try:
    cursor.execute("SELECT * FROM Movies")
    results = cursor.fetchall()
    if results:
        for result in results:
            print("ID: {}\nMOVIE: {}\nDATE: {}\nMCU_PHASE: {}\n".format(result[0], result[1], result[2], result[3]))
        print("All movies have been displayed.")

    else:
        print("No movies found.")

except mysql.connector.Error as error:
    print("Failed to retrieve movie details: {}".format(error))

#b Remove TheIncredibleHulk from the table
try:
    cursor.execute("DELETE FROM Movies WHERE MOVIE = 'TheIncredibleHulk'")
    connection.commit()
    print("TheIncredibleHulk movie removed from the table.")
except mysql.connector.Error as error:
    print("Failed to remove TheIncredibleHulk movie: {}".format(error))

#c List all Phase 2 Movies
try:
    cursor.execute("SELECT * FROM Movies WHERE MCU_PHASE = 'Phase2'")
    results = cursor.fetchall()
    for result in results:
        print("ID: {}\nMOVIE: {}\nDATE: {}\nMCU_PHASE: {}\n".format(result[0], result[1], result[2], result[3]))
except mysql.connector.Error as error:
    print("Failed to retrieve Phase 2 movies: {}".format(error))


#d Fix the date of Thor:Ragnarok. The date should be 2017 not 2019

try:
    cursor.execute("UPDATE Movies SET DATE = '2017-11-03' WHERE MOVIE = 'Thor:Ragnarok'")
    connection.commit()
    print("Date of Thor:Ragnarok updated successfully.")
except mysql.connector.Error as error:
    print("Failed to update the date of Thor:Ragnarok: {}".format(error))


window.mainloop()


















