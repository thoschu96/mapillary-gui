#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://zetcode.com/gui/tkinter/layout/
# http://docs.activestate.com/komodo/3.5/komodo-doc-guibuilder.html
# http://sebsauvage.net/python/gui/
# http://effbot.org/tkinterbook/grid.htm
 
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from ttk import *
 
import os

######## 26-10-2015 ######
import Tkinter as tk
######## 26-10-2015 ENDE ######

pathname = "Folder"
zaehleFiles = 0

# 
from upload_with_authentication import *
# hol dir die funktionen fuer das Uploaden der files

######## 26-10-2015 ######
counter = 0

def counter_label(label):
  counter = 0
  def count():
    global counter
    counter += 1
    label.config(text=str(counter))
    label.after(1000, count)
  count()

######## 26-10-2015 ENDE ######

    
def answer():
    showerror("Answer", "Sorry, no answer available")
 
def CloseButtonClass():
        quit()
 
def BrowseButtonClass(var):
    name = askopenfilename()
    global pathname
    pathname = os.path.split(name)[0]
#    print pathname
    var.set(pathname)
 
 
#    versuch nach dem browser das script zu starten mit dem parameter des folders
#    os.system('upload_with_authentication.py pathname')
 
 
def HelpButtonClass():
    showwarning('Help', 'Not yet implemented')
 
def GoButtonClass():
    global zaehleFiles
    #showwarning('Go', 'Not yet implemented')
    if pathname == "Folder":
        # was macheen, wenn der Pfad noch nicht ausgewaehlt is
        showwarning('ERROR', 'Bitte einen Pfad auswaehlen')
    else:
        # wenn etwas ausgewaehlt ist, dann loslesen
        path=pathname

        # if no success/failed folders, create them
        create_dirs()

        # erzeuge die Fileliste
        file_list = []
        for root, sub_folders, files in os.walk(path):
            file_list += [os.path.join(root, filename) for filename in files if filename.lower().endswith(".jpg")]

        # hier wird gezaehlt, geht bestimmt auch kuerzer ....

        #print len(file_list)

        x=len(file_list)

        print ('There are', x ,'files in this Directory, yeah')
        #Label(area, text=zaehleFiles).grid(row=1, column=1)

        # variable uebergabe mit der anzahl der dateien die im folder gefunden wurden.
        
        #var.set(x)
                   
        # hier waeres es toll, wenn ich wueste, wieviele Dateien es sind
        # damit ein Ladebalken erzeugt werden kann
        # oder irgendwas aehnliches (counter)


        ###########
        # for DEBUGGING
        ###########

        #print file_list

        ###########
        # for DEBUGGING
        ###########
        
        # get env variables
        try:
            MAPILLARY_USERNAME = "chuck"
            MAPILLARY_PERMISSION_HASH = "eyJleHBpcmF0aW9uIjoiMjAyMC0wMS0wMVQwMDowMDowMFoiLCJjb25kaXRpb25zIjpbeyJidWNrZXQiOiJtYXBpbGxhcnkudXBsb2Fkcy5tYW51YWwuaW1hZ2VzIn0sWyJzdGFydHMtd2l0aCIsIiRrZXkiLCJjaHVjay8iXSx7ImFjbCI6InByaXZhdGUifSxbInN0YXJ0cy13aXRoIiwiJENvbnRlbnQtVHlwZSIsIiJdLFsiY29udGVudC1sZW5ndGgtcmFuZ2UiLDAsMTA0ODU3NjBdXX0="
            MAPILLARY_SIGNATURE_HASH = "gu5rBg1NprnoBEFEzJIVGPZU7Zs="
        except KeyError:
            print("You are missing one of the environment variables MAPILLARY_USERNAME, MAPILLARY_PERMISSION_HASH or MAPILLARY_SIGNATURE_HASH. These are required.")
            sys.exit()

        # generate a sequence UUID
        sequence_id = uuid.uuid4()

        # S3 bucket
        s3_bucket = MAPILLARY_USERNAME+"/"+str(sequence_id)+"/"
        print("Uploading sequence {0}.".format(sequence_id))

    
        # set upload parameters
        params = {"url": MAPILLARY_UPLOAD_URL, "key": s3_bucket,
                "permission": MAPILLARY_PERMISSION_HASH, "signature": MAPILLARY_SIGNATURE_HASH,
                "move_files": MOVE_FILES}

        # create upload queue with all files

        #####
        # hier erstmal alles auf 0 setzen
        #####
        
        zaehleFiles=0

        
        q = Queue()
        for filepath in file_list:
            if verify_exif(filepath):
                q.put(filepath)

                #
                zaehleFiles+=1
                #
                #
                

                #######
                # hier koennte auch gezaehlt werden
                #######
                
            else:
                print("Skipping: {0}".format(filepath))

        # create uploader threads with permission parameters
        uploaders = [UploadThread(q, params) for i in range(NUMBER_THREADS)]

        # ausgeben, wieviele files es sind

        print("Total:", zaehleFiles)
        
        # start uploaders as daemon threads that can be stopped (ctrl-c)
        try:
            for uploader in uploaders:
                uploader.daemon = True
                uploader.start()

                print("Threat ", i, part)

            for uploader in uploaders:
                uploaders[i].join(1)

                #print("Threat", i)

            while q.unfinished_tasks:
                time.sleep(1)
            q.join()
        except (KeyboardInterrupt, SystemExit):
            print("\nBREAK: Stopping upload.")
            sys.exit()

        # ask user if finalize upload to check that everything went fine
        print("===\nFinalizing upload will submit all successful uploads and ignore all failed.\nIf all files were marked as successful, everything is fine, just press 'y'.")

        # ask 3 times if input is unclear
        for i in range(3):
            proceed = raw_input("Finalize upload? [y/n]: ")
            if proceed in ["y", "Y", "yes", "Yes"]:
                # upload an empty DONE file
                upload_done_file(params)
                print("Done uploading.")
                break
            elif proceed in ["n", "N", "no", "No"]:
                print("Aborted. No files were submitted. Try again if you had failures.")
                break
            else:
                if i==2:
                    print("Aborted. No files were submitted. Try again if you had failures.")
                else:
                    print('Please answer y or n. Try again.')
                    
class MapillaryGui(Frame):
 
    def __init__(self, parent):
        Frame.__init__(self, parent)   
 
        self.parent = parent
 
        self.initUI()
 
    def initUI(self):

        value = StringVar()
        value.set(pathname)

        self.parent.title("Mapillary Upload GUI")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
 
        # hier wird die variable "Folder" uebergeben
        
        lbl = Label(self, textvariable=value)
        lbl.grid(sticky=W, pady=4, padx=5)

        #lb2 = Label(self, text=0, textvariable=zaehleFiles)
        #lb2.grid(sticky=W, pady=1, padx=1, row=1, column=1)
        lb2 = Label(self, text=0, textvariable=zaehleFiles)
        lb2.place(x=20, y=20)

        #das weisse Feld  - old code
        #area = Text(self)
 
        area = Text(self)
 
        Label(area, text="Threat 1 : ").grid(row=1)
        Label(area, text="Threat 2 : ").grid(row=2)
        Label(area, text="Threat 3 : ").grid(row=3)
        Label(area, text="Threat 4 : ").grid(row=4)
 
        #value = StringVar()
        #value.set(pathname)
        
        #Threat1 = Entry(area)
        #Threat1 = Entry(area, textvariable=value)

        #Label(area, text=zaehleFiles).grid(row=1, column=1)
        Threat1 = Entry(area, textvariable="value")
        Threat2 = Entry(area)
        Threat3 = Entry(area)
        Threat4 = Entry(area)
        
        ##  Feld mit daten Fuellen, wie updaten ?
        
        Threat1.insert(10,pathname)
        Threat2.insert(10,zaehleFiles)

        ##
        
        Threat1.grid(row=1, column=1)
        Threat2.grid(row=2, column=1)
        Threat3.grid(row=3, column=1)
        Threat4.grid(row=4, column=1)
 
        
 
        area.grid(row=1, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
 
        # Button Browse
        abtn = Button(self, text="Browse", command=lambda:BrowseButtonClass(value))
        abtn.grid(row=1, column=3)
 
        #Button Close
        cbtn = Button(self, text="Close", command=CloseButtonClass)
        cbtn.grid(row=2, column=3, pady=4)
 
        #Button Help
        hbtn = Button(self, text="Help", command=HelpButtonClass)
        hbtn.grid(row=5, column=0, padx=5)
 
        #Button Go
        obtn = Button(self, text="GO", command=GoButtonClass)
        obtn.grid(row=5, column=3)
         
 
def main():
 
    root = Tk()
    root.geometry("600x200+300+300")
    app = MapillaryGui(root)
    ######## 26-10-2015 ######
    label = tk.Label(root, fg="dark green")
    label.pack()
    ### counter_label(label)
    ### zaehleFiles
    ######## 26-10-2015 ENDE ######
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
 
