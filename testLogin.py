import tkinter as tk
from components.login import show_login_dialog

root = tk.Tk()
root.withdraw()
if show_login_dialog(root):
    root.deiconify()
    tk.Label(root, text="Đăng nhập thành công!", font=("Helvetica", 16)).pack(padx=30, pady=30)
    root.mainloop()
else:
    root.destroy()