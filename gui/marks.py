import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class MarksPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F5F7FB")

        self.selected_id = None
        self.student_data = {}
        self.subject_data = {}

        self.create_widgets()
        self.load_students()
        self.load_subjects()
        self.load_marks()

    # =========================
    # CREATE GUI
    # =========================
    def create_widgets(self):

        # =========================
        # TITLE
        # =========================
        title_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )
        title_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            title_frame,
            text="📝 Marks Management",
            font=("Arial", 26, "bold"),
            text_color="#111827"
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        # =========================
        # STUDENT DETAILS
        # =========================
        student_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )
        student_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            student_frame,
            text="👨‍🎓 Student Information",
            font=("Arial", 18, "bold"),
            text_color="#1D4ED8"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(15, 10),
            sticky="w"
        )

        # Student ID
        ctk.CTkLabel(
            student_frame,
            text="Student ID",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.student_combo = ctk.CTkComboBox(
            student_frame,
            width=190,
            values=["Loading..."],
            command=self.student_selected
        )
        self.student_combo.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Student Name
        ctk.CTkLabel(
            student_frame,
            text="Student Name",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=1,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.name_label = ctk.CTkLabel(
            student_frame,
            text="-",
            width=190,
            anchor="w",
            font=("Arial", 13),
            text_color="#374151"
        )
        self.name_label.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # Course
        ctk.CTkLabel(
            student_frame,
            text="Course",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=2,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.course_label = ctk.CTkLabel(
            student_frame,
            text="-",
            width=190,
            anchor="w",
            font=("Arial", 13),
            text_color="#374151"
        )
        self.course_label.grid(
            row=2,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Semester
        ctk.CTkLabel(
            student_frame,
            text="Semester",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=3,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.semester_label = ctk.CTkLabel(
            student_frame,
            text="-",
            width=100,
            anchor="w",
            font=("Arial", 13),
            text_color="#374151"
        )
        self.semester_label.grid(
            row=2,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        # Email
        ctk.CTkLabel(
            student_frame,
            text="Email",
            font=("Arial", 12, "bold")
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.email_label = ctk.CTkLabel(
            student_frame,
            text="-",
            width=190,
            anchor="w",
            font=("Arial", 13),
            text_color="#374151"
        )
        self.email_label.grid(
            row=4,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Phone
        ctk.CTkLabel(
            student_frame,
            text="Phone",
            font=("Arial", 12, "bold")
        ).grid(
            row=3,
            column=1,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.phone_label = ctk.CTkLabel(
            student_frame,
            text="-",
            width=190,
            anchor="w",
            font=("Arial", 13),
            text_color="#374151"
        )
        self.phone_label.grid(
            row=4,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # =========================
        # MARKS FORM
        # =========================
        marks_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )
        marks_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            marks_frame,
            text="📚 Marks Details",
            font=("Arial", 18, "bold"),
            text_color="#1D4ED8"
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            padx=20,
            pady=(15, 10),
            sticky="w"
        )

        # Subject Code
        ctk.CTkLabel(
            marks_frame,
            text="Subject Code",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.subject_combo = ctk.CTkComboBox(
            marks_frame,
            width=180,
            values=["Loading..."],
            command=self.subject_selected
        )
        self.subject_combo.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Internal
        ctk.CTkLabel(
            marks_frame,
            text="Internal Marks / 40",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=1,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.internal_entry = ctk.CTkEntry(
            marks_frame,
            width=150,
            placeholder_text="0 - 40"
        )
        self.internal_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # External
        ctk.CTkLabel(
            marks_frame,
            text="External Marks / 60",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=2,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.external_entry = ctk.CTkEntry(
            marks_frame,
            width=150,
            placeholder_text="0 - 60"
        )
        self.external_entry.grid(
            row=2,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Total
        ctk.CTkLabel(
            marks_frame,
            text="Total / 100",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=3,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.total_label = ctk.CTkLabel(
            marks_frame,
            text="0",
            width=120,
            font=("Arial", 20, "bold"),
            text_color="#2563EB"
        )
        self.total_label.grid(
            row=2,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        # Grade
        ctk.CTkLabel(
            marks_frame,
            text="Grade",
            font=("Arial", 12, "bold")
        ).grid(
            row=1,
            column=4,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.grade_label = ctk.CTkLabel(
            marks_frame,
            text="-",
            width=80,
            font=("Arial", 20, "bold"),
            text_color="#16A34A"
        )
        self.grade_label.grid(
            row=2,
            column=4,
            padx=15,
            pady=(0, 15)
        )

        # Calculate when marks are typed
        self.internal_entry.bind(
            "<KeyRelease>",
            self.calculate_preview
        )

        self.external_entry.bind(
            "<KeyRelease>",
            self.calculate_preview
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            marks_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=3,
            column=0,
            columnspan=5,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add Marks",
            width=130,
            height=38,
            command=self.add_marks
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="✏️ Update",
            width=120,
            height=38,
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self.update_marks
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            width=120,
            height=38,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_marks
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="🔄 Clear",
            width=120,
            height=38,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.clear_fields
        ).pack(
            side="left",
            padx=5
        )

        # =========================
        # SEARCH
        # =========================
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

        ctk.CTkLabel(
            search_frame,
            text="🔍 Search:",
            font=("Arial", 13, "bold")
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Student ID or Subject Code"
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            command=self.search_marks
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="Show All",
            width=100,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.load_marks
        ).pack(
            side="left",
            padx=5
        )

        # =========================
        # TABLE
        # =========================
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

        columns = (
            "ID",
            "Student ID",
            "Student Name",
            "Subject Code",
            "Internal",
            "External",
            "Total",
            "Grade"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.tree.heading(
                column,
                text=column
            )

        self.tree.column(
            "ID",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "Student ID",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "Student Name",
            width=180,
            anchor="center"
        )

        self.tree.column(
            "Subject Code",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Internal",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "External",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "Total",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "Grade",
            width=70,
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
            padx=(10, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 10)
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_record
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    # =========================
    # LOAD STUDENTS
    # =========================
    def load_students(self):

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    student_id,
                    full_name,
                    email,
                    phone,
                    course,
                    semester
                FROM students
                ORDER BY student_id
            """)

            records = cursor.fetchall()

            self.student_data = {}

            student_ids = []

            for record in records:

                student_id = record[0]

                self.student_data[student_id] = {
                    "name": record[1] or "-",
                    "email": record[2] or "-",
                    "phone": record[3] or "-",
                    "course": record[4] or "-",
                    "semester": record[5] or "-"
                }

                student_ids.append(student_id)

            if student_ids:
                self.student_combo.configure(
                    values=student_ids
                )
                self.student_combo.set(
                    "Select Student"
                )
            else:
                self.student_combo.configure(
                    values=["No students found"]
                )
                self.student_combo.set(
                    "No students found"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load students.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # STUDENT SELECTED
    # =========================
    def student_selected(self, student_id):

        if student_id not in self.student_data:
            return

        student = self.student_data[student_id]

        self.name_label.configure(
            text=student["name"]
        )

        self.email_label.configure(
            text=student["email"]
        )

        self.phone_label.configure(
            text=student["phone"]
        )

        self.course_label.configure(
            text=student["course"]
        )

        self.semester_label.configure(
            text=str(student["semester"])
        )

    # =========================
    # LOAD SUBJECTS
    # =========================
    def load_subjects(self):

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    subject_code,
                    subject_name,
                    course_code,
                    semester
                FROM subjects
                ORDER BY subject_code
            """)

            records = cursor.fetchall()

            self.subject_data = {}

            subject_codes = []

            for record in records:

                subject_code = record[0]

                self.subject_data[subject_code] = {
                    "name": record[1] or "-",
                    "course": record[2] or "-",
                    "semester": record[3] or "-"
                }

                subject_codes.append(subject_code)

            if subject_codes:

                self.subject_combo.configure(
                    values=subject_codes
                )

                self.subject_combo.set(
                    "Select Subject"
                )

            else:

                self.subject_combo.configure(
                    values=["No subjects found"]
                )

                self.subject_combo.set(
                    "No subjects found"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load subjects.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # SUBJECT SELECTED
    # =========================
    def subject_selected(self, subject_code):

        if subject_code not in self.subject_data:
            return

    # =========================
    # CALCULATE PREVIEW
    # =========================
    def calculate_preview(self, event=None):

        try:

            internal_text = self.internal_entry.get().strip()
            external_text = self.external_entry.get().strip()

            if not internal_text or not external_text:
                self.total_label.configure(
                    text="0"
                )

                self.grade_label.configure(
                    text="-"
                )

                return

            internal = float(internal_text)
            external = float(external_text)

            if internal < 0 or external < 0:
                return

            total = internal + external

            if total > 100:
                return

            grade = self.calculate_grade(total)

            self.total_label.configure(
                text=f"{total:g}"
            )

            self.grade_label.configure(
                text=grade
            )

        except ValueError:

            self.total_label.configure(
                text="0"
            )

            self.grade_label.configure(
                text="-"
            )

    # =========================
    # GRADE
    # =========================
    def calculate_grade(self, total):

        if total >= 90:
            return "A+"

        elif total >= 80:
            return "A"

        elif total >= 70:
            return "B+"

        elif total >= 60:
            return "B"

        elif total >= 50:
            return "C"

        elif total >= 40:
            return "D"

        else:
            return "F"

    # =========================
    # GET FORM DATA
    # =========================
    def get_form_data(self):

        student_id = self.student_combo.get().strip()
        subject_code = self.subject_combo.get().strip()

        internal_text = self.internal_entry.get().strip()
        external_text = self.external_entry.get().strip()

        if student_id not in self.student_data:

            messagebox.showwarning(
                "Student Required",
                "Please select a valid student."
            )

            return None

        if subject_code not in self.subject_data:

            messagebox.showwarning(
                "Subject Required",
                "Please select a valid subject."
            )

            return None

        try:

            internal = float(internal_text)
            external = float(external_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Marks",
                "Internal and External marks must be numbers."
            )

            return None

        if internal < 0 or internal > 40:

            messagebox.showwarning(
                "Invalid Marks",
                "Internal marks must be between 0 and 40."
            )

            return None

        if external < 0 or external > 60:

            messagebox.showwarning(
                "Invalid Marks",
                "External marks must be between 0 and 60."
            )

            return None

        total = internal + external

        grade = self.calculate_grade(total)

        return (
            student_id,
            subject_code,
            internal,
            external,
            total,
            grade
        )

    # =========================
    # ADD MARKS
    # =========================
    def add_marks(self):

        data = self.get_form_data()

        if not data:
            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO marks
                (
                    student_id,
                    subject_code,
                    internal_marks,
                    external_marks,
                    total_marks,
                    grade
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                data
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Marks added successfully!"
            )

            self.clear_fields()
            self.load_marks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not add marks.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # LOAD MARKS
    # =========================
    def load_marks(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    m.id,
                    m.student_id,
                    s.full_name,
                    m.subject_code,
                    m.internal_marks,
                    m.external_marks,
                    m.total_marks,
                    m.grade
                FROM marks m
                LEFT JOIN students s
                    ON m.student_id = s.student_id
                ORDER BY m.id DESC
            """

            cursor.execute(query)

            records = cursor.fetchall()

            for record in records:

                self.tree.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load marks.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # SEARCH
    # =========================
    def search_marks(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_marks()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    m.id,
                    m.student_id,
                    s.full_name,
                    m.subject_code,
                    m.internal_marks,
                    m.external_marks,
                    m.total_marks,
                    m.grade
                FROM marks m
                LEFT JOIN students s
                    ON m.student_id = s.student_id
                WHERE m.student_id LIKE %s
                   OR m.subject_code LIKE %s
                   OR s.full_name LIKE %s
                ORDER BY m.id DESC
            """

            value = "%" + search_text + "%"

            cursor.execute(
                query,
                (value, value, value)
            )

            records = cursor.fetchall()

            for record in records:

                self.tree.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Search failed.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # SELECT RECORD
    # =========================
    def select_record(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_id = values[0]

        student_id = values[1]
        subject_code = values[3]

        self.student_combo.set(
            student_id
        )

        self.student_selected(
            student_id
        )

        self.subject_combo.set(
            subject_code
        )

        self.internal_entry.delete(
            0,
            "end"
        )

        self.internal_entry.insert(
            0,
            values[4]
        )

        self.external_entry.delete(
            0,
            "end"
        )

        self.external_entry.insert(
            0,
            values[5]
        )

        self.total_label.configure(
            text=str(values[6])
        )

        self.grade_label.configure(
            text=str(values[7])
        )

    # =========================
    # UPDATE
    # =========================
    def update_marks(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Record",
                "Please select a marks record from the table."
            )

            return

        data = self.get_form_data()

        if not data:
            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE marks
                SET
                    student_id = %s,
                    subject_code = %s,
                    internal_marks = %s,
                    external_marks = %s,
                    total_marks = %s,
                    grade = %s
                WHERE id = %s
            """

            cursor.execute(
                query,
                data + (self.selected_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Marks updated successfully!"
            )

            self.clear_fields()
            self.load_marks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not update marks.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # DELETE
    # =========================
    def delete_marks(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Select Record",
                "Please select a marks record first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Marks",
            "Are you sure you want to delete this marks record?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL."
            )

            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM marks WHERE id = %s",
                (self.selected_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Marks deleted successfully!"
            )

            self.clear_fields()
            self.load_marks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not delete marks.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================
    # CLEAR
    # =========================
    def clear_fields(self):

        self.selected_id = None

        if self.student_data:

            self.student_combo.set(
                "Select Student"
            )

        if self.subject_data:

            self.subject_combo.set(
                "Select Subject"
            )

        self.name_label.configure(
            text="-"
        )

        self.email_label.configure(
            text="-"
        )

        self.phone_label.configure(
            text="-"
        )

        self.course_label.configure(
            text="-"
        )

        self.semester_label.configure(
            text="-"
        )

        self.internal_entry.delete(
            0,
            "end"
        )

        self.external_entry.delete(
            0,
            "end"
        )

        self.total_label.configure(
            text="0"
        )

        self.grade_label.configure(
            text="-"
        )

        self.search_entry.delete(
            0,
            "end"
        )


# =========================
# TEST
# =========================
if __name__ == "__main__":

    app = ctk.CTk()

    app.title("Marks Management")

    app.geometry("1250x800")

    page = MarksPage(app)

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()