import wmi
import logging
from tkinter import *
from tkinter import messagebox
import os
from time import sleep

logging.basicConfig(filename='opc_services_restart.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.basicConfig(filename='opc_services_restart.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# ---------------------------- CONSTANTS ------------------------------- #
NAVY = "#334257"
LIGHT_NAVY = "#476072"
DARK_BLUE = "#548CA8"
GRAY = "#EEEEEE"
FONT = ("Courier", 12, "normal")
remote_pc = "None"
SERVICES = ["OPCServer.WinCC", "OpcEnum"]

# ---------------------------- FUNCTIONS ------------------------------- #
def current_user():
    return os.getlogin()


def reading_config_file():
    try:
        with open("configuration.txt", "r") as config_data:
            temp = config_data.readlines()
    except FileNotFoundError:
        logging.error(f"[!] File 'configuration.txt' wasn't found.")
        messagebox.showerror("Oops", message="Couldn't find configuration file")
    else:
        servers = []
        for record in temp[1::]:
            for server in record.split(","):
                servers.append(server.split("=")[1])
        logging.info(f"[+] Reading from the file completed successfully. Servers list: {servers}")
        return servers[0], servers[1]


def radiobutton_1():
    global remote_pc
    remote_pc = pc_1


def radiobutton_2():
    global remote_pc
    remote_pc = pc_2


def service_state(connection, service_name):
    if len(connection.Win32_Service(Name=service_name, State="Running")) != 0:
        return 1
    else:
        logging.error(f"[!] Seems that service {service_name} was stopped before app started running.")
        return False


def getting_list_of_services(connection):
    list_of_services = []
    for service in connection.Win32_Service():
        list_of_services.append(service.Name)

        with open("list_of_services.txt", "w") as data_file:
            for service in list_of_services:
                data_file.write(f"{service}\n")

def stop_service(connection, service_name):
    for service in connection.Win32_Service(Name=service_name):
        result, = service.StopService()
        if result == 0:
            logging.info(f"[+] Service {service.Name} was stopped.")
        else:
            logging.error(f"[!] Some issue with {service.Name} appeared.")
        break
    else:
        logging.error(f"[!] Service {service_name} wasn't found.")

def start_service(connection, service_name):
    for service in connection.Win32_Service(Name=service_name):
        result, = service.StartService()
        if result == 0:
            logging.info(f"[+] Service {service.Name} was started.")
        else:
            logging.error(f"[!] Some issue with {service.Name} appeared.")
        break
    else:
        logging.error(f"[!] Service {service_name} wasn't found.")


def services_restart(connection, service_name):
    # TODO Need to add logging for each action the function does
    if service_state(connection, service_name) == 1:
        stop_service(connection, service_name)
        start_service(connection, service_name)
    else:
        start_service(connection, service_name)


def remote_connection():
    global remote_pc, SERVICES
    try:
        connection = wmi.WMI(remote_pc, user=r"pcg\svcbackups", password="pcgbackups")
        logging.info(f"[+] The user '{current_user()}' initiated services reboot. The reason: '{e_comment.get()}'.")
    except:
        logging.error(f"[!] Couldn't connect to the server {remote_pc}.")
        messagebox.showerror(title="Error!", message=f"Couldn't connect to the server {remote_pc}")
    else:
        # TODO I need to be able to reboot 2 services 2 times each
        # service_state(connection, "WSearch")
        for service in SERVICES:
            services_restart(connection, service)
        sleep(10)
        for service in SERVICES:
            services_restart(connection, service)
        messagebox.showinfo(title="Success!", message=f"Restart of services on the {remote_pc} was done successfully!")
        logging.info(f"Restart of services on the {remote_pc} was done successfully!")
    finally:
        ...

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

# Radiobuttons
# pc_1, pc_2 = reading_config_file()[0], reading_config_file()[1]  # the function return a list where I'm using only
pc_1, pc_2 = reading_config_file()

radio_state = StringVar()
rb_server1 = Radiobutton(text=pc_1, value=1, variable=radio_state, command=radiobutton_1)
rb_server1.grid(column=0, row=3)
rb_server1.config(indicatoron=0, bd=4, width=12)

rb_server2 = Radiobutton(text=pc_2, value=2, variable=radio_state, command=radiobutton_2)
rb_server2.grid(column=1, row=3)
rb_server2.config(indicatoron=0, bd=4, width=12)

# Buttons
b_services_restart = Button(text="Restart", font=FONT, bg=GRAY, activebackground=DARK_BLUE, width=28,
                            command=remote_connection)
b_services_restart.grid(column=0, row=4, pady=(5, 5), columnspan=2)

window.mainloop()
# for record in reading_config_file():
#     print(record[0])
# print(reading_config_file())
# checkbutton_used()
# messagebox.showinfo(title="Done!", message=f"This server was chose {checkbutton_used()}")
# print("Hello World!")

# ---------------------------- LOGIC ------------------------------- #


# pc = input("Please, indicate the name of the PC: ")
# user = input("Please, indicate the user: ")
# password = input("Please, indicate the password: ")

# list_of_services = []
# for service in connection.Win32_Service():
#     list_of_services.append(service.Name)
#
#     with open("list_of_services.txt", "w") as data_file:
#         for service in list_of_services:
#             data_file.write(f"{service}\n")

# connection.Win32_Process.Create(CommandLine='cmd.exe taskkill /pid 3644 /F')


# result = connection.Win32_Process.Create(CommandLine='cmd.exe ipconfig')
# print(result)
