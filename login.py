import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from database import create_connection

from gui.admin_dashboard import AdminDashboard
from gui.teacher_dashboard import TeacherDashboard
from gui.student_dashboard import StudentDashboard
from student_teacher_registration import RegistrationPage


class LoginApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==================================================
        # WINDOW
        # ==================================================

        self.title("Student Management System")
        self.geometry("1200x720")
        self.minsize(1050, 650)
        self.resizable(True, True)

        # ==================================================
        # APPEARANCE
        # ==================================================

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#DCE8F0")

        self.login_page = None
        self.registration_page = None

        self.show_login_page()

    # ======================================================
    # SHOW LOGIN PAGE
    # ======================================================

    def show_login_page(self):

        if self.registration_page is not None:
            self.registration_page.destroy()
            self.registration_page = None

        if self.login_page is not None:
            self.login_page.destroy()

        self.login_page = ctk.CTkFrame(
            self,
            fg_color="#DCE8F0",
            corner_radius=0
        )

        self.login_page.pack(
            fill="both",
            expand=True
        )

        self.create_login_ui()

    # ======================================================
    # CREATE LOGIN UI
    # ======================================================

    def create_login_ui(self):

        background = self.login_page

        # ==================================================
        # MAIN CONTAINER
        # ==================================================

        main = ctk.CTkFrame(
            background,
            fg_color="transparent"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=45
        )

        # ==================================================
        # LEFT BRANDING PANEL
        # ==================================================

        branding = ctk.CTkFrame(
            main,
            width=470,
            corner_radius=28,
            fg_color="#17324D"
        )

        branding.pack(
            side="left",
            fill="both",
            padx=(0, 30)
        )

        branding.pack_propagate(False)

        # ==================================================
        # TOP ACCENT
        # ==================================================

        accent = ctk.CTkFrame(
            branding,
            height=5,
            corner_radius=3,
            fg_color="#4B86A5"
        )

        accent.pack(
            fill="x",
            padx=45,
            pady=(30, 0)
        )

        # ==================================================
        # LOGO
        # ==================================================

        logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "logo.png"
        )

        if os.path.exists(logo_path):

            try:

                logo_image = Image.open(logo_path)

                self.logo = ctk.CTkImage(
                    light_image=logo_image,
                    dark_image=logo_image,
                    size=(180, 180)
                )

                logo_label = ctk.CTkLabel(
                    branding,
                    image=self.logo,
                    text=""
                )

                logo_label.pack(
                    pady=(40, 15)
                )

            except Exception:

                logo_label = ctk.CTkLabel(
                    branding,
                    text="COLLEGE",
                    font=("Arial", 28, "bold"),
                    text_color="#F2F5F7"
                )

                logo_label.pack(
                    pady=(55, 30)
                )

        else:

            logo_label = ctk.CTkLabel(
                branding,
                text="COLLEGE",
                font=("Arial", 28, "bold"),
                text_color="#F2F5F7"
            )

            logo_label.pack(
                pady=(55, 30)
            )

        # ==================================================
        # BRAND TITLE
        # ==================================================

        title = ctk.CTkLabel(
            branding,
            text="STUDENT\nMANAGEMENT\nSYSTEM",
            font=("Arial", 32, "bold"),
            text_color="#F4F7F9",
            justify="center"
        )

        title.pack(
            pady=(15, 12)
        )

        # ==================================================
        # DIVIDER
        # ==================================================

        line = ctk.CTkFrame(
            branding,
            width=75,
            height=4,
            corner_radius=2,
            fg_color="#4B86A5"
        )

        line.pack(
            pady=(8, 25)
        )

        # ==================================================
        # SMALL BRAND TEXT
        # ==================================================

        portal_text = ctk.CTkLabel(
            branding,
            text="ACADEMIC MANAGEMENT PORTAL",
            font=("Arial", 13, "bold"),
            text_color="#B8CAD6"
        )

        portal_text.pack(
            pady=(0, 8)
        )

        tagline = ctk.CTkLabel(
            branding,
            text="Secure  •  Simple  •  Connected",
            font=("Arial", 12),
            text_color="#8FA9BA"
        )

        tagline.pack(
            pady=(0, 20)
        )

        # ==================================================
        # RIGHT LOGIN CARD
        # ==================================================

        card = ctk.CTkFrame(
            main,
            width=440,
            corner_radius=25,
            fg_color="#F5F7F9",
            border_width=1,
            border_color="#C5D2DA"
        )

        card.pack(
            side="right",
            fill="both",
            expand=True
        )

        card.pack_propagate(False)

        # ==================================================
        # CARD CONTENT
        # ==================================================

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=42
        )

        # ==================================================
        # LOGIN HEADER
        # ==================================================

        welcome = ctk.CTkLabel(
            content,
            text="Welcome Back",
            font=("Arial", 30, "bold"),
            text_color="#243746"
        )

        welcome.pack(
            anchor="w",
            pady=(8, 5)
        )

        subtitle = ctk.CTkLabel(
            content,
            text="Sign in to access your dashboard",
            font=("Arial", 14),
            text_color="#657987"
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 30)
        )

        # ==================================================
        # USERNAME LABEL
        # ==================================================

        username_label = ctk.CTkLabel(
            content,
            text="USERNAME",
            font=("Arial", 11, "bold"),
            text_color="#405665"
        )

        username_label.pack(
            anchor="w",
            pady=(0, 7)
        )

        # ==================================================
        # USERNAME FRAME
        # ==================================================

        username_frame = ctk.CTkFrame(
            content,
            height=50,
            corner_radius=10,
            fg_color="#E8EEF2",
            border_width=1,
            border_color="#C5D2DA"
        )

        username_frame.pack(
            fill="x",
            pady=(0, 18)
        )

        username_frame.pack_propagate(False)

        username_icon = ctk.CTkLabel(
            username_frame,
            text="👤",
            font=("Arial", 16),
            text_color="#4B86A5"
        )

        username_icon.pack(
            side="left",
            padx=(14, 5)
        )

        self.username_entry = ctk.CTkEntry(
            username_frame,
            height=46,
            corner_radius=0,
            border_width=0,
            fg_color="transparent",
            text_color="#243746",
            placeholder_text="Enter username",
            placeholder_text_color="#81929D",
            font=("Arial", 14)
        )

        self.username_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(3, 10)
        )

        # ==================================================
        # PASSWORD LABEL
        # ==================================================

        password_label = ctk.CTkLabel(
            content,
            text="PASSWORD",
            font=("Arial", 11, "bold"),
            text_color="#405665"
        )

        password_label.pack(
            anchor="w",
            pady=(0, 7)
        )

        # ==================================================
        # PASSWORD FRAME
        # ==================================================

        password_frame = ctk.CTkFrame(
            content,
            height=50,
            corner_radius=10,
            fg_color="#E8EEF2",
            border_width=1,
            border_color="#C5D2DA"
        )

        password_frame.pack(
            fill="x",
            pady=(0, 18)
        )

        password_frame.pack_propagate(False)

        password_icon = ctk.CTkLabel(
            password_frame,
            text="🔒",
            font=("Arial", 15),
            text_color="#4B86A5"
        )

        password_icon.pack(
            side="left",
            padx=(14, 5)
        )

        self.password_entry = ctk.CTkEntry(
            password_frame,
            height=46,
            corner_radius=0,
            border_width=0,
            fg_color="transparent",
            text_color="#243746",
            placeholder_text="Enter password",
            placeholder_text_color="#81929D",
            show="*",
            font=("Arial", 14)
        )

        self.password_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(3, 5)
        )

        # ==================================================
        # SHOW / HIDE PASSWORD
        # ==================================================

        self.password_visible = False

        self.eye_button = ctk.CTkButton(
            password_frame,
            text="◉",
            width=35,
            height=35,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#D4E0E6",
            text_color="#5C788A",
            font=("Arial", 15),
            command=self.toggle_password
        )

        self.eye_button.pack(
            side="right",
            padx=(0, 7)
        )

        # ==================================================
        # ROLE LABEL
        # ==================================================

        role_label = ctk.CTkLabel(
            content,
            text="LOGIN AS",
            font=("Arial", 11, "bold"),
            text_color="#405665"
        )

        role_label.pack(
            anchor="w",
            pady=(0, 7)
        )

        # ==================================================
        # ROLE DROPDOWN
        # ==================================================

        self.role_menu = ctk.CTkComboBox(
            content,
            height=50,
            corner_radius=10,
            border_width=1,
            border_color="#C5D2DA",
            fg_color="#E8EEF2",
            button_color="#4B86A5",
            button_hover_color="#3D718D",
            dropdown_fg_color="#F5F7F9",
            dropdown_hover_color="#DCE7ED",
            dropdown_text_color="#243746",
            text_color="#243746",
            values=[
                "Administrator",
                "Teacher",
                "Student"
            ],
            font=("Arial", 14)
        )

        self.role_menu.set("Administrator")

        self.role_menu.pack(
            fill="x",
            pady=(0, 28)
        )

        # ==================================================
        # SIGN IN BUTTON
        # ==================================================

        login_button = ctk.CTkButton(
            content,
            text="SIGN IN   →",
            height=52,
            corner_radius=10,
            font=("Arial", 16, "bold"),
            fg_color="#4B86A5",
            hover_color="#3D718D",
            text_color="#FFFFFF",
            command=self.login
        )

        login_button.pack(
            fill="x",
            pady=(0, 12)
        )

        # ==================================================
        # CREATE ACCOUNT BUTTON
        # ==================================================

        create_account_button = ctk.CTkButton(
            content,
            text="CREATE ACCOUNT",
            height=42,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            fg_color="transparent",
            hover_color="#DCE7ED",
            border_width=1,
            border_color="#7C9BAD",
            text_color="#4B7186",
            command=self.show_registration_page
        )

        create_account_button.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # SECURITY INFORMATION
        # ==================================================

        security = ctk.CTkLabel(
            content,
            text="🔐  Secure academic management portal",
            font=("Arial", 12),
            text_color="#728692"
        )

        security.pack(
            pady=(3, 0)
        )

        # ==================================================
        # ENTER KEY
        # ==================================================

        self.bind(
            "<Return>",
            lambda event: self.login()
        )

        # ==================================================
        # FOCUS USERNAME
        # ==================================================

        self.after(
            300,
            lambda: self.username_entry.focus()
        )

    # ======================================================
    # SHOW REGISTRATION PAGE
    # ======================================================

    def show_registration_page(self):

        if self.login_page is not None:

            self.login_page.destroy()

            self.login_page = None

        self.registration_page = RegistrationPage(
            self,
            self.show_login_page
        )

        self.registration_page.pack(
            fill="both",
            expand=True
        )

        self.after(
            300,
            lambda: self.registration_page.id_entry.focus()
        )

    # ======================================================
    # SHOW / HIDE PASSWORD
    # ======================================================

    def toggle_password(self):

        if self.password_visible:

            self.password_entry.configure(
                show="*"
            )

            self.password_visible = False

        else:

            self.password_entry.configure(
                show=""
            )

            self.password_visible = True

    # ======================================================
    # LOGIN THROUGH LOCAL MYSQL
    # ======================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_menu.get()

        # ==================================================
        # VALIDATE INPUT
        # ==================================================

        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )

            return

        connection = None
        cursor = None

        try:

            # ==================================================
            # CONNECT TO LOCAL MYSQL
            # ==================================================

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to the local MySQL database.\n\n"
                    "Please check your MySQL server and database.py."
                )

                return

            # ==================================================
            # CREATE CURSOR
            # ==================================================

            cursor = connection.cursor(
                dictionary=True
            )

            # ==================================================
            # LOGIN QUERY
            # ==================================================

            query = """
                SELECT *
                FROM users
                WHERE username = %s
                AND password = %s
                AND role = %s
                LIMIT 1
            """

            cursor.execute(
                query,
                (
                    username,
                    password,
                    role
                )
            )

            user = cursor.fetchone()

            # ==================================================
            # LOGIN FAILED
            # ==================================================

            if not user:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username, password, or role."
                )

                return

            # ==================================================
            # ACCOUNT STATUS CHECK
            # ==================================================

            if user.get("status") != "Active":

                messagebox.showerror(
                    "Access Denied",
                    "Your account is inactive.\n"
                    "Please contact the administrator."
                )

                return

            # ==================================================
            # CHECK STUDENT / TEACHER PERSON ID
            # ==================================================

            if user.get("role") in (
                "Student",
                "Teacher"
            ):

                if not user.get("person_id"):

                    messagebox.showerror(
                        "Account Configuration Error",
                        "Your account is not properly linked to "
                        "your Student/Teacher ID.\n\n"
                        "Please contact the administrator."
                    )

                    return

            # ==================================================
            # LOGIN SUCCESS
            # ==================================================

            full_name = user.get(
                "full_name",
                username
            )

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {full_name}!"
            )

            # ==================================================
            # CLOSE LOGIN WINDOW
            # ==================================================

            self.destroy()

            # ==================================================
            # ADMINISTRATOR
            # ==================================================

            if user.get("role") == "Administrator":

                dashboard = AdminDashboard(
                    full_name=full_name
                )

                dashboard.mainloop()

            # ==================================================
            # TEACHER
            # ==================================================

            elif user.get("role") == "Teacher":

                dashboard = TeacherDashboard(
                    teacher_name=full_name,
                    teacher_id=user.get("person_id")
                )

                dashboard.mainloop()

            # ==================================================
            # STUDENT
            # ==================================================

            elif user.get("role") == "Student":

                dashboard = StudentDashboard(
                    student_id=user.get("person_id"),
                    student_name=full_name
                )

                dashboard.mainloop()

        # ======================================================
        # DATABASE / OTHER ERROR
        # ======================================================

        except Exception as e:

            messagebox.showerror(
                "Login Error",
                f"Something went wrong:\n\n{e}"
            )

        # ======================================================
        # CLOSE DATABASE CONNECTION
        # ======================================================

        finally:

            try:

                if cursor:
                    cursor.close()

            except Exception:
                pass

            try:

                if connection:
                    connection.close()

            except Exception:
                pass


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    app = LoginApp()
    app.mainloop()