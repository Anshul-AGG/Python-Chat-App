import socket
import threading
import tkinter
from tkinter import simpledialog, scrolledtext

class ChatClient:
    def __init__(self, host, port):
        # Initialize Connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        # Ask for Nickname via Popup
        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        
        self.gui_done = False
        self.running = True

        # Start Threads
        threading.Thread(target=self.gui_loop).start()
        threading.Thread(target=self.receive).start()

    def gui_loop(self):
        """Builds the Tkinter Interface."""
        self.win = tkinter.Tk()
        self.win.title("Python LAN Chat")
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        """Sends messages and handles commands."""
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        
        # Deliverable: Command support (/exit)
        if "/exit" in message:
            self.stop()
        else:
            self.client.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def receive(self):
        """Listens for messages from the server."""
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("An error occurred!")
                self.client.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.client.close()
        exit()

client = ChatClient('127.0.0.1', 55555)