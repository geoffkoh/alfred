""" TKinter Based Interface """

# Standard imports
from dataclasses import asdict
import logging
from pprint import pformat
import queue

# Third party imports
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename

# Application imports
from alfred import __version__
from alfred.io.question import create_from_file
from alfred.net.driver.myleo import MyLeoDriver
from alfred.net.driver.mysa import MySADriver
from alfred.action.upload_myleo import ActionUpload_MCQ2MyLEO
from alfred.action.upload_mysa import ActionUpload_MCQ2MySA

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
    # Handler to put all messages into queue

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class App(tk.Tk):
    """The main application"""

    def __init__(self):
        """Constructor"""

        super().__init__()

        self.question = None

        self.title(f"ALFRED v{__version__}")

        # Sets geometry
        window_width = 800
        window_height = 600
        self.minsize(width=window_width, height=400)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Adds in the log queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter("%(levelname)s:%(asctime)s: %(message)s")
        self.queue_handler.setFormatter(formatter)
        logging.root.addHandler(self.queue_handler)
        logging.root.setLevel(logging.INFO)

        # Sets the size of the window
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)

        # Declares the components
        self.scrolled_text = ScrolledText(self, state="disabled", height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrolled_text.configure(font="TkFixedFont")
        self.scrolled_text.tag_config("INFO", foreground="black")
        self.scrolled_text.tag_config("DEBUG", foreground="gray")
        self.scrolled_text.tag_config("WARNING", foreground="orange")
        self.scrolled_text.tag_config("ERROR", foreground="red")
        self.scrolled_text.tag_config("CRITICAL", foreground="red", underline=1)

        frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)
        btn_open_file = tk.Button(
            frm_buttons, text="Open MCQ Question", command=self.open_file
        )
        btn_upload_myleo = tk.Button(
            frm_buttons, text="Upload to LEO2.0", command=self.upload_myleo
        )
        btn_upload_mysa = tk.Button(
            frm_buttons, text="Upload to SA2.0", command=self.upload_mysa
        )
        btn_exit = tk.Button(frm_buttons, text="Exit", command=self.destroy)

        # Placing the components
        btn_open_file.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_upload_myleo.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_upload_mysa.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_exit.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        frm_buttons.grid(row=0, column=0, sticky="ns")
        self.scrolled_text.grid(row=0, column=1, sticky="nsew")

        # Start polling messages from the queue
        self.after(100, self.poll_log_queue)

        logger.info(f"\n{create_start_image()}")

    def display(self, record):
        """Displays the record"""
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state="normal")
        self.scrolled_text.insert(tk.END, msg + "\n", record.levelname)
        self.scrolled_text.configure(state="disabled")
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.after(100, self.poll_log_queue)

    def open_file(self):
        """Command to open the file"""

        filename = askopenfilename()
        bank = create_from_file(filename)
        logger.info("Loaded file %s", filename)
        logger.info("Questions:\n%s", pformat(asdict(bank)))

        self.question = bank

    # end open_file()

    def upload_myleo(self):
        """Command to upload to MyLeo"""

        if not self.question:
            logger.error("You have not yet open a question file")
            return

        # Displays the username and password dialog in succession
        driver = MyLeoDriver()

        # Checks to see if I need to connect
        connected = driver.is_connected()

        if not connected:
            driver.driver.close()
            username = askstring("Username", "Enter username (without @rp.edu.sg)")
            if not username:
                logger.error('No username given')
                return
            if not username.endswith("@rp.edu.sg"):
                username = f"{username}@rp.edu.sg"
            logger.info("Username is %s", username)
            password = askstring("Password", "Enter Password", show="*")
            if not password:
                logger.error('No password given')
                return
            logger.info("Creating driver for LEO2.0")
            driver = MyLeoDriver()
            connected = driver.connect(username=username, password=password)

        if connected:
            # Creates the action and tries to upload the question
            logger.info("Uploading question")
            action = ActionUpload_MCQ2MyLEO()
            action.run(driver=driver, bank=self.question)
            logger.info("Done")
        else:
            logger.error("Cannot log in. Perhaps incorrect username and password")

    # end upload_myleo()

    def upload_mysa(self):
        """Command to upload to MySA 2.0"""

        if not self.question:
            logger.error("You have not yet open a question file")
            return

        # Displays the username and password dialog in succession
        username = askstring("Username", "Enter username (without @rp.edu.sg)")
        if not username:
            logger.error('No username given')
            return
        logger.info("Username is %s", username)
        password = askstring("Password", "Enter Password", show="*")
        if not password:
            logger.error('No password given')
            return

        logger.info("Creating driver for MySA")
        driver = MySADriver()

        if driver.connect(username=username, password=password):
            # Creates the action and tries to upload the question
            logger.info("Uploading question")
            action = ActionUpload_MCQ2MySA()
            action.run(driver=driver, bank=self.question)
            logger.info("Done")
        else:
            logger.error("Cannot log in. Perhaps incorrect username and password")

    # end upload_myleo()


def create_start_image():
    """Function to generate the initial image"""
    pattern = f"""
    ___    __    __________  __________ 
   /   |  / /   / ____/ __ \/ ____/ __ \\
  / /| | / /   / /_  / /_/ / __/ / / / /
 / ___ |/ /___/ __/ / _, _/ /___/ /_/ / 
/_/  |_/_____/_/   /_/ |_/_____/_____/  v{__version__}
Automation for Learning FRamework for EDucation
    """
    return pattern
