from tkinter import *
from tkinter.filedialog import askopenfilename
from detector import Detector
import JsonReader
import JsonConfig


class ProgramGui:
    def __init__(self, master):
        detector = Detector()

        self.master = master
        master.title("Disease simulation")
        master.minsize(width=600, height=120)

        self.menu = Menu(master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Load configuration", command=self.load_file)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        master.config(menu=self.menu)

        self.entries = []
        self.canvas = None
        self.config_file = "config.json"
        self.program = None
        self.is_config_file_loaded = False

        self.entries_frame = Frame(master)

        self.make_form()
        self.button_start = Button(master, text="Start application", command=detector.start)
        self.entries_frame.pack()
        self.button_start.pack()

        self.thumb = 0 # must match fields order and len(config)
        self.palm = 1
        self.fist = 2
        self.straight = 3
        self.peace = 4

        self.config = [None, None, None, None, None]

    def load_file(self):
        filename = askopenfilename()
        if len(filename) > 0 and filename.endswith(".json"):
            self.config_file = filename
            self.is_config_file_loaded = True
            self.load_config()

    def load_config(self):
        reader = JsonReader.Reader()
        reader.read_config(self.config_file)
        self.config[self.thumb] = reader.get_attribute(JsonConfig.THUMB)
        self.config[self.palm] = reader.get_attribute(JsonConfig.PALM)
        self.config[self.fist] = reader.get_attribute(JsonConfig.FIST)
        self.config[self.straight] = reader.get_attribute(JsonConfig.STRAIGHT)
        self.config[self.peace] = reader.get_attribute(JsonConfig.PEACE)

        for i, entry in enumerate(self.entries):
            print("elo: " + str(i))
            entry.delete(0, END)
            entry.insert(0, str(self.config[i]))

    def make_form(self):
        fields = 'Thumb:', 'Peace', 'Palm', 'Fist', 'Straight'
        for i, field in enumerate(fields):
            row_frame = Frame(self.entries_frame)
            field_label = Label(row_frame, width=15, text=fields[i], anchor='w')
            entry = Entry(row_frame)
            row_frame.grid(row=int(i / 2), column=(i % 2))
            field_label.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append(entry)


if __name__ == "__main__":
    root = Tk()
    gui = ProgramGui(root)
    root.mainloop()
