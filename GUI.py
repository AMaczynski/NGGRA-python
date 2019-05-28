from tkinter import *
from tkinter.filedialog import askopenfilename
from detector import Detector
import cv2
import JsonReader
from JsonConfig import *
import threading
from imutils.video import VideoStream
import imutils
from PIL import Image
from PIL import ImageTk

DEFAULT_CONFIG_PATH = "config.json"
target_algorithm = 0


class ProgramGui:
    def __init__(self, master):
        self.master = master
        master.title("NGGRA-python")
        master.minsize(width=600, height=400)

        self.menu = Menu(master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Load configuration", command=self.load_file)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        master.config(menu=self.menu)
        self.vs = VideoStream().start()
        self.frame = None

        self.spinners = {}
        self.canvas = None
        self.config_file = "config.json"
        self.program = None
        self.is_config_file_loaded = False
        self.panel = None

        self.entries_frame = Frame(master)

        self.make_form()
        self.button_start = Button(master, text="Start application", command=self.start_detector)
        self.entries_frame.pack()
        self.button_start.pack()

        self.config = {}
        self.load_file(DEFAULT_CONFIG_PATH)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

    def video_loop(self):
        while not self.stopEvent.is_set():
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=600)
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            if self.panel is None:
                self.panel = Label(image=image)
                self.panel.image = image
                self.panel.pack(padx=10, pady=10)
            else:
                self.panel.configure(image=image)
                self.panel.image = image

    def load_file(self, path=None):
        if path is None:
            filename = askopenfilename()
        else:
            filename = path
        if len(filename) > 0 and filename.endswith(".json"):
            self.config_file = filename
            self.is_config_file_loaded = True
            self.load_config()

    def load_config(self):
        reader = JsonReader.Reader()
        reader.read_config(self.config_file)
        self.config[THUMB] = reader.get_attribute(THUMB)
        self.config[PALM] = reader.get_attribute(PALM)
        self.config[FIST] = reader.get_attribute(FIST)
        self.config[STRAIGHT] = reader.get_attribute(STRAIGHT)
        self.config[PEACE] = reader.get_attribute(PEACE)

        for key, spinner in self.spinners.items():
            var = StringVar(root)
            var.set(self.config[key])
            spinner.config(textvariable=var)

    def make_form(self):
        fields = THUMB, PALM, FIST, STRAIGHT, PEACE
        values = (MOVE_MOUSE, CLICK_MOUSE, PLAY_PAUSE, MUTE, NEXT_TRACK)
        for i, field in enumerate(fields):
            row_frame = Frame(self.entries_frame)
            field_label = Label(row_frame, width=15, text=fields[i], anchor='w')
            spinner = Spinbox(row_frame)
            spinner.config(values=values)
            row_frame.grid(row=int(i / 2), column=(i % 2))
            field_label.pack(side=LEFT)
            spinner.pack(side=RIGHT, expand=YES, fill=X)
            self.spinners[field] = spinner

    def start_detector(self):
        fun_config = []
        indexes = [THUMB, PALM, FIST, STRAIGHT, PEACE]
        for i in range(len(self.spinners)):
            gesture = indexes[i]
            config_tuple = (gesture, self.spinners[gesture].get())
            fun_config.append(config_tuple)

        self.vs.stop()
        self.master.destroy()
        detector = Detector()
        Detector.start(detector, fun_config)


if __name__ == "__main__":
    root = Tk()
    gui = ProgramGui(root)
    root.mainloop()
