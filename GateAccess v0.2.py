import tkinter as tk
import time
import threading
from sys import exit
import requests
import json


def main():
    startButton.config(state='disabled')
    t = time.localtime()
    user_input = id_entry.get()
    current_time = time.strftime("%H:%M:%S - ", t)
    if len(user_input)>8:
        entryresult=user_access(user_input)
        if entryresult['ArrivalAdded']:
            open_gates()
        response_listbox.insert(tk.END, current_time+user_input+"  "+str(entryresult))
        response_listbox.yview(tk.END)

        id_entry.delete(0, tk.END)
        root.after(5000, main)
    else:

        root.after(2000, main) 

def user_access(user_input):
    url = 'https://api.com/add_customer_arrival'
    response = requests.post('https://address_for_dynamic_key.com/key.json')
    authorization=response.json()
    auth_key=authorization['AccessToken']

    headers = {
        'API-Key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'Accept': 'application/json',
        'Site': '1234',
        'Content-Type': 'application/json',
        'authorization': auth_key,
    }

    data = {
        'CustomerId': user_input,
        'LocationId': 3,
        'RegisterAccessId': 123,
        'Test': False,
    }
    try:
    # Make the request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return str(response.json())
    except requests.exceptions.Timeout as e:
        return f"Timeout error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def open_gates():
    # Make an HTTP request to a gate on the network
    url = 'http://192.168.1.94/api/opengate'
    response = requests.post(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Parse the JSON response
            json_result = response.json()

            # Display the result
            result=(json.dumps(json_result, indent=2))
            response_listbox.insert(tk.END, result)
            response_listbox.yview(tk.END)
        except json.JSONDecodeError:
            print('Error decoding JSON response')
    else:
        print('Error:', response.status_code)

def startThread():
    startButton.config(state='disabled')
    threading.Thread(target=main, args=(), daemon=True).start()

def endThread():
    exit()
    
def reset_script():
    # Restart the script by destroying the current Tkinter window and creating a new one
    root.destroy()
    create_gui()

def create_gui():
    global root, startButton, endScript, id_entry, response_listbox

    # Create the Tkinter window
    root = tk.Tk()
    root.title("Gate Access")
    root.geometry("900x600+100+100")

    # Set dark grey background color
    root.configure(bg="#303030")


    # Title label
    title_label = tk.Label(root, text="Gate Access", bg="#303030", fg="white", font=("Arial", 16))
    title_label.pack(pady=10)

    openButton = tk.Button(root, text=' Open Gate ', fg="white", bg="#181A1C", command=open_gates)
    openButton.pack(pady=10)

    # ID's field
    id_entry = tk.Entry(root, bg="white", fg="black", font=("Arial", 12))
    id_entry.pack(pady=10)
    id_entry.focus_set()
    id_entry.focus_force()
    
    # Buttons frame
    button_frame = tk.Frame(root, bg="#303030")
    button_frame.pack()

    startButton = tk.Button(button_frame, text='Start', fg="white", bg="#181A1C", command=startThread)
    startButton.pack(side=tk.LEFT, padx=5, pady=10)

    endScript = tk.Button(button_frame, text='End', fg="white", bg="#181A1C", command=endThread)
    endScript.pack(side=tk.LEFT, padx=5, pady=10)

    # Response window with history
    response_frame = tk.Frame(root, bg="black")
    response_frame.pack(fill="both", expand=True)

    response_listbox = tk.Listbox(response_frame, bg="black", fg="white", font=("Arial", 8), selectbackground="#303030", selectforeground="white")
    response_listbox.pack(fill="both", expand=True)

    # Make the response window always cover the entire bottom half of the GUI
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(3, weight=1)
    # Enabled as client wants the program always-on 
    root.after(2000, startButton.invoke)

    # Schedule the script reset every 24 hours (86400000 milliseconds)
    root.after(86400000, reset_script)
    
    # Start the Tkinter event loop
    root.mainloop()

# Create the GUI for the first time
create_gui()