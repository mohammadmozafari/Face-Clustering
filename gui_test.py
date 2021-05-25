import tkinter as tk
from tkinter.constants import LEFT, RIGHT

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('{}x{}+{}+{}'.format(900, 600, 300, 100))
        self.title('Clusterer')
        self.resizable(0, 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

    def create_left_bar(self):
        sidebar = tk.Frame(self)
        sidebar.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        sidebar['borderwidth'] = 5
        sidebar.configure(bg='blue')
        sidebar.pack()

    

def main():

    gui = GUI()
    gui.create_left_bar()
    gui.mainloop()
    # window = tk.Tk()
    # window.geometry('{}x{}+{}+{}'.format(900, 600, 300, 100))


    # sidebar = tk.Frame(width=10)
    # sidebar['borderwidth'] = 5
    # sidebar['relief'] = 'sunken'
    # sidebar.configure(bg='blue')
    # sidebar.pack(expand=True, side=LEFT, fill='both')

    # sidebar2 = tk.Frame(width=200)
    # sidebar2['borderwidth'] = 5
    # sidebar2['relief'] = 'sunken'
    # sidebar2.configure(bg='red')
    # sidebar2.pack(expand=True, side=RIGHT, fill='both')

    # window.mainloop()


if __name__ == "__main__":
    main()
