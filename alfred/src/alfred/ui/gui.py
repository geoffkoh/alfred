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
from alfred.io.question import create_from_file
from alfred.net.driver.myleo import MyLeoDriver
from alfred.action.upload import ActionUploadQuestion

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
    # Handler to put all messages into queue

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class App(tk.Tk):
    """ The main application """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self.question = None

        self.title('ALFRED v0.1')

        # Adds in the log queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(levelname)s:%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logging.root.addHandler(self.queue_handler)
        logging.root.setLevel(logging.INFO)

        # Sets the size of the window
        self.rowconfigure(0, minsize=800, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)

        # Declares the components
        self.scrolled_text = ScrolledText(self, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)

        frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)
        btn_open_file = tk.Button(frm_buttons, text="Open MCQ Question", command=self.open_file)
        btn_upload_myleo = tk.Button(frm_buttons, text="Upload to MyLEO", command=self.upload_myleo)
        btn_upload_sa20 = tk.Button(frm_buttons, text="Upload to SA2.0")
        btn_exit = tk.Button(frm_buttons, text="Exit", command=self.destroy)

        # Placing the components
        btn_open_file.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_upload_myleo.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_upload_sa20.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_exit.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        frm_buttons.grid(row=0, column=0, sticky="ns")
        self.scrolled_text.grid(row=0, column=1, sticky="nsew")

        # Start polling messages from the queue
        self.after(100, self.poll_log_queue)

        logger.info(f'\n{create_start_image()}')

    def display(self, record):
        """ Displays the record """
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
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
        """ Command to open the file """

        filename = askopenfilename()
        bank = create_from_file(filename)
        logger.info('Loaded file %s', filename)
        logger.info('Questions:\n%s', pformat(asdict(bank)))

        self.question = bank

    # end open_file()

    def upload_myleo(self):
        """ Command to upload to MyLeo """

        if not self.question:
            logger.warning('You have not yet open a question file yet')
            return

        # Displays the username and password dialog in succession
        username = askstring('Username', 'Enter username (without @rp.edu.sg')
        if not username:
            return
        if not username.endswith('@rp.edu.sg'):
            username = f'{username}@rp.edu.sg'
        logger.info('Username is %s', username)
        password = askstring('Password', 'Enter Password', show='*')
        if not password:
            return
    
        logger.info('Creating driver for MyLEO')
        driver = MyLeoDriver()
        driver.connect(
            username=username,
            password=password
        )

        # Creates the action and tries to upload the question
        logger.info('Uploading quesion')
        action = ActionUploadQuestion()
        action.run(driver=driver, bank=self.question)

        logger.info('Done')


def create_start_image():
    """ Function to generate the initial image """
    pattern = '''
    ___    __    ____  __________ 
   /   |  / /   / __ \/ ____/ __ \\
  / /| | / /   / /_/ / __/ / / / /
 / ___ |/ /___/ _, _/ /___/ /_/ / 
/_/  |_/_____/_/ |_/_____/_____/  v0.1
Automation for Learning FRamework for EDucation
    '''
    return pattern
