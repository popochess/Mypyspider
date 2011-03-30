#! /usr/bin/env python
from Tkinter import *
from Tkconstants import *
import tkMessageBox
import pyspider

class GUIFramework(Frame):
    """This is the GUI"""
       
    def __init__(self,master=None):

        """Initialize"""
        Frame.__init__(self,master)

        self.master.title("PyCrawler")

        """Display the main window"""       
        self.grid(padx=10,  pady=30)                                              
        self.create_widgets()
    





    def create_widgets(self):
        

        self.lb_ip = Label(self, text="http://")
        self.lb_ip.grid(row=0, column=0)

        self.lb_d = Label(self, text="depth ")
        self.lb_d.grid(row=1, column=0)

        self.entry_ip = Entry(self)
        self.entry_ip.grid(row=0, column=1, columnspan=1)

        self.entry_d = Entry(self)
        self.entry_d.grid(row=1, column=1, columnspan=1)

        self.btnDisplay = Button(self, text="GO !!", command=self.crawl_and_save)
        self.btnDisplay.grid(row =3, column=2)
    '''
    def Display(self):
    tkMessageBox.showinfo("Text", "You typed: %s" % self.enText.get() )
    '''
    def crawl_and_save(self):
     
        spider.run()

        url_txet = "\n".join(spider.followedURLs)
        fp = file('urls_output.txt','w')
        fp.write(url_txet)
        fp.close()
         
        tkMessageBox.showinfo("Text", "Output file has saved to your Desktop!" )
         
    

if __name__ == "__main__":
    guiFrame = GUIFramework()
    guiFrame.mainloop()
