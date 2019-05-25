from tkinter import *
from tkinter.filedialog import askopenfilename
from detector import Detector
import cv2
import JsonReader
import JsonConfig
import threading
from imutils.video import VideoStream
import imutils
from PIL import Image
from PIL import ImageTk
import const

DEFAULT_CONFIG_PATH = "config.json"
target_algorithm = 0


class ProgramGui:
    def __init__(self, master):
        self.master = master
        master.title("Disease simulation")
        master.minsize(width=600, height=400)

        self.menu = Menu(master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Load configuration", command=self.load_file)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        master.config(menu=self.menu)
        self.vs = VideoStream().start()

        self.spinners = []
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

        self.config = [None, None, None, None, None]
        self.load_file(DEFAULT_CONFIG_PATH)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

    def video_loop(self):
        # keep looping over frames until we are instructed to stop
        while not self.stopEvent.is_set():
            # grab the frame from the video stream and resize it to
            # have a maximum width of 300 pixels
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=300)

            # OpenCV represents images in BGR order; however PIL
            # represents images in RGB order, so we need to swap
            # the channels, then convert to PIL and ImageTk format
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # if the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = Label(image=image)
                self.panel.image = image
                self.panel.pack(padx=10, pady=10)

            # otherwise, simply update the panel
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
        self.config[const.thumb] = reader.get_attribute(JsonConfig.THUMB)
        self.config[const.palm] = reader.get_attribute(JsonConfig.PALM)
        self.config[const.fist] = reader.get_attribute(JsonConfig.FIST)
        self.config[const.straight] = reader.get_attribute(JsonConfig.STRAIGHT)
        self.config[const.peace] = reader.get_attribute(JsonConfig.PEACE)

        for i, spinner in enumerate(self.spinners):
            print("elo: " + str(i))
            var = StringVar(root)
            var.set(self.config[i])
            spinner.config(textvariable=var)

    def make_form(self):
        fields = 'Thumb', 'Peace', 'Palm', 'Fist', 'Straight'
        values = ('Move mouse', 'Click mouse', 'Next track', 'Mute', 'Play/Pause')
        for i, field in enumerate(fields):
            row_frame = Frame(self.entries_frame)
            field_label = Label(row_frame, width=15, text=fields[i], anchor='w')
            spinner = Spinbox(row_frame)
            spinner.config(values=values)
            row_frame.grid(row=int(i / 2), column=(i % 2))
            field_label.pack(side=LEFT)
            spinner.pack(side=RIGHT, expand=YES, fill=X)
            self.spinners.append(spinner)

    def start_detector(self):
        fun_config = []
        indexes = [const.thumb, const.palm, const.fist, const.straight, const.peace]
        for i in range(len(self.spinners)):
            config_tuple = (indexes[i], self.spinners[i].get())
            fun_config.append(config_tuple)

        self.vs.stop()
        self.master.destroy()
        detector = Detector()
        Detector.start(detector, fun_config)


if __name__ == "__main__":
    root = Tk()
    gui = ProgramGui(root)
    root.mainloop()
