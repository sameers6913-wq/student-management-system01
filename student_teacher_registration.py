import customtkinter as ctk
from tkinter import messagebox

from database import create_connection


class RegistrationPage(ctk.CTkFrame):

    def __init__(self, parent, back_to_login):
        super().__init__(
            parent,
            fg_color="#071A2B",
            corner_radius=0
        )

        self.back_to_login = back_to_login

        self.create_ui()

    # ======================================================
    # MAIN UI
    # ======================================================

    def create_ui(self):

        background = ctk.CTkFrame(
            self,
            fg_color="#071A2B",
            corner_radius=0
        )

        background.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # CARD
        # ==================================================

        card = ctk.CTkFrame(
            background,
            corner_radius=25,
            fg_color="#10283D",
            border_width=1,
            border_color="#1E405C"
        )

        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        # ==================================================
        # SCROLLABLE CONTENT
        # ==================================================

        scroll = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # ==================================================
        # BACK TO LOGIN
        # ==================================================

        back_button = ctk.CTkButton(
            scroll,
            text="←  BACK TO LOGIN",
            height=38,
            width=170,
            corner_radius=9,
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            hover_color="#17364E",
            border_width=1,
            border_color="#294860",
            text_color="#91CFF5",
            command=self.back_to_login
        )

        back_button.pack(
            anchor="w",
            pady=(0, 15)
        )

        # ==================================================
        # HEADER
        # ==================================================

        title = ctk.CTkLabel(
            scroll,
            text="Create Account",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        )

        title.pack(
            anchor="w",
            pady=(5, 3)
        )

        subtitle = ctk.CTkLabel(
            scroll,
            text="Create your academic portal account",
            font=("Arial", 13),
            text_color="#91A9BB"
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 22)
        )

        # ==================================================
        # ACCOUNT TYPE
        # ==================================================

        type_label = ctk.CTkLabel(
            scroll,
            text="ACCOUNT TYPE",
            font=("Arial", 11, "bold"),
            text_color="#BFD0DE"
        )

        type_label.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.account_type = ctk.CTkComboBox(
            scroll,
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#294860",
            fg_color="#0A1E30",
            button_color="#1769AA",
            button_hover_color="#2187C7",
            dropdown_fg_color="#10283D",
            dropdown_hover_color="#17364E",
            dropdown_text_color="white",
            text_color="white",
            values=[
                "Student",
                "Teacher"
            ],
            font=("Arial", 14)
        )

        self.account_type.set("Student")

        self.account_type.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # STUDENT / TEACHER ID
        # ==================================================

        id_label = ctk.CTkLabel(
            scroll,
            text="STUDENT / TEACHER ID",
            font=("Arial", 11, "bold"),
            text_color="#BFD0DE"
        )

        id_label.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.id_entry = ctk.CTkEntry(
            scroll,
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#294860",
            fg_color="#0A1E30",
            text_color="white",
            placeholder_text="Enter your registered ID",
            placeholder_text_color="#60798D",
            font=("Arial", 14)
        )

        self.id_entry.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # USERNAME
        # ==================================================

        username_label = ctk.CTkLabel(
            scroll,
            text="USERNAME",
            font=("Arial", 11, "bold"),
            text_color="#BFD0DE"
        )

        username_label.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.username_entry = ctk.CTkEntry(
            scroll,
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#294860",
            fg_color="#0A1E30",
            text_color="white",
            placeholder_text="Create your username",
            placeholder_text_color="#60798D",
            font=("Arial", 14)
        )

        self.username_entry.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # PASSWORD
        # ==================================================

        password_label = ctk.CTkLabel(
            scroll,
            text="PASSWORD",
            font=("Arial", 11, "bold"),
            text_color="#BFD0DE"
        )

        password_label.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.password_entry = ctk.CTkEntry(
            scroll,
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#294860",
            fg_color="#0A1E30",
            text_color="white",
            placeholder_text="Create your password",
            placeholder_text_color="#60798D",
            show="*",
            font=("Arial", 14)
        )

        self.password_entry.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # CONFIRM PASSWORD
        # ==================================================

        confirm_label = ctk.CTkLabel(
            scroll,
            text="CONFIRM PASSWORD",
            font=("Arial", 11, "bold"),
            text_color="#BFD0DE"
        )

        confirm_label.pack(
            anchor="w",
            pady=(0, 6)
        )

        self.confirm_entry = ctk.CTkEntry(
            scroll,
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#294860",
            fg_color="#0A1E30",
            text_color="white",
            placeholder_text="Confirm your password",
            placeholder_text_color="#60798D",
            show="*",
            font=("Arial", 14)
        )

        self.confirm_entry.pack(
            fill="x",
            pady=(0, 22)
        )

        # ==================================================
        # CREATE ACCOUNT BUTTON
        # ==================================================

        create_button = ctk.CTkButton(
            scroll,
            text="CREATE ACCOUNT  →",
            height=52,
            corner_radius=10,
            font=("Arial", 16, "bold"),
            fg_color="#1687D9",
            hover_color="#0F6EBA",
            text_color="white",
            command=self.create_account
        )

        create_button.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==================================================
        # INFORMATION
        # ==================================================

        info = ctk.CTkLabel(
            scroll,
            text="Your ID must be registered by the administrator.",
            font=("Arial", 11),
            text_color="#718DA2"
        )

        info.pack(
            pady=(0, 15)
        )

    # ======================================================
    # CREATE ACCOUNT
    # ======================================================

    def create_account(self):

        account_type = self.account_type.get().strip()
        person_id = self.id_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        # ==================================================
        # VALIDATION
        # ==================================================

        if not person_id:

            messagebox.showwarning(
                "Missing Information",
                "Please enter your Student ID or Teacher ID.",
                parent=self
            )

            return

        if not username:

            messagebox.showwarning(
                "Missing Information",
                "Please create a username.",
                parent=self
            )

            return

        if not password:

            messagebox.showwarning(
                "Missing Information",
                "Please create a password.",
                parent=self
            )

            return

        if not confirm_password:

            messagebox.showwarning(
                "Missing Information",
                "Please confirm your password.",
                parent=self
            )

            return

        if password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters.",
                parent=self
            )

            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to MySQL database.",
                    parent=self
                )

                return

            cursor = connection.cursor()

            # ==================================================
            # CHECK REGISTERED PERSON
            # ==================================================

            if account_type == "Student":

                cursor.execute(
                    """
                    SELECT student_id, full_name
                    FROM students
                    WHERE student_id = %s
                    """,
                    (person_id,)
                )

            else:

                cursor.execute(
                    """
                    SELECT teacher_id, full_name
                    FROM teachers
                    WHERE teacher_id = %s
                    """,
                    (person_id,)
                )

            person = cursor.fetchone()

            if not person:

                messagebox.showerror(
                    "Registration Not Found",
                    f"No registered {account_type.lower()} was found "
                    f"with ID:\n{person_id}\n\n"
                    "Please contact the administrator.",
                    parent=self
                )

                return

            # ==================================================
            # CHECK USERNAME
            # ==================================================

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            existing_username = cursor.fetchone()

            if existing_username:

                messagebox.showerror(
                    "Username Already Exists",
                    "This username is already in use.\n"
                    "Please choose another username.",
                    parent=self
                )

                return

            # ==================================================
            # CHECK EXISTING ACCOUNT
            # ==================================================

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE person_id = %s
                AND role = %s
                """,
                (
                    person_id,
                    account_type
                )
            )

            existing_account = cursor.fetchone()

            if existing_account:

                messagebox.showerror(
                    "Account Already Exists",
                    f"This {account_type.lower()} already has an account.",
                    parent=self
                )

                return

            # ==================================================
            # CREATE ACCOUNT
            # ==================================================

            cursor.execute(
                """
                INSERT INTO users
                (username, password, role, full_name, status, person_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    username,
                    password,
                    account_type,
                    person[1],
                    "Active",
                    person_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Account Created",
                f"Account created successfully!\n\n"
                f"Name: {person[1]}\n"
                f"Username: {username}\n"
                f"Role: {account_type}\n"
                f"ID: {person_id}",
                parent=self
            )

            # Go back to login page
            self.back_to_login()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Error",
                f"Something went wrong:\n{e}",
                parent=self
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()