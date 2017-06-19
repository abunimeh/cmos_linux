#! /usr/bin/env python3
"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: im client for pj
"""

import os
import socket
import tkinter as tk
import tkinter.ttk as ttk

USER_NAME = os.path.expandvars("$USER")
RECV_BUF = 4096
HOST = "172.51.13.205"
PORT = 5000

SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SS.settimeout(2)

class PJIM(ttk.Frame):
    """pj im tk class"""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.ivar = tk.StringVar()
        self.oframe = ttk.LabelFrame(self, text="Chat content")
        self.oframe.pack(side="top", fill="both", expand="yes")
        self.iframe = ttk.LabelFrame(self, text="Input")
        self.iframe.pack(side="top", fill="both", expand="yes")
        self.oscroll = ttk.Scrollbar(self.oframe)
        self.oscroll.pack(side="right", fill="y")
        self.ientry = ttk.Entry(self.iframe, width=70, textvariable=self.ivar)
        self.ientry.pack(side="top")
        self.otext = tk.Text(self.oframe, yscrollcommand=self.oscroll.set)
        self.otext.pack(side="top")
        self.oscroll.config(command=self.otext.yview)
        self.ientry.focus()
        self.ientry.bind("<Return>", self.send_msg)
        self.tk.createfilehandler(SS, tk.READABLE, self.recv_msg)
    def send_msg(self, *args):
        """sending message toggle function"""
        msg = self.ivar.get()
        self.ientry.delete(0, "end")
        SS.send(msg.encode())
        self.otext.insert("end", f"<You> {msg}{os.linesep}")
        self.otext.see("end")
    def recv_msg(self, sock, mask):
        """receiving message from socket by using tk fh"""
        data = sock.recv(RECV_BUF)
        if not data:
            raise Exception("Disconnected from chat server")
        else:
            self.otext.insert("end", data.decode())
            self.otext.see("end")

def main():
    """im client tk main function"""
    SS.send(f"/u {USER_NAME}".encode())
    root = tk.Tk()
    root.title("PJ IM")
    root.geometry("600x450")
    app = PJIM(master=root)
    app.mainloop()

def run_im(args):
    """to run im sub cmd"""
    if args:
        pass
    try:
        SS.connect((HOST, PORT))
    except socket.error:
        raise Exception("Unable to connect")
    try:
        main()
    except KeyboardInterrupt:
        SS.close()
