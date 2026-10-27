import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_connection


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F4F7FB"
        )

        self.create_ui()
        self.load_students()

    # =====================================================
    # MAIN UI
    # =====================================================

    def create_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(25, 15)
        )

        title = ctk.CTkLabel(
            header,
            text="Student Management",
            font=("Arial", 26, "bold"),
            text_color="#17202A"
        )

        title.pack(
            side="left",
            padx=20,
            pady=20
        )

        add_button = ctk.CTkButton(
            header,
            text="+ Add Student",
            width=150,
            height=40,
            corner_radius=10,
            command=self.show_add_form
        )

        add_button.pack(
            side="right",
            padx=20
        )

        # =================================================
        # SEARCH
        # =================================================

        search_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by Student ID or Name...",
            width=350,
            height=40
        )

        self.search_entry.pack(
            side="left",
            padx=20,
            pady=15
        )

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            height=40,
            command=self.search_students
        )

        search_button.pack(
            side="left",
            padx=5
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_students
        )

        refresh_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # TABLE
        # =================================================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = (
            "id",
            "student_id",
            "full_name",
            "email",
            "phone",
            "gender",
            "course",
            "semester"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "student_id": "Student ID",
            "full_name": "Full Name",
            "email": "Email",
            "phone": "Phone",
            "gender": "Gender",
            "course": "Course",
            "semester": "Semester"
        }

        widths = {
            "id": 50,
            "student_id": 100,
            "full_name": 170,
            "email": 180,
            "phone": 110,
            "gender": 90,
            "course": 100,
            "semester": 80
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
            padx=15,
            pady=15
        )

        # =================================================
        # ACTION BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit Selected",
            width=130,
            height=40,
            command=self.edit_student
        )

        edit_button.pack(
            side="left",
            padx=5
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            width=130,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_student
        )

        delete_button.pack(
            side="left",
            padx=5
        )

    # =====================================================
    # LOAD STUDENTS FROM LOCAL MYSQL
    # =====================================================

    def load_students(self):

        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

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
                    student_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    course,
                    semester
                FROM students
                ORDER BY id ASC
            """)

            students = cursor.fetchall()

            for student in students:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        student[0],
                        student[1],
                        student[2],
                        student[3] or "",
                        student[4] or "",
                        student[5] or "",
                        student[6] or "",
                        student[7] or ""
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # SEARCH STUDENTS
    # =====================================================

    def search_students(self):

        search = self.search_entry.get().strip()

        if not search:

            self.load_students()

            return

        for item in self.tree.get_children():
            self.tree.delete(item)

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

            search_value = f"%{search}%"

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    course,
                    semester
                FROM students
                WHERE student_id LIKE %s
                   OR full_name LIKE %s
                ORDER BY id ASC
            """, (
                search_value,
                search_value
            ))

            students = cursor.fetchall()

            for student in students:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        student[0],
                        student[1],
                        student[2],
                        student[3] or "",
                        student[4] or "",
                        student[5] or "",
                        student[6] or "",
                        student[7] or ""
                    )
                )

            if not students:

                messagebox.showinfo(
                    "Search",
                    "No matching students found."
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
    # SHOW ADD FORM
    # =====================================================

    def show_add_form(self):

        self.show_form()

    # =====================================================
    # SHOW FORM
    # =====================================================

    def show_form(self, student_data=None):

        for widget in self.winfo_children():
            widget.pack_forget()

        form_container = ctk.CTkFrame(
            self,
            fg_color="#F4F7FB"
        )

        form_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        form_header = ctk.CTkFrame(
            form_container,
            fg_color="white",
            corner_radius=15
        )

        form_header.pack(
            fill="x",
            pady=(0, 15)
        )

        title_text = (
            "Edit Student"
            if student_data
            else "Add New Student"
        )

        title = ctk.CTkLabel(
            form_header,
            text=title_text,
            font=("Arial", 26, "bold"),
            text_color="#17202A"
        )

        title.pack(
            side="left",
            padx=20,
            pady=20
        )

        back_button = ctk.CTkButton(
            form_header,
            text="← Back",
            width=100,
            height=38,
            command=lambda: self.close_form(
                form_container
            )
        )

        back_button.pack(
            side="right",
            padx=20
        )

        body = ctk.CTkFrame(
            form_container,
            fg_color="white",
            corner_radius=15
        )

        body.pack(
            fill="both",
            expand=True
        )

        left = ctk.CTkFrame(
            body,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(30, 15),
            pady=25
        )

        right = ctk.CTkFrame(
            body,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(15, 30),
            pady=25
        )

        self.student_id_entry = self.create_field(
            left,
            "Student ID"
        )

        self.full_name_entry = self.create_field(
            left,
            "Full Name"
        )

        self.email_entry = self.create_field(
            left,
            "Email"
        )

        self.phone_entry = self.create_field(
            left,
            "Phone"
        )

        gender_label = ctk.CTkLabel(
            left,
            text="Gender",
            font=("Arial", 13),
            text_color="#475467"
        )

        gender_label.pack(
            anchor="w",
            pady=(10, 5)
        )

        self.gender_combo = ctk.CTkComboBox(
            left,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            height=40
        )

        self.gender_combo.pack(
            fill="x",
            pady=(0, 10)
        )

        self.dob_entry = self.create_field(
            right,
            "Date of Birth (YYYY-MM-DD)"
        )

        self.course_entry = self.create_field(
            right,
            "Course"
        )

        semester_label = ctk.CTkLabel(
            right,
            text="Semester",
            font=("Arial", 13),
            text_color="#475467"
        )

        semester_label.pack(
            anchor="w",
            pady=(10, 5)
        )

        self.semester_combo = ctk.CTkComboBox(
            right,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8"
            ],
            height=40
        )

        self.semester_combo.pack(
            fill="x",
            pady=(0, 10)
        )

        self.address_entry = self.create_field(
            right,
            "Address"
        )

        save_button = ctk.CTkButton(
            body,
            text="Save Student",
            width=200,
            height=45,
            corner_radius=10,
            command=lambda: self.save_student(
                student_data,
                form_container
            )
        )

        save_button.pack(
            side="bottom",
            pady=25
        )

        if student_data:

            self.fill_form(student_data)

        else:

            self.gender_combo.set("Male")
            self.semester_combo.set("1")

    # =====================================================
    # CREATE FIELD
    # =====================================================

    def create_field(
        self,
        parent,
        placeholder
    ):

        label = ctk.CTkLabel(
            parent,
            text=placeholder,
            font=("Arial", 13),
            text_color="#475467"
        )

        label.pack(
            anchor="w",
            pady=(10, 5)
        )

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=40
        )

        entry.pack(
            fill="x",
            pady=(0, 10)
        )

        return entry

    # =====================================================
    # FILL EDIT FORM
    # =====================================================

    def fill_form(self, data):

        self.student_id_entry.insert(
            0,
            data[1]
        )

        self.full_name_entry.insert(
            0,
            data[2]
        )

        self.email_entry.insert(
            0,
            data[3] or ""
        )

        self.phone_entry.insert(
            0,
            data[4] or ""
        )

        self.gender_combo.set(
            data[5] or "Male"
        )

        self.course_entry.insert(
            0,
            data[6] or ""
        )

        self.semester_combo.set(
            str(data[7])
            if data[7]
            else "1"
        )

        # Get DOB and address directly from MySQL

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    date_of_birth,
                    address
                FROM students
                WHERE student_id = %s
                LIMIT 1
            """, (
                data[1],
            ))

            student = cursor.fetchone()

            if student:

                self.dob_entry.insert(
                    0,
                    str(student[0])
                    if student[0]
                    else ""
                )

                self.address_entry.insert(
                    0,
                    student[1]
                    if student[1]
                    else ""
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
    # SAVE STUDENT
    # =====================================================

    def save_student(
        self,
        student_data,
        form_container
    ):

        student_id = self.student_id_entry.get().strip()
        full_name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        gender = self.gender_combo.get().strip()
        dob = self.dob_entry.get().strip()
        course = self.course_entry.get().strip()
        semester = self.semester_combo.get().strip()
        address = self.address_entry.get().strip()

        # =================================================
        # VALIDATION
        # =================================================

        if not student_id:

            messagebox.showwarning(
                "Required Field",
                "Please enter Student ID."
            )

            return

        if not full_name:

            messagebox.showwarning(
                "Required Field",
                "Please enter Full Name."
            )

            return

        # Convert empty DOB to NULL

        dob_value = dob if dob else None

        # Convert semester to integer

        try:

            semester_value = int(semester)

        except ValueError:

            messagebox.showwarning(
                "Invalid Semester",
                "Please select a valid semester."
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

            # =================================================
            # UPDATE EXISTING STUDENT
            # =================================================

            if student_data:

                old_student_id = student_data[1]

                cursor.execute("""
                    UPDATE students
                    SET
                        student_id = %s,
                        full_name = %s,
                        email = %s,
                        phone = %s,
                        gender = %s,
                        date_of_birth = %s,
                        course = %s,
                        semester = %s,
                        address = %s
                    WHERE student_id = %s
                """, (
                    student_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    dob_value,
                    course,
                    semester_value,
                    address,
                    old_student_id
                ))

            # =================================================
            # INSERT NEW STUDENT
            # =================================================

            else:

                cursor.execute("""
                    INSERT INTO students
                    (
                        student_id,
                        full_name,
                        email,
                        phone,
                        gender,
                        date_of_birth,
                        course,
                        semester,
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
                        %s
                    )
                """, (
                    student_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    dob_value,
                    course,
                    semester_value,
                    address
                ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student saved successfully."
            )

            self.close_form(
                form_container
            )

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
    # CLOSE FORM
    # =====================================================

    def close_form(
        self,
        form_container
    ):

        form_container.destroy()

        self.create_ui()

        self.load_students()

    # =====================================================
    # EDIT STUDENT
    # =====================================================

    def edit_student(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.show_form(values)

    # =====================================================
    # DELETE STUDENT
    # =====================================================

    def delete_student(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        student_id = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete student {student_id}?"
        )

        if not confirm:
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

            cursor.execute("""
                DELETE FROM students
                WHERE student_id = %s
            """, (
                student_id,
            ))

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Student deleted successfully."
            )

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

        self.load_students()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.geometry("1250x750")

    root.title(
        "Student Management System"
    )

    page = StudentsPage(root)

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()