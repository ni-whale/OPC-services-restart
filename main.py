import wmi
import logging
from tkinter import *
from tkinter import messagebox
import os


def main():
    logging.basicConfig(filename='opc_services_restart.log', level=logging.INFO, format='%(asctime)s %(message)s')

    # ---------------------------- CONSTANTS ------------------------------- #
    NAVY = "#334257"
    LIGHT_NAVY = "#476072"
    DARK_BLUE = "#548CA8"
    GRAY = "#EEEEEE"
    FONT = ("Courier", 12, "normal")

    # ---------------------------- FUNCTIONS ------------------------------- #
    def current_user():
        return os.getlogin()

    def checkbutton_used():
        print(radio_state.get())

    def reading_config_file():
        with open("configuration.txt", "r") as config_data:
            temp = config_data.readlines()
        servers = []
        for record in temp[1::]:
            servers.append((record.split("=")[1::])[0])
        return servers

    def remote_connection():
        ...

    # ---------------------------- LOGIC ------------------------------- #

    # pc = input("Please, indicate the name of the PC: ")
    # user = input("Please, indicate the user: ")
    # password = input("Please, indicate the password: ")

    # connection = wmi.WMI("192.168.31.19", user=r"admin", password="p@ssword")
    # connection = wmi.WMI(pc, user=user, password=password)
    # list_of_services = []
    # for service in connection.Win32_Service():
    #     list_of_services.append(service.Name)
    #
    #     with open("list_of_services.txt", "w") as data_file:
    #         for service in list_of_services:
    #             data_file.write(f"{service}\n")

    # connection.Win32_Process.Create(CommandLine='cmd.exe taskkill /pid 3644 /F')

    # for service in connection.Win32_Service(Name="WSearch"):
    #   result, = service.StartService()
    #   if result == 0:
    #     print("Service", service.Name, "started")
    #   else:
    #     print("Some problem")
    #   break
    # else:
    #   print("Service not found")

    # result = connection.Win32_Process.Create(CommandLine='cmd.exe ipconfig')
    # print(result)

    # ---------------------------- UI SETUP ------------------------------- #
    window = Tk()
    window.title("OPC services restart")
    window.config(padx=20, pady=20, bg=NAVY)

    # Canvas
    canvas = Canvas(width=250, height=250, bg=NAVY, highlightthickness=0)
    gear_logo = PhotoImage(file="img/Black Minimal Electronics Logo.png")
    canvas.create_image(125, 125, image=gear_logo)
    canvas.grid(column=0, row=0, columnspan=2)

    # Labels
    l_comment = Label(text="Indicate the reason for restart", font=FONT, bg=NAVY, fg=GRAY)
    l_comment.grid(column=0, row=1, columnspan=2)

    # Entries
    e_comment = Entry(width=48, bg=GRAY)
    e_comment.focus()
    e_comment.grid(column=0, row=2, pady=(5, 5), columnspan=2)

    def test1():
        print("server1")

    def test2():
        print("server2")

    # Radiobuttons
    radio_state = StringVar()
    rb_server1 = Radiobutton(text="Server1", value="test1", variable=radio_state, command=test1)
    rb_server1.grid(column=0, row=3)
    rb_server1.config(indicatoron=0, bd=4, width=12)

    rb_server2 = Radiobutton(text="Server2", value="test2", variable=radio_state, command=test2)
    rb_server2.grid(column=1, row=3)
    rb_server2.config(indicatoron=0, bd=4, width=12)

    # Buttons
    b_services_restart = Button(text="Restart", font=FONT, bg=GRAY, activebackground=DARK_BLUE, width=28,
                                command=...)
    b_services_restart.grid(column=0, row=4, pady=(5, 5), columnspan=2)
    window.mainloop()
    # for record in reading_config_file():
    #     print(record[0])
    # print(reading_config_file())
    # checkbutton_used()
    messagebox.showinfo(title="Done!", message=f"This server was chose {checkbutton_used()}")
    # print("Hello World!")



main()
