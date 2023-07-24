import tkinter
import customtkinter
import webbrowser
import threading
import os


def Start():

    print('EyeGaze is launching...')

    webbrowser.open('http://127.0.0.1:5000')
    os.system('flask run')


def Stop():
    print('EyeGaze is stopping...')

    os.system('taskkill -f -im python*')


def start_thread():
    global start_thread_status
    start_thread_status = threading.Thread(target=Start)
    start_thread_status.daemon = True
    start_thread_status.start()
    app.after(20, check_start_thread)


def check_start_thread():
    if start_thread_status.is_alive():
        app.after(20, check_start_thread)


def change_appearance_mode(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


def on_closing(self, event=0):
    self.destroy()


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x380")
app.title("EyeGazer")
app.iconbitmap(r"./static/images/EyeGazer.ico")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=50, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(
    master=frame_1, justify=tkinter.LEFT, text="EyeGazer",  text_font=("Roboto Medium", -16))
label_1.pack(pady=22, padx=10)

button_1 = customtkinter.CTkButton(
    master=frame_1, text="Start", command=lambda: start_thread())
button_1.pack(pady=12, padx=10)

button_2 = customtkinter.CTkButton(master=frame_1, text="Stop", command=Stop)
button_2.pack(pady=12, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(master=frame_1, values=[
                                           "Light", "Dark", "System"], command=change_appearance_mode)
optionmenu_1.pack(pady=12, padx=10)
optionmenu_1.set("Dark")

app.mainloop()
