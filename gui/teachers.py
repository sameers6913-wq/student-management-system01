import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_connection


# =========================================================
# TEACHER MANAGEMENT
# =========================================================

class TeachersPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.selected_id = None
        self.subject_map = {}

        self.configure(
            fg_color="#F5F7FA"
        )

        self.build_ui()

        self.load_subjects()
        self.load_teachers()

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=0
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="Teacher Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#162B40"
        )

        title.pack(
            side="left",
            padx=25,
            pady=20
        )

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        self.search_entry = ctk.CTkEntry(
            header,
            width=300,
            height=40,
            placeholder_text="Search teachers..."
        )

        self.search_entry.pack(
            side="right",
            padx=(10, 20),
            pady=20
        )

        search_button = ctk.CTkButton(
            header,
            text="Search",
            width=100,
            height=40,
            command=self.search_teachers
        )

        search_button.pack(
            side="right",
            padx=5,
            pady=20
        )

        refresh_button = ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_teachers
        )

        refresh_button.pack(
            side="right",
            padx=5,
            pady=20
        )

        # -------------------------------------------------
        # FORM
        # -------------------------------------------------

        form = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        form.pack(
            fill="x",
            padx=20,
            pady=10
        )

        form_title = ctk.CTkLabel(
            form,
            text="Teacher Details",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color="#162B40"
        )

        form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=25,
            pady=(20, 15)
        )

        # -------------------------------------------------
        # TEACHER ID
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Teacher ID"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=25,
            pady=8
        )

        self.teacher_id_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.teacher_id_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # FULL NAME
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Full Name"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=25,
            pady=8
        )

        self.full_name_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.full_name_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # EMAIL
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Email"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=25,
            pady=8
        )

        self.email_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.email_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # PHONE
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Phone"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=25,
            pady=8
        )

        self.phone_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.phone_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # GENDER
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Gender"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=25,
            pady=8
        )

        self.gender_combo = ctk.CTkComboBox(
            form,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            width=250,
            height=38
        )

        self.gender_combo.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # DEPARTMENT
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Department"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=25,
            pady=8
        )

        self.department_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.department_entry.grid(
            row=3,
            column=3,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # DESIGNATION
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Designation"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=25,
            pady=8
        )

        self.designation_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.designation_entry.grid(
            row=4,
            column=1,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # SUBJECT
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Subject"
        ).grid(
            row=4,
            column=2,
            sticky="w",
            padx=25,
            pady=8
        )

        self.subject_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."],
            width=250,
            height=38
        )

        self.subject_combo.grid(
            row=4,
            column=3,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # QUALIFICATION
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Qualification"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=25,
            pady=8
        )

        self.qualification_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.qualification_entry.grid(
            row=5,
            column=1,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # ADDRESS
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Address"
        ).grid(
            row=5,
            column=2,
            sticky="w",
            padx=25,
            pady=8
        )

        self.address_entry = ctk.CTkEntry(
            form,
            width=250,
            height=38
        )

        self.address_entry.grid(
            row=5,
            column=3,
            padx=10,
            pady=8
        )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=6,
            column=0,
            columnspan=4,
            pady=(15, 20)
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Teacher",
            width=150,
            height=40,
            command=self.save_teacher
        )

        save_button.pack(
            side="left",
            padx=8
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=40,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.clear_form
        )

        cancel_button.pack(
            side="left",
            padx=8
        )

        # -------------------------------------------------
        # TABLE FRAME
        # -------------------------------------------------

        table_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        # -------------------------------------------------
        # TREEVIEW STYLE
        # -------------------------------------------------

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        # -------------------------------------------------
        # SCROLLBARS
        # -------------------------------------------------

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        columns = (
            "id",
            "teacher_id",
            "full_name",
            "email",
            "phone",
            "gender",
            "department",
            "designation",
            "subject",
            "qualification",
            "address"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.config(
            command=self.tree.yview
        )

        scrollbar_x.config(
            command=self.tree.xview
        )

        headings = {
            "id": "ID",
            "teacher_id": "Teacher ID",
            "full_name": "Full Name",
            "email": "Email",
            "phone": "Phone",
            "gender": "Gender",
            "department": "Department",
            "designation": "Designation",
            "subject": "Subject",
            "qualification": "Qualification",
            "address": "Address"
        }

        widths = {
            "id": 60,
            "teacher_id": 110,
            "full_name": 160,
            "email": 200,
            "phone": 120,
            "gender": 90,
            "department": 120,
            "designation": 140,
            "subject": 140,
            "qualification": 150,
            "address": 220
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_teacher
        )

        self.tree.bind(
            "<Double-1>",
            self.edit_teacher
        )

    # =====================================================
    # LOAD SUBJECTS FROM LOCAL MYSQL
    # =====================================================

    def load_subjects(self):

        connection = create_connection()

        if connection is None:

            self.subject_combo.configure(
                values=["Database unavailable"]
            )

            self.subject_combo.set(
                "Database unavailable"
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    subject_code,
                    subject_name
                FROM subjects
                ORDER BY subject_name ASC
            """)

            subjects = cursor.fetchall()

            self.subject_map = {}

            values = []

            for subject in subjects:

                code = subject[0] or ""
                name = subject[1] or ""

                display = f"{code} - {name}"

                self.subject_map[display] = code

                values.append(display)

            if values:

                self.subject_combo.configure(
                    values=values
                )

                self.subject_combo.set(
                    values[0]
                )

            else:

                self.subject_combo.configure(
                    values=["No subjects found"]
                )

                self.subject_combo.set(
                    "No subjects found"
                )

        except Exception as e:

            self.subject_combo.configure(
                values=["Unable to load subjects"]
            )

            self.subject_combo.set(
                "Unable to load subjects"
            )

            messagebox.showerror(
                "Database Error",
                f"Unable to load subjects.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # SAVE TEACHER
    # =====================================================

    def save_teacher(self):

        teacher_id = self.teacher_id_entry.get().strip()
        full_name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        gender = self.gender_combo.get().strip()
        department = self.department_entry.get().strip()
        designation = self.designation_entry.get().strip()
        qualification = self.qualification_entry.get().strip()
        address = self.address_entry.get().strip()

        subject_display = self.subject_combo.get().strip()

        subject_code = self.subject_map.get(
            subject_display,
            subject_display
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not teacher_id:

            messagebox.showwarning(
                "Validation",
                "Please enter Teacher ID."
            )

            return

        if not full_name:

            messagebox.showwarning(
                "Validation",
                "Please enter Full Name."
            )

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Connection Error",
                "Unable to connect to local MySQL database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            # -------------------------------------------------
            # UPDATE
            # -------------------------------------------------

            if self.selected_id is not None:

                cursor.execute("""
                    UPDATE teachers
                    SET
                        teacher_id = %s,
                        full_name = %s,
                        email = %s,
                        phone = %s,
                        gender = %s,
                        department = %s,
                        designation = %s,
                        subject = %s,
                        qualification = %s,
                        address = %s
                    WHERE id = %s
                """, (
                    teacher_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    department,
                    designation,
                    subject_code,
                    qualification,
                    address,
                    self.selected_id
                ))

            # -------------------------------------------------
            # INSERT
            # -------------------------------------------------

            else:

                cursor.execute("""
                    INSERT INTO teachers
                    (
                        teacher_id,
                        full_name,
                        email,
                        phone,
                        gender,
                        department,
                        designation,
                        subject,
                        qualification,
                        address
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """, (
                    teacher_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    department,
                    designation,
                    subject_code,
                    qualification,
                    address
                ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Teacher saved successfully."
            )

            self.clear_form()

            self.load_subjects()
            self.load_teachers()

        except Exception as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # LOAD TEACHERS FROM LOCAL MYSQL
    # =====================================================

    def load_teachers(self):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Connection Error",
                "Unable to connect to local MySQL database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    teacher_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    department,
                    designation,
                    subject,
                    qualification,
                    address
                FROM teachers
                ORDER BY id ASC
            """)

            teachers = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for teacher in teachers:

                values = (
                    teacher[0] or "",
                    teacher[1] or "",
                    teacher[2] or "",
                    teacher[3] or "",
                    teacher[4] or "",
                    teacher[5] or "",
                    teacher[6] or "",
                    teacher[7] or "",
                    teacher[8] or "",
                    teacher[9] or "",
                    teacher[10] or ""
                )

                self.tree.insert(
                    "",
                    "end",
                    values=values
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load teachers.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # SEARCH TEACHERS
    # =====================================================

    def search_teachers(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_teachers()

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Connection Error",
                "Unable to connect to local MySQL database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            search_value = f"%{search_text}%"

            cursor.execute("""
                SELECT
                    id,
                    teacher_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    department,
                    designation,
                    subject,
                    qualification,
                    address
                FROM teachers
                WHERE teacher_id LIKE %s
                   OR full_name LIKE %s
                   OR email LIKE %s
                   OR department LIKE %s
                   OR designation LIKE %s
                ORDER BY id ASC
            """, (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))

            teachers = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for teacher in teachers:

                values = (
                    teacher[0] or "",
                    teacher[1] or "",
                    teacher[2] or "",
                    teacher[3] or "",
                    teacher[4] or "",
                    teacher[5] or "",
                    teacher[6] or "",
                    teacher[7] or "",
                    teacher[8] or "",
                    teacher[9] or "",
                    teacher[10] or ""
                )

                self.tree.insert(
                    "",
                    "end",
                    values=values
                )

            if not teachers:

                messagebox.showinfo(
                    "Search",
                    "No matching teachers found."
                )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # SELECT TEACHER
    # =====================================================

    def select_teacher(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:
            return

        self.selected_id = values[0]

    # =====================================================
    # EDIT TEACHER
    # =====================================================

    def edit_teacher(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:
            return

        self.selected_id = values[0]

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Connection Error",
                "Unable to connect to local MySQL database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    teacher_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    department,
                    designation,
                    subject,
                    qualification,
                    address
                FROM teachers
                WHERE id = %s
                LIMIT 1
            """, (
                self.selected_id,
            ))

            teacher = cursor.fetchone()

            if not teacher:

                messagebox.showerror(
                    "Error",
                    "Teacher record not found."
                )

                return

            # -------------------------------------------------
            # FILL FORM
            # -------------------------------------------------

            self.teacher_id_entry.delete(
                0,
                "end"
            )

            self.teacher_id_entry.insert(
                0,
                teacher[1] or ""
            )

            self.full_name_entry.delete(
                0,
                "end"
            )

            self.full_name_entry.insert(
                0,
                teacher[2] or ""
            )

            self.email_entry.delete(
                0,
                "end"
            )

            self.email_entry.insert(
                0,
                teacher[3] or ""
            )

            self.phone_entry.delete(
                0,
                "end"
            )

            self.phone_entry.insert(
                0,
                teacher[4] or ""
            )

            self.gender_combo.set(
                teacher[5] or "Male"
            )

            self.department_entry.delete(
                0,
                "end"
            )

            self.department_entry.insert(
                0,
                teacher[6] or ""
            )

            self.designation_entry.delete(
                0,
                "end"
            )

            self.designation_entry.insert(
                0,
                teacher[7] or ""
            )

            self.qualification_entry.delete(
                0,
                "end"
            )

            self.qualification_entry.insert(
                0,
                teacher[9] or ""
            )

            self.address_entry.delete(
                0,
                "end"
            )

            self.address_entry.insert(
                0,
                teacher[10] or ""
            )

            # -------------------------------------------------
            # SUBJECT
            # -------------------------------------------------

            subject_code = teacher[8] or ""

            found_subject = False

            for display, code in self.subject_map.items():

                if str(code) == str(subject_code):

                    self.subject_combo.set(
                        display
                    )

                    found_subject = True
                    break

            if not found_subject and subject_code:

                self.subject_combo.set(
                    subject_code
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.selected_id = None

        self.teacher_id_entry.delete(
            0,
            "end"
        )

        self.full_name_entry.delete(
            0,
            "end"
        )

        self.email_entry.delete(
            0,
            "end"
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.gender_combo.set(
            "Male"
        )

        self.department_entry.delete(
            0,
            "end"
        )

        self.designation_entry.delete(
            0,
            "end"
        )

        self.qualification_entry.delete(
            0,
            "end"
        )

        self.address_entry.delete(
            0,
            "end"
        )

        if self.subject_map:

            first_subject = next(
                iter(self.subject_map)
            )

            self.subject_combo.set(
                first_subject
            )


# =========================================================
# TEST WINDOW
# =========================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "Teacher Management - Student Management System"
    )

    root.geometry(
        "1450x850"
    )

    root.minsize(
        1200,
        700
    )

    page = TeachersPage(
        root
    )

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()