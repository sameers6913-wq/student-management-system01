import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date
from database import create_connection


class AttendancePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F5F7FB"
        )

        self.student_data = {}

        self.create_ui()
        self.load_students()
        self.load_subjects()
        self.load_attendance()

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="📅 Attendance Management",
            font=("Arial", 26, "bold"),
            text_color="#111827"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            header,
            text="Manage student attendance using saved students and subjects",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
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

        # -------------------------------------------------
        # STUDENT ID
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Student ID",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.student_combo = ctk.CTkComboBox(
            form,
            width=220,
            height=35,
            values=["Select Student"],
            command=self.student_selected
        )

        self.student_combo.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # STUDENT NAME
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Student Name",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.name_label = ctk.CTkLabel(
            form,
            text="Select a student",
            width=220,
            height=35,
            fg_color="#F3F4F6",
            corner_radius=6,
            anchor="w",
            padx=10,
            text_color="#374151"
        )

        self.name_label.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # COURSE
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Course",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.course_label = ctk.CTkLabel(
            form,
            text="-",
            width=180,
            height=35,
            fg_color="#F3F4F6",
            corner_radius=6,
            anchor="w",
            padx=10,
            text_color="#374151"
        )

        self.course_label.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # SEMESTER
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Semester",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=3,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.semester_label = ctk.CTkLabel(
            form,
            text="-",
            width=100,
            height=35,
            fg_color="#F3F4F6",
            corner_radius=6,
            anchor="w",
            padx=10,
            text_color="#374151"
        )

        self.semester_label.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # SUBJECT CODE
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Subject Code",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.subject_combo = ctk.CTkComboBox(
            form,
            width=220,
            height=35,
            values=["Select Subject"]
        )

        self.subject_combo.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # -------------------------------------------------
        # ATTENDANCE DATE
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Attendance Date",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.date_entry = ctk.CTkEntry(
            form,
            width=220,
            height=35,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=3,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        ctk.CTkLabel(
            form,
            text="Attendance Status",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.status_combo = ctk.CTkComboBox(
            form,
            width=180,
            height=35,
            values=["Present", "Absent"]
        )

        self.status_combo.grid(
            row=3,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        self.status_combo.set("Present")

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add",
            width=90,
            height=35,
            command=self.add_attendance
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="✏ Update",
            width=90,
            height=35,
            command=self.update_attendance
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="🗑 Delete",
            width=90,
            height=35,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_attendance
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        search_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            height=35,
            placeholder_text="Search Student ID or Subject Code"
        )

        self.search_entry.pack(
            side="left",
            padx=20,
            pady=15
        )

        ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            width=100,
            command=self.search_attendance
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="🔄 Show All",
            width=100,
            command=self.load_attendance
        ).pack(
            side="left",
            padx=5
        )

        # -------------------------------------------------
        # TABLE
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
            pady=(0, 20)
        )

        columns = (
            "id",
            "student_id",
            "student_name",
            "subject_code",
            "attendance_date",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "student_id",
            text="Student ID"
        )

        self.tree.heading(
            "student_name",
            text="Student Name"
        )

        self.tree.heading(
            "subject_code",
            text="Subject Code"
        )

        self.tree.heading(
            "attendance_date",
            text="Date"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "student_id",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "student_name",
            width=200
        )

        self.tree.column(
            "subject_code",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "attendance_date",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=120,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=15
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_record
        )

    # =====================================================
    # LOAD STUDENTS FROM LOCAL MYSQL
    # =====================================================

    def load_students(self):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    student_id,
                    full_name,
                    email,
                    phone,
                    course,
                    semester
                FROM students
                ORDER BY student_id ASC
            """

            cursor.execute(query)

            students = cursor.fetchall()

            self.student_data.clear()

            student_ids = []

            for student in students:

                student_id = student.get("student_id")

                if not student_id:
                    continue

                student_ids.append(
                    str(student_id)
                )

                self.student_data[str(student_id)] = {
                    "name": student.get("full_name", ""),
                    "email": student.get("email", ""),
                    "phone": student.get("phone", ""),
                    "course": student.get("course", ""),
                    "semester": student.get("semester")
                }

            if student_ids:

                self.student_combo.configure(
                    values=student_ids
                )

                self.student_combo.set(
                    "Select Student"
                )

            else:

                self.student_combo.configure(
                    values=["No students saved"]
                )

                self.student_combo.set(
                    "No students saved"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # LOAD SUBJECTS FROM LOCAL MYSQL
    # =====================================================

    def load_subjects(self):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    subject_code
                FROM subjects
                ORDER BY subject_code ASC
            """

            cursor.execute(query)

            subjects = cursor.fetchall()

            subject_codes = []

            for subject in subjects:

                subject_code = subject.get(
                    "subject_code"
                )

                if subject_code:

                    subject_codes.append(
                        str(subject_code)
                    )

            if subject_codes:

                self.subject_combo.configure(
                    values=subject_codes
                )

                self.subject_combo.set(
                    "Select Subject"
                )

            else:

                self.subject_combo.configure(
                    values=["No subjects saved"]
                )

                self.subject_combo.set(
                    "No subjects saved"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load subjects.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # STUDENT SELECTED
    # =====================================================

    def student_selected(self, student_id):

        if student_id not in self.student_data:
            return

        student = self.student_data[
            student_id
        ]

        self.name_label.configure(
            text=student.get(
                "name",
                ""
            )
        )

        self.course_label.configure(
            text=student.get(
                "course",
                ""
            ) or "-"
        )

        semester = student.get(
            "semester"
        )

        self.semester_label.configure(
            text=str(semester)
            if semester is not None
            else "-"
        )

    # =====================================================
    # ADD ATTENDANCE
    # =====================================================

    def add_attendance(self):

        student_id = self.student_combo.get().strip()
        subject_code = self.subject_combo.get().strip()
        attendance_date = self.date_entry.get().strip()
        status = self.status_combo.get().strip()

        # Validate student
        if student_id not in self.student_data:

            messagebox.showwarning(
                "Invalid Student",
                "Please select a student from the list."
            )

            return

        # Validate subject
        if subject_code in (
            "",
            "Select Subject",
            "No subjects saved"
        ):

            messagebox.showwarning(
                "Missing Subject",
                "Please select a subject."
            )

            return

        # Validate date
        if not attendance_date:

            messagebox.showwarning(
                "Missing Date",
                "Please enter the attendance date."
            )

            return

        try:

            date.fromisoformat(
                attendance_date
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please enter date in YYYY-MM-DD format."
            )

            return

        # Validate status
        if status not in (
            "Present",
            "Absent"
        ):

            messagebox.showwarning(
                "Invalid Status",
                "Please select Present or Absent."
            )

            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor()

            # Check duplicate attendance
            duplicate_query = """
                SELECT id
                FROM attendance
                WHERE student_id = %s
                AND subject_code = %s
                AND attendance_date = %s
                LIMIT 1
            """

            cursor.execute(
                duplicate_query,
                (
                    student_id,
                    subject_code,
                    attendance_date
                )
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Duplicate Attendance",
                    "Attendance already exists for this student, subject and date."
                )

                return

            query = """
                INSERT INTO attendance
                (
                    student_id,
                    subject_code,
                    attendance_date,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    student_id,
                    subject_code,
                    attendance_date,
                    status
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Attendance added successfully."
            )

            self.clear_form()
            self.load_attendance()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add attendance.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # UPDATE ATTENDANCE
    # =====================================================

    def update_attendance(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select an attendance record from the table."
            )

            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:

            messagebox.showwarning(
                "Select Record",
                "Invalid attendance record."
            )

            return

        record_id = values[0]

        student_id = self.student_combo.get().strip()
        subject_code = self.subject_combo.get().strip()
        attendance_date = self.date_entry.get().strip()
        status = self.status_combo.get().strip()

        if student_id not in self.student_data:

            messagebox.showwarning(
                "Invalid Student",
                "Please select a valid student."
            )

            return

        if subject_code in (
            "",
            "Select Subject",
            "No subjects saved"
        ):

            messagebox.showwarning(
                "Missing Subject",
                "Please select a subject."
            )

            return

        try:

            date.fromisoformat(
                attendance_date
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please enter date in YYYY-MM-DD format."
            )

            return

        if status not in (
            "Present",
            "Absent"
        ):

            messagebox.showwarning(
                "Invalid Status",
                "Please select Present or Absent."
            )

            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor()

            # Check whether another record already has
            # the same student, subject and date
            duplicate_query = """
                SELECT id
                FROM attendance
                WHERE student_id = %s
                AND subject_code = %s
                AND attendance_date = %s
                AND id != %s
                LIMIT 1
            """

            cursor.execute(
                duplicate_query,
                (
                    student_id,
                    subject_code,
                    attendance_date,
                    record_id
                )
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Duplicate Attendance",
                    "Another attendance record already exists for this student, subject and date."
                )

                return

            query = """
                UPDATE attendance
                SET
                    student_id = %s,
                    subject_code = %s,
                    attendance_date = %s,
                    status = %s
                WHERE id = %s
            """

            cursor.execute(
                query,
                (
                    student_id,
                    subject_code,
                    attendance_date,
                    status,
                    record_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Attendance updated successfully."
            )

            self.clear_form()
            self.load_attendance()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update attendance.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # DELETE ATTENDANCE
    # =====================================================

    def delete_attendance(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select an attendance record."
            )

            return

        item = self.tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if not values:

            messagebox.showwarning(
                "Select Record",
                "Invalid attendance record."
            )

            return

        record_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this attendance record?"
        )

        if not confirm:
            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor()

            query = """
                DELETE FROM attendance
                WHERE id = %s
            """

            cursor.execute(
                query,
                (record_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Attendance deleted successfully."
            )

            self.clear_form()
            self.load_attendance()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete attendance.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # LOAD ATTENDANCE FROM LOCAL MYSQL
    # =====================================================

    def load_attendance(self):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    a.id,
                    a.student_id,
                    s.full_name AS student_name,
                    a.subject_code,
                    a.attendance_date,
                    a.status
                FROM attendance a
                LEFT JOIN students s
                    ON a.student_id = s.student_id
                ORDER BY
                    a.attendance_date DESC,
                    a.id DESC
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.get("id"),
                        row.get("student_id"),
                        row.get("student_name"),
                        row.get("subject_code"),
                        row.get("attendance_date"),
                        row.get("status")
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load attendance.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # SEARCH ATTENDANCE
    # =====================================================

    def search_attendance(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_attendance()

            return

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to local MySQL."
                )
                return

            cursor = connection.cursor(dictionary=True)

            search_value = f"%{search_text}%"

            query = """
                SELECT
                    a.id,
                    a.student_id,
                    s.full_name AS student_name,
                    a.subject_code,
                    a.attendance_date,
                    a.status
                FROM attendance a
                LEFT JOIN students s
                    ON a.student_id = s.student_id
                WHERE
                    a.student_id LIKE %s
                    OR a.subject_code LIKE %s
                    OR s.full_name LIKE %s
                ORDER BY
                    a.attendance_date DESC,
                    a.id DESC
            """

            cursor.execute(
                query,
                (
                    search_value,
                    search_value,
                    search_value
                )
            )

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.get("id"),
                        row.get("student_id"),
                        row.get("student_name"),
                        row.get("subject_code"),
                        row.get("attendance_date"),
                        row.get("status")
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search attendance.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # CLEAR TABLE
    # =====================================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    # =====================================================
    # SELECT TABLE RECORD
    # =====================================================

    def select_record(self, event=None):

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

        if len(values) < 6:
            return

        student_id = str(
            values[1]
        )

        subject_code = str(
            values[3]
        )

        attendance_date = str(
            values[4]
        )

        status = str(
            values[5]
        )

        # Student
        self.student_combo.set(
            student_id
        )

        self.student_selected(
            student_id
        )

        # Subject
        self.subject_combo.set(
            subject_code
        )

        # Date
        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            attendance_date
        )

        # Status
        self.status_combo.set(
            status
        )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.student_combo.set(
            "Select Student"
        )

        self.name_label.configure(
            text="Select a student"
        )

        self.course_label.configure(
            text="-"
        )

        self.semester_label.configure(
            text="-"
        )

        self.subject_combo.set(
            "Select Subject"
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )

        self.status_combo.set(
            "Present"
        )


# =========================================================
# STANDALONE TEST
# =========================================================

if __name__ == "__main__":

    ctk.set_appearance_mode(
        "light"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    app = ctk.CTk()

    app.title(
        "Attendance Management"
    )

    app.geometry(
        "1200x700"
    )

    app.minsize(
        1100,
        650
    )

    page = AttendancePage(
        app
    )

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()