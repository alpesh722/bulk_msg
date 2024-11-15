# import all functions from the tkinter    
import csv
import time
import threading
import pywhatkit
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class WpMsg:
    def __init__(self):        
        self.country_code = "+91"
        self.wait_time_1 = 65
        self.close_time_1 = 70
        self.wait_time = 8
        self.close_time = 10
        self.image =""
        self.num_list=[]
        self.message_list = []
        # self.time_list = []
        self.message_text = ""  
        self.var = "Status" 
        self.csv_path = "No file selected..!"
        self.img_path = ""       

    
    def sendMessage(self) :          
        result = "Successful" 
        error = "ERROR: Sending Interupted..."          
        try:
            if self.message_list[1] != "":
                message = self.message_list[1]        
        except IndexError:
            # self.var.set("WARNING: Select proper CSV file")    
            message = self.TextArea.get(1.0,END)
        
        print("Message: {}".format(message))
        if message == "":
            self.var.set("WARNING: Not any Text message found")
            return False
        
        schedule_time = self.set_timeField.get() #self.time_list[1]
        if schedule_time != '':   
            hour = int(schedule_time[:2])
            minut = int(schedule_time[3:])        
            print("Scheduled Time: ",self.set_timeField.get())
        
        if self.num_list == []:
            self.var.set("WARNING: Select proper CSV file") 
            return False

        count = 0
        try:
            for contact in self.num_list[1:]:
                count += 1
                contact = self.country_code+contact
                if self.image == "y":

                    if (schedule_time != '') or (not contact[1:].isdigit()):
                        error = """ERROR:Not Possible Image/scheduled-time/whatsapp-group together."""                        
                        raise ValueError(error)                        
                    else:
                        if count == 1:
                            pywhatkit.sendwhats_image(contact, "{}".format(self.image_file), 
                                                      message, self.wait_time_1, 
                                                      True, self.close_time_1)
                            time.sleep(60)
                        else:
                            pywhatkit.sendwhats_image(contact, "{}".format(self.image_file), 
                                                      message, self.wait_time, 
                                                      True, self.close_time)
                else:  
                    print("Only Text message without Image !!!")      
                    if count == 1:
                        if not contact[1:].isdigit() :
                            if schedule_time != '':
                                pywhatkit.sendwhatmsg_to_group(contact, message, 
                                                               hour, minut, 
                                                               self.wait_time_1, 
                                                               True, self.close_time_1)                    
                            else:
                                pywhatkit.sendwhatmsg_to_group_instantly(contact, 
                                                                    message, 
                                                                    self.wait_time_1, 
                                                                    True, 
                                                                    self.close_time_1)             
                        else:
                            if schedule_time != '':
                                pywhatkit.sendwhatmsg(contact, message, hour, 
                                                      minut , self.wait_time_1, 
                                                      True, self.close_time_1)                    
                            else:
                                pywhatkit.sendwhatmsg_instantly(contact, message, 
                                                                self.wait_time_1, 
                                                                True, self.close_time_1)
                        time.sleep(60)
                    else:
                        if not contact[1:].isdigit() :                           
                            pywhatkit.sendwhatmsg_to_group_instantly(contact, 
                                                                    message, 
                                                                    self.wait_time, 
                                                                    True, 
                                                                    self.close_time)             
                        else:                            
                            pywhatkit.sendwhatmsg_instantly(contact, message, 
                                                            self.wait_time, 
                                                            True, self.close_time)
            
            # self.sendField.insert(10, str(result)) 
            self.var.set(result)
        except Exception as e:
            self.var.set(error)
            # self.sendField.insert(10, str(error))
            print("ERROR: Sending Interupted...")

        print("+++++ Completed. +++++")         
        
    # Function for clearing the contents of all text entry boxes 
    def Clear(self): 

        self.num_list = []
        self.message_list = []
        self.image = ""
        self.set_timeField.delete(0,'end')
        self.TextArea.delete(1.0,END)        
        self.var.set("Status")   
        self.csv_path.set("")
        self.img_path.set("")  

    # Function to open a specific .csv file
    def open_csv_file(self):
        num = []
        msg = []
        t_list = []    
        file_path = filedialog.askopenfilename(defaultextension=".csv", 
                                               filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path.set(str(file_path.split("/")[-1]))  
            self.var.set("Status") 
            try:
                with open(file_path, "r") as csv_file:
                    # Read and display the CSV file's contents
                    csvFile = csv.reader(csv_file)
                    for line in csvFile:    
                        _num=line[0].strip()
                        num.append(_num)
                        msg.append(line[1])
                        # t_list.append(line[2])                    
                self.num_list = num
                self.message_list = msg
                # self.time_list = t_list
            except Exception as e:
                print(f"Error: {e}")  
        if self.message_list[1] != "":
            self.TextArea.insert(END,self.message_list[1])
        else:
            self.TextArea.insert(END,"Write Text Message Here..!")

    # Define the function to upload and save the image
    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img_path.set(str(file_path.split("/")[-1]))
            self.image_file = Image.open(file_path)
            # image.thumbnail((300, 300))  # Resize image if necessary
            # photo = ImageTk.PhotoImage(image)
            # self.image_label.config(image=photo)
            # self.image_label.image = photo  # Keep a reference to avoid garbage 
            # save_image(file_path)
            # messagebox.showinfo(&quot;Success&quot;, &quot;Image uploaded successfully!&quot;)
            if self.image_file:
                self.image = "y"

                                
    def main(self):
        # Create a GUI window 
        gui = Tk()   
        
        gui.configure(background = "light grey")    
        gui.title("WhatsApp- Bulk Message Sender")    
        gui.geometry("900x500")   
        self.var = StringVar()
        self.csv_path = StringVar()
        self.img_path = StringVar()
        csv_text = Label(gui,text = " Browse CSV File for numbers :",
                         bg = "Light Grey", font=("TimesNewRoman",10))                       
        message = Label(gui,text = " Message :",bg = "Light Grey",
                        font=("TimesNewRoman",10))                 
        set_time = Label(gui,text = "Enter Schedule Time If required :", 
                         bg = "Light Grey", font=("TimesNewRoman",10)) 
        img_text = Label(gui,text = " Do you Want to send Photo/Image? ",
                         bg = "Light Grey", font=("TimesNewRoman",10)) 
        self.send_lable =   Label(gui,textvariable=self.var, bg = "Dark Grey",
                                height=2, width = 63) 
        self.csv_status = Label(gui,textvariable=self.csv_path, bg = "Light Grey",
                                height=2, width = 20, font=("TimesNewRoman",10)) 
        self.img_status = Label(gui,textvariable=self.img_path, bg = "Light Grey",
                                height=2, width = 20, font=("TimesNewRoman",10)) 
        self.TextArea = Text(gui, height = 5, width = 55)
        # Create a button to open the .csv file
        open_button = Button(gui, text="Click Here to Upload CSV file", 
                            command=self.open_csv_file)   
        upload_button = Button(gui, text="Click Here to Upload Image", 
                               command=self.upload_image)        
        clear = Button(gui, text = "   Clear   ", bg = "Dark Grey",
                       command = self.Clear)    #fg = "Black",  
        # Threading is used to avoid GUI not responding issue
        # lambda func is used to avoid RuntimeError: threads can only be started once                   
        send = Button(gui, text = "   Send   ", bg = "Dark Grey",
                    command = lambda:threading.Thread(target=self.sendMessage).start())  
        

        csv_text.grid(row = 15, column = 20, padx = 10, pady = 20, ipady = 5)
        open_button.grid(row = 15, column = 25, padx = 10, pady = 20, ipady = 5) 
        self.csv_status.grid(row = 15, column = 26, ipady = 5, sticky='w') 
        img_text.grid(row = 35, column = 20, padx = 10, pady = 20, ipady = 5)     
        upload_button.grid(row = 35, column = 25, padx = 10, pady = 20, ipady = 5)
        self.img_status.grid(row = 35, column = 26, ipady = 5, sticky='w')  
        set_time.grid(row = 45, column = 20, padx = 10,  pady = 20, ipady = 5)
        message.grid(row = 55, column = 20, padx = 10, pady = 20, ipady = 5) 
        self.TextArea.grid(row = 55, column = 25, columnspan=5, sticky='w')          
        send.grid(row = 75, column = 20, padx = 10, pady = 20, ipady = 5) 
        clear.grid(row = 95, column = 20,padx = 10, pady = 20, ipady = 5)      
        
        self.set_timeField = Entry(gui)        
        # self.sendField = Entry(gui)            
        
        self.set_timeField.grid(row = 45, column = 25, ipady = 5, sticky='w')
        # self.sendField.grid(row = 75, column = 25, ipadx= 160, ipady = 20)  
        self.send_lable.grid(row = 75, column = 25, columnspan=2, sticky='w')
        
        
        # Start the GUI 
        gui.mainloop() 

# Driver Code
if __name__ == "__main__" :
    # root = Tk()
    # wp_gui = WpMsg(root)
    # root.mainloop()
    test = WpMsg()
    test.main()
  
    