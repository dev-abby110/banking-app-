import tkinter as tk
from tkinter import ttk
from Banking.account import SavingsAccount, CurrentAccount
from Banking.transactions import deposit, withdraw

accounts = {}

# Dark theme colors
BG_COLOR = "#23272f"
FG_COLOR = "#f5f6fa"
BTN_BG = "#353b48"
BTN_FG = "#f5f6fa"
ENTRY_BG = "#2f3640"
ENTRY_FG = "#f5f6fa"
ACCENT = "#00a8ff"
ERROR_COLOR = "#e84118"

def style_widget(widget):
    widget.configure(bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground=BG_COLOR)

def dark_style_ttk():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
        fieldbackground=ENTRY_BG,
        background=ENTRY_BG,
        foreground=ENTRY_FG,
        selectbackground=ENTRY_BG,
        selectforeground=ENTRY_FG,
        arrowcolor=ACCENT,
        bordercolor=BG_COLOR,
        lightcolor=BG_COLOR,
        darkcolor=BG_COLOR,
        borderwidth=0,
        relief="flat"
    )
    style.map("TCombobox",
        fieldbackground=[('readonly', ENTRY_BG)],
        foreground=[('readonly', ENTRY_FG)],
        background=[('readonly', ENTRY_BG)]
    )

class DarkSimpleDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.result = None
        self.grab_set()
        self.transient(parent)
        tk.Label(self, text=prompt, bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12)).pack(padx=18, pady=(18, 8))
        self.entry = tk.Entry(self, font=("Segoe UI", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, relief="flat")
        self.entry.pack(padx=18, pady=8)
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=(8, 18))
        tk.Button(btn_frame, text="OK", width=8, font=("Segoe UI", 11, "bold"),
                  bg=ACCENT, fg=BG_COLOR, activebackground=BTN_BG, activeforeground=FG_COLOR,
                  bd=0, relief="flat", command=self.ok, cursor="hand2").pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", width=8, font=("Segoe UI", 11),
                  bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                  bd=0, relief="flat", command=self.cancel, cursor="hand2").pack(side="left", padx=6)
        self.entry.focus_set()
        self.bind("<Return>", lambda e: self.ok())
        self.bind("<Escape>", lambda e: self.cancel())
        self.wait_window(self)

    def ok(self):
        try:
            self.result = float(self.entry.get())
        except ValueError:
            self.result = None
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

def dark_messagebox(parent, title, message, error=False):
    win = tk.Toplevel(parent)
    win.title(title)
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    win.grab_set()
    win.transient(parent)
    fg = ERROR_COLOR if error else FG_COLOR
    tk.Label(win, text=message, bg=BG_COLOR, fg=fg, font=("Segoe UI", 12)).pack(padx=22, pady=(22, 14))
    tk.Button(win, text="OK", width=10, font=("Segoe UI", 11, "bold"),
              bg=ACCENT, fg=BG_COLOR, activebackground=BTN_BG, activeforeground=FG_COLOR,
              bd=0, relief="flat", command=win.destroy, cursor="hand2").pack(pady=(0, 18))
    win.wait_window(win)

class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Of Ro706 - Banking System")
        self.root.configure(bg=BG_COLOR)
        self.current_account = None

        dark_style_ttk()

        self.container = tk.Frame(root, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainMenu, CreateAccountFrame, LoginFrame, DashboardFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if frame_class == DashboardFrame:
            frame.refresh()

    def set_current_account(self, account):
        self.current_account = account

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="Bank Of Ro706 - Banking System", font=("Segoe UI", 18, "bold"),
                 bg=BG_COLOR, fg=ACCENT).pack(pady=(30, 15))
        for text, cmd in [
            ("Create Account", lambda: controller.show_frame(CreateAccountFrame)),
            ("Login", lambda: controller.show_frame(LoginFrame)),
            ("Exit", controller.root.quit)
        ]:
            btn = tk.Button(self, text=text, width=22, font=("Segoe UI", 12, "bold"),
                            bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                            bd=0, relief="flat", command=cmd, cursor="hand2")
            btn.pack(pady=8)

class CreateAccountFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="Create Account", font=("Segoe UI", 16, "bold"),
                 bg=BG_COLOR, fg=ACCENT).grid(row=0, column=0, columnspan=2, pady=(25, 15))

        tk.Label(self, text="Account Holder's Name:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = tk.Entry(self, font=("Segoe UI", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, relief="flat")
        self.name_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(self, text="Account Type:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.type_var = tk.StringVar(value="Savings")
        type_menu = ttk.Combobox(self, textvariable=self.type_var, values=["Savings", "Current"], font=("Segoe UI", 12), state="readonly")
        type_menu.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Initial Deposit:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.deposit_entry = tk.Entry(self, font=("Segoe UI", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, relief="flat")
        self.deposit_entry.grid(row=3, column=1, pady=5, padx=10)

        btn_create = tk.Button(self, text="Create", font=("Segoe UI", 12, "bold"),
                              bg=ACCENT, fg=BG_COLOR, activebackground=BTN_BG, activeforeground=FG_COLOR,
                              bd=0, relief="flat", command=self.submit, cursor="hand2")
        btn_create.grid(row=4, column=0, columnspan=2, pady=(18, 8), ipadx=10)

        btn_back = tk.Button(self, text="Back", font=("Segoe UI", 11),
                            bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                            bd=0, relief="flat", command=lambda: controller.show_frame(MainMenu), cursor="hand2")
        btn_back.grid(row=5, column=0, columnspan=2, pady=2, ipadx=10)

    def submit(self):
        name = self.name_entry.get().strip()
        account_type = self.type_var.get().lower()
        try:
            initial_deposit = float(self.deposit_entry.get())
        except ValueError:
            dark_messagebox(self, "Error", "Invalid deposit amount.", error=True)
            return
        if account_type == "savings":
            account = SavingsAccount(name, balance=initial_deposit)
        elif account_type == "current":
            account = CurrentAccount(name, balance=initial_deposit)
        else:
            dark_messagebox(self, "Error", "Invalid account type.", error=True)
            return
        accounts[account.account_number] = account
        dark_messagebox(self, "Success", f"Account created successfully!\nAccount Number: {account.account_number}")
        self.name_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)
        self.controller.show_frame(MainMenu)

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="Login", font=("Segoe UI", 16, "bold"),
                 bg=BG_COLOR, fg=ACCENT).pack(pady=(30, 10))
        tk.Label(self, text="Enter your account number:", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12)).pack(pady=5)
        self.acc_entry = tk.Entry(self, font=("Segoe UI", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, relief="flat")
        self.acc_entry.pack(pady=5)

        btn_login = tk.Button(self, text="Login", font=("Segoe UI", 12, "bold"),
                             bg=ACCENT, fg=BG_COLOR, activebackground=BTN_BG, activeforeground=FG_COLOR,
                             bd=0, relief="flat", command=self.login, cursor="hand2")
        btn_login.pack(pady=(15, 5), ipadx=10)

        btn_back = tk.Button(self, text="Back", font=("Segoe UI", 11),
                            bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                            bd=0, relief="flat", command=lambda: controller.show_frame(MainMenu), cursor="hand2")
        btn_back.pack(pady=2, ipadx=10)

    def login(self):
        try:
            acc_num = int(self.acc_entry.get())
        except ValueError:
            dark_messagebox(self, "Error", "Invalid account number.", error=True)
            return
        if acc_num in accounts:
            self.controller.set_current_account(accounts[acc_num])
            self.acc_entry.delete(0, tk.END)
            self.controller.show_frame(DashboardFrame)
        else:
            dark_messagebox(self, "Error", "Account not found. Please create an account first.", error=True)

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        self.title_label = tk.Label(self, font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=ACCENT)
        self.title_label.pack(pady=(25, 10))

        self.balance_var = tk.StringVar()
        tk.Label(self, textvariable=self.balance_var, font=("Segoe UI", 13), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

        btn_deposit = tk.Button(self, text="Deposit", width=22, font=("Segoe UI", 12, "bold"),
                                bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                                bd=0, relief="flat", command=self.do_deposit, cursor="hand2")
        btn_deposit.pack(pady=6)

        btn_withdraw = tk.Button(self, text="Withdraw", width=22, font=("Segoe UI", 12, "bold"),
                                 bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                                 bd=0, relief="flat", command=self.do_withdraw, cursor="hand2")
        btn_withdraw.pack(pady=6)

        btn_check = tk.Button(self, text="Check Balance", width=22, font=("Segoe UI", 12, "bold"),
                              bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                              bd=0, relief="flat", command=self.refresh, cursor="hand2")
        btn_check.pack(pady=6)

        self.interest_btn = tk.Button(self, text="Calculate Interest", width=22, font=("Segoe UI", 12, "bold"),
                                      bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT, activeforeground=BG_COLOR,
                                      bd=0, relief="flat", command=self.do_interest, cursor="hand2")
        self.interest_btn.pack(pady=6)

        btn_logout = tk.Button(self, text="Logout", width=22, font=("Segoe UI", 12, "bold"),
                               bg=ACCENT, fg=BG_COLOR, activebackground=BTN_BG, activeforeground=FG_COLOR,
                               bd=0, relief="flat", command=lambda: controller.show_frame(MainMenu), cursor="hand2")
        btn_logout.pack(pady=(18, 10))

    def refresh(self):
        acc = self.controller.current_account
        self.title_label.config(text=f"Welcome {acc.name} to the Bank Of Ro706")
        self.balance_var.set(f"Current Balance: {acc.get_balance()}")
        if isinstance(acc, SavingsAccount):
            self.interest_btn.config(state="normal")
        else:
            self.interest_btn.config(state="disabled")

    def do_deposit(self):
        dlg = DarkSimpleDialog(self, "Deposit", "Enter deposit amount:")
        amount = dlg.result
        if amount is not None:
            deposit(self.controller.current_account, amount)
            self.refresh()
            dark_messagebox(self, "Success", "Deposit successful.")

    def do_withdraw(self):
        dlg = DarkSimpleDialog(self, "Withdraw", "Enter withdrawal amount:")
        amount = dlg.result
        if amount is not None:
            try:
                withdraw(self.controller.current_account, amount)
                self.refresh()
                dark_messagebox(self, "Success", "Withdrawal successful.")
            except Exception as e:
                dark_messagebox(self, "Error", str(e), error=True)

    def do_interest(self):
        self.controller.current_account.calculate_interest()
        self.refresh()
        dark_messagebox(self, "Interest", "Interest calculated and added to balance.")

def main():
    root = tk.Tk()
    root.geometry("420x500")
    app = BankingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()