from tkinter import *
from MRS import startSearch
from datetime import date
from tkcalendar import Calendar, DateEntry

xPad = 5
yPad = 3

class App:
  def __init__(self, master):
    frame = Frame(master)

    queryLabel = Label(text="Query: ")
    queryLabel.grid(row = 0, column = 0, padx= xPad, pady = yPad)

    self.queryEntry = Entry()
    self.queryEntry.insert(0, "trump")
    self.queryEntry.grid(row = 0, column = 1, padx= xPad, pady = yPad, sticky='ew')

    subLabel = Label(text="Subreddit: ")
    subLabel.grid(row = 1, column = 0, padx= xPad, pady = yPad)

    self.subEntry = Entry()
    self.subEntry.insert(0, "worldnews")
    self.subEntry.grid(row = 1, column = 1, padx= xPad, pady = yPad, sticky='ew')

    filenameLabel = Label(text="Filename: ")
    filenameLabel.grid(row = 2, column = 0, padx= xPad, pady = yPad)

    self.filenameEntry = Entry()
    self.filenameEntry.insert(0, "test")
    self.filenameEntry.grid(row = 2, column = 1, padx= xPad, pady = yPad, sticky='ew')

    afterLabel = Label(text="After: ")
    afterLabel.grid(row = 3, column = 0, padx= xPad, pady = yPad)

    self.afterEntry = DateEntry()
    self.afterEntry.grid(row = 3, column = 1, padx= xPad, pady = yPad, sticky='ew')

    beforeLabel = Label(text="Before: ")
    beforeLabel.grid(row = 4, column = 0, padx= xPad, pady = yPad)

    self.beforeEntry = DateEntry()
    self.beforeEntry.grid(row = 4, column = 1, padx= xPad, pady = yPad, sticky='ew')

    self.searchBtn = Button(
                         text="Search",
                         command=self.search)
    self.searchBtn.grid(row = 100, column = 0, columnspan=2, sticky='nesw', padx= xPad, pady = yPad)

    self.statusText = Text(width=41, height=20)
    self.statusText.grid(row = 101, column = 0, columnspan=2, sticky='nesw', padx= xPad, pady = yPad)
    self.statusText.tag_configure("success", foreground="green")
    self.statusText.tag_configure("fail", foreground="red")

  def search(self):
    query = self.queryEntry.get()
    subr = self.subEntry.get()
    filename = self.filenameEntry.get()
    after = self.afterEntry.get_date()
    before = self.beforeEntry.get_date()

    startSearch(query, after, before, subr, filename, self.statusText, root)

root = Tk()
root.title("MyRedditScrapper")
root.geometry("350x450")
app = App(root)
root.mainloop()
