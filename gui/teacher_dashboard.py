
import customtkinter as ctk
from tkinter import messagebox
from database import create_connection
from datetime import date


class TeacherDashboard(ctk.CTk):

    def __init__(self, teacher_name="Teacher", teacher_id=None):
        super().__init__()

        self.teacher_name = teacher_name
        self.teacher_id = teacher_id

        self.title("Teacher Dashboard - Student Management System")
        self.geometry("1450x850")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.selected_attendance_id = None
        self.selected_marks_id = None

        self.setup_ui()
        self.show_dashboard()

    # =========================================================
    # MAIN UI
    # =========================================================

    def setup_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR ----------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="TEACHER PORTAL",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Student Management System",
            font=ctk.CTkFont(size=11)
        )
        subtitle.pack(pady=(0, 30))

        buttons = [
            ("🏠  Dashboard", self.show_dashboard),
            ("👤  My Profile", self.show_profile),
            ("📚  My Subjects", self.show_subjects),
            ("👨‍🎓  My Students", self.show_students),
            ("📅  Attendance", self.show_attendance),
            ("📊  Marks", self.show_marks),
            ("🕐  Timetable", self.show_timetable),
            ("📢  Announcements", self.show_announcements),
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=42,
                corner_radius=8,
                anchor="w",
                font=ctk.CTkFont(size=14)
            )
            btn.pack(fill="x", padx=15, pady=4)

        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪  Logout",
            command=self.logout,
            height=42,
            corner_radius=8,
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=ctk.CTkFont(size=14)
        )
        logout_btn.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        # ---------------- MAIN AREA ----------------

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#F5F7FA"
        )
        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(
            self.main_frame,
            height=75,
            corner_radius=0,
            fg_color="white"
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        self.header.grid_propagate(False)

        self.page_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.page_title.pack(
            side="left",
            padx=30,
            pady=20
        )

        self.welcome_label = ctk.CTkLabel(
            self.header,
            text=f"Welcome, {self.teacher_name}",
            font=ctk.CTkFont(size=14)
        )
        self.welcome_label.pack(
            side="right",
            padx=30
        )

        self.content = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="#F5F7FA"
        )
        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def get_connection(self):
        return create_connection()

    def create_stat_card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color="white",
            height=130
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=30, weight="bold")
        )
        value_label.pack(
            anchor="w",
            padx=20
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.page_title.configure(text="Teacher Dashboard")
        self.clear_content()

        conn = self.get_connection()

        subjects_count = 0
        students_count = 0
        attendance_percentage = 0
        marks_count = 0

        if conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT COUNT(*) FROM subjects WHERE teacher_id = %s",
                    (self.teacher_id,)
                )
                subjects_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT e.student_id)
                    FROM enrollments e
                    INNER JOIN subjects s
                        ON e.course_code = s.course_code
                        AND e.semester = s.semester
                    WHERE s.teacher_id = %s
                """, (self.teacher_id,))

                students_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN a.status = 'Present' THEN 1 END),
                        COUNT(*)
                    FROM attendance a
                    INNER JOIN subjects s
                        ON a.subject_code = s.subject_code
                    WHERE s.teacher_id = %s
                """, (self.teacher_id,))

                present, total = cursor.fetchone()

                if total:
                    attendance_percentage = round(
                        (present / total) * 100,
                        2
                    )

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM marks m
                    INNER JOIN subjects s
                        ON m.subject_code = s.subject_code
                    WHERE s.teacher_id = %s
                """, (self.teacher_id,))

                marks_count = cursor.fetchone()[0]

            except Exception as e:
                print("Dashboard error:", e)

            finally:
                cursor.close()
                conn.close()

        title = ctk.CTkLabel(
            self.content,
            text=f"Welcome, {self.teacher_name}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        subtitle = ctk.CTkLabel(
            self.content,
            text="Manage your teaching activities and student academic records.",
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack(
            anchor="w",
            padx=10,
            pady=(0, 20)
        )

        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        cards_frame.pack(
            fill="x",
            padx=10
        )

        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        self.create_stat_card(
            cards_frame,
            "My Subjects",
            subjects_count,
            0,
            0
        )

        self.create_stat_card(
            cards_frame,
            "My Students",
            students_count,
            0,
            1
        )

        self.create_stat_card(
            cards_frame,
            "Attendance",
            f"{attendance_percentage}%",
            0,
            2
        )

        self.create_stat_card(
            cards_frame,
            "Marks Entered",
            marks_count,
            0,
            3
        )

        notice = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )
        notice.pack(
            fill="x",
            padx=10,
            pady=20
        )

        ctk.CTkLabel(
            notice,
            text="Quick Access",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        quick_frame = ctk.CTkFrame(
            notice,
            fg_color="transparent"
        )
        quick_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        quick_buttons = [
            ("📅 Attendance", self.show_attendance),
            ("📊 Marks", self.show_marks),
            ("🕐 Timetable", self.show_timetable),
            ("📢 Announcements", self.show_announcements)
        ]

        for i, (text, command) in enumerate(quick_buttons):

            quick_frame.grid_columnconfigure(
                i,
                weight=1
            )

            ctk.CTkButton(
                quick_frame,
                text=text,
                command=command,
                height=45
            ).grid(
                row=0,
                column=i,
                padx=5,
                sticky="ew"
            )

    # =========================================================
    # PROFILE
    # =========================================================

    def show_profile(self):

        self.page_title.configure(text="My Profile")
        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM teachers WHERE teacher_id = %s",
            (self.teacher_id,)
        )

        teacher = cursor.fetchone()

        cursor.close()
        conn.close()

        if not teacher:
            ctk.CTkLabel(
                self.content,
                text="Teacher profile not found.",
                font=ctk.CTkFont(size=18)
            ).pack(pady=50)
            return

        card = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )
        card.pack(
            fill="x",
            padx=20,
            pady=20
        )

        fields = [
            ("Teacher ID", teacher.get("teacher_id")),
            ("Full Name", teacher.get("full_name")),
            ("Email", teacher.get("email")),
            ("Phone", teacher.get("phone")),
            ("Gender", teacher.get("gender")),
            ("Department", teacher.get("department")),
            ("Designation", teacher.get("designation")),
            ("Subject", teacher.get("subject")),
            ("Qualification", teacher.get("qualification")),
            ("Address", teacher.get("address")),
        ]

        for label, value in fields:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            row.pack(
                fill="x",
                padx=25,
                pady=7
            )

            ctk.CTkLabel(
                row,
                text=label,
                width=180,
                anchor="w",
                font=ctk.CTkFont(weight="bold")
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(value or ""),
                anchor="w"
            ).pack(side="left")

    # =========================================================
    # MY SUBJECTS
    # =========================================================

    def show_subjects(self):

        self.page_title.configure(text="My Subjects")
        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                subject_code,
                subject_name,
                course_code,
                semester,
                credits,
                description
            FROM subjects
            WHERE teacher_id = %s
            ORDER BY semester, subject_name
        """, (self.teacher_id,))

        subjects = cursor.fetchall()

        cursor.close()
        conn.close()

        if not subjects:

            ctk.CTkLabel(
                self.content,
                text="No subjects assigned to you.",
                font=ctk.CTkFont(size=18)
            ).pack(pady=50)

            return

        for subject in subjects:

            card = ctk.CTkFrame(
                self.content,
                fg_color="white",
                corner_radius=10
            )
            card.pack(
                fill="x",
                padx=15,
                pady=7
            )

            ctk.CTkLabel(
                card,
                text=subject["subject_name"],
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(15, 5)
            )

            info = (
                f"Code: {subject['subject_code']}    "
                f"Course: {subject['course_code']}    "
                f"Semester: {subject['semester']}    "
                f"Credits: {subject['credits']}"
            )

            ctk.CTkLabel(
                card,
                text=info
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

    # =========================================================
    # MY STUDENTS
    # =========================================================

    def show_students(self):

        self.page_title.configure(text="My Students")
        self.clear_content()

        search_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        search_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search student..."
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        table_frame = ctk.CTkScrollableFrame(
            self.content,
            fg_color="white"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def load_students():

            for widget in table_frame.winfo_children():
                widget.destroy()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT
                    s.student_id,
                    s.full_name,
                    s.email,
                    s.phone,
                    s.course,
                    s.semester,
                    e.status
                FROM students s
                INNER JOIN enrollments e
                    ON s.student_id = e.student_id
                INNER JOIN subjects sub
                    ON e.course_code = sub.course_code
                    AND e.semester = sub.semester
                WHERE sub.teacher_id = %s
                AND (
                    s.student_id LIKE %s
                    OR s.full_name LIKE %s
                )
                ORDER BY s.full_name
            """, (
                self.teacher_id,
                "%" + search_entry.get() + "%",
                "%" + search_entry.get() + "%"
            ))

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            headers = [
                "Student ID",
                "Name",
                "Email",
                "Phone",
                "Course",
                "Semester",
                "Status"
            ]

            for col, header in enumerate(headers):

                ctk.CTkLabel(
                    table_frame,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                ).grid(
                    row=0,
                    column=col,
                    padx=10,
                    pady=10,
                    sticky="w"
                )

            for r, row in enumerate(rows, start=1):

                for c, value in enumerate(row):

                    ctk.CTkLabel(
                        table_frame,
                        text=str(value or "")
                    ).grid(
                        row=r,
                        column=c,
                        padx=10,
                        pady=8,
                        sticky="w"
                    )

        ctk.CTkButton(
            search_frame,
            text="Search",
            command=load_students
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Show All",
            command=lambda: [
                search_entry.delete(0, "end"),
                load_students()
            ]
        ).pack(
            side="left",
            padx=5
        )

        load_students()

    # =========================================================
    # ATTENDANCE
    # =========================================================

    def show_attendance(self):

        self.page_title.configure(text="Attendance")
        self.clear_content()

        self.selected_attendance_id = None

        form = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )
        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Student

        ctk.CTkLabel(
            form,
            text="Student"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        student_combo = ctk.CTkComboBox(
            form,
            width=300
        )
        student_combo.grid(
            row=0,
            column=1,
            padx=15,
            pady=10
        )

        # Subject

        ctk.CTkLabel(
            form,
            text="Subject"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        subject_combo = ctk.CTkComboBox(
            form,
            width=300
        )
        subject_combo.grid(
            row=1,
            column=1,
            padx=15,
            pady=10
        )

        # Date

        ctk.CTkLabel(
            form,
            text="Date"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        date_entry = ctk.CTkEntry(form)
        date_entry.insert(0, str(date.today()))
        date_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=10
        )

        # Status

        ctk.CTkLabel(
            form,
            text="Status"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        status_combo = ctk.CTkComboBox(
            form,
            values=["Present", "Absent"]
        )
        status_combo.set("Present")
        status_combo.grid(
            row=3,
            column=1,
            padx=15,
            pady=10
        )

        # Load students

        conn = self.get_connection()

        if conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT s.student_id, s.full_name
                FROM students s
                INNER JOIN enrollments e
                    ON s.student_id = e.student_id
                INNER JOIN subjects sub
                    ON e.course_code = sub.course_code
                    AND e.semester = sub.semester
                WHERE sub.teacher_id = %s
                ORDER BY s.full_name
            """, (self.teacher_id,))

            students = cursor.fetchall()

            cursor.close()
            conn.close()

            student_values = [
                f"{name} ({sid})"
                for sid, name in students
            ]

            student_combo.configure(
                values=student_values
            )

        def load_subjects(event=None):

            selected = student_combo.get()

            if not selected:
                return

            student_id = selected.split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT
                    sub.subject_code,
                    sub.subject_name
                FROM subjects sub
                INNER JOIN enrollments e
                    ON e.course_code = sub.course_code
                    AND e.semester = sub.semester
                WHERE sub.teacher_id = %s
                AND e.student_id = %s
                ORDER BY sub.subject_name
            """, (
                self.teacher_id,
                student_id
            ))

            subjects = cursor.fetchall()

            cursor.close()
            conn.close()

            subject_values = [
                f"{name} ({code})"
                for code, name in subjects
            ]

            subject_combo.configure(
                values=subject_values
            )

            if subject_values:
                subject_combo.set(subject_values[0])

        student_combo.bind(
            "<<ComboboxSelected>>",
            load_subjects
        )

        def add_attendance():

            student = student_combo.get()
            subject = subject_combo.get()
            attendance_date = date_entry.get()
            status = status_combo.get()

            if not student or not subject:
                messagebox.showwarning(
                    "Missing Data",
                    "Please select student and subject."
                )
                return

            student_id = student.split("(")[-1].replace(")", "")
            subject_code = subject.split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id
                FROM attendance
                WHERE student_id = %s
                AND subject_code = %s
                AND attendance_date = %s
            """, (
                student_id,
                subject_code,
                attendance_date
            ))

            existing = cursor.fetchone()

            if existing:

                cursor.close()
                conn.close()

                messagebox.showwarning(
                    "Already Exists",
                    "Attendance already exists for this date."
                )

                return

            cursor.execute("""
                INSERT INTO attendance
                (student_id, subject_code, attendance_date, status)
                VALUES (%s, %s, %s, %s)
            """, (
                student_id,
                subject_code,
                attendance_date,
                status
            ))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance added successfully."
            )

            load_attendance()

        def update_attendance():

            if not self.selected_attendance_id:
                messagebox.showwarning(
                    "Select Record",
                    "Please select an attendance record."
                )
                return

            student_id = student_combo.get().split("(")[-1].replace(")", "")
            subject_code = subject_combo.get().split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE attendance
                SET student_id=%s,
                    subject_code=%s,
                    attendance_date=%s,
                    status=%s
                WHERE id=%s
            """, (
                student_id,
                subject_code,
                date_entry.get(),
                status_combo.get(),
                self.selected_attendance_id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Attendance updated."
            )

            load_attendance()

        def delete_attendance():

            if not self.selected_attendance_id:
                messagebox.showwarning(
                    "Select Record",
                    "Please select an attendance record."
                )
                return

            if not messagebox.askyesno(
                "Confirm",
                "Delete selected attendance?"
            ):
                return

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM attendance WHERE id=%s",
                (self.selected_attendance_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            self.selected_attendance_id = None

            messagebox.showinfo(
                "Deleted",
                "Attendance deleted."
            )

            load_attendance()

        buttons = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )
        buttons.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=15
        )

        ctk.CTkButton(
            buttons,
            text="Add",
            command=add_attendance
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Update",
            command=update_attendance
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Delete",
            command=delete_attendance
        ).pack(
            side="left",
            padx=5
        )

        # Table

        table = ctk.CTkScrollableFrame(
            self.content,
            fg_color="white"
        )
        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def load_attendance():

            for widget in table.winfo_children():
                widget.destroy()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    a.id,
                    a.student_id,
                    s.full_name,
                    a.subject_code,
                    a.attendance_date,
                    a.status
                FROM attendance a
                INNER JOIN students s
                    ON a.student_id = s.student_id
                INNER JOIN subjects sub
                    ON a.subject_code = sub.subject_code
                WHERE sub.teacher_id = %s
                ORDER BY a.attendance_date DESC
            """, (self.teacher_id,))

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            headers = [
                "ID",
                "Student ID",
                "Student Name",
                "Subject",
                "Date",
                "Status",
                "Action"
            ]

            for col, header in enumerate(headers):

                ctk.CTkLabel(
                    table,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                ).grid(
                    row=0,
                    column=col,
                    padx=10,
                    pady=10
                )

            for r, row in enumerate(rows, start=1):

                for c, value in enumerate(row[:-1]):

                    ctk.CTkLabel(
                        table,
                        text=str(value)
                    ).grid(
                        row=r,
                        column=c,
                        padx=10,
                        pady=7
                    )

                ctk.CTkButton(
                    table,
                    text="View",
                    width=70,
                    command=lambda data=row: select_attendance(data)
                ).grid(
                    row=r,
                    column=6,
                    padx=10,
                    pady=7
                )

        def select_attendance(data):

            self.selected_attendance_id = data[0]

            student_combo.set(
                f"{data[2]} ({data[1]})"
            )

            load_subjects()

            subject_combo.set(
                f"{data[3]}"
            )

            date_entry.delete(0, "end")
            date_entry.insert(0, str(data[4]))

            status_combo.set(data[5])

        load_attendance()

    # =========================================================
    # MARKS
    # =========================================================

    def show_marks(self):

        self.page_title.configure(text="Marks")
        self.clear_content()

        self.selected_marks_id = None

        form = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )
        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            form,
            text="Student"
        ).grid(row=0, column=0, padx=15, pady=10)

        student_combo = ctk.CTkComboBox(
            form,
            width=300
        )
        student_combo.grid(row=0, column=1, padx=15, pady=10)

        ctk.CTkLabel(
            form,
            text="Subject"
        ).grid(row=1, column=0, padx=15, pady=10)

        subject_combo = ctk.CTkComboBox(
            form,
            width=300
        )
        subject_combo.grid(row=1, column=1, padx=15, pady=10)

        ctk.CTkLabel(
            form,
            text="Internal Marks (0-40)"
        ).grid(row=2, column=0, padx=15, pady=10)

        internal_entry = ctk.CTkEntry(form)
        internal_entry.grid(row=2, column=1, padx=15, pady=10)

        ctk.CTkLabel(
            form,
            text="External Marks (0-60)"
        ).grid(row=3, column=0, padx=15, pady=10)

        external_entry = ctk.CTkEntry(form)
        external_entry.grid(row=3, column=1, padx=15, pady=10)

        total_label = ctk.CTkLabel(
            form,
            text="Total: 0    Grade: -",
            font=ctk.CTkFont(weight="bold")
        )
        total_label.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )

        conn = self.get_connection()

        if conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT s.student_id, s.full_name
                FROM students s
                INNER JOIN enrollments e
                    ON s.student_id = e.student_id
                INNER JOIN subjects sub
                    ON e.course_code = sub.course_code
                    AND e.semester = sub.semester
                WHERE sub.teacher_id = %s
                ORDER BY s.full_name
            """, (self.teacher_id,))

            students = cursor.fetchall()

            cursor.close()
            conn.close()

            student_combo.configure(
                values=[
                    f"{name} ({sid})"
                    for sid, name in students
                ]
            )

        def load_subjects(event=None):

            selected = student_combo.get()

            if not selected:
                return

            student_id = selected.split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT
                    sub.subject_code,
                    sub.subject_name
                FROM subjects sub
                INNER JOIN enrollments e
                    ON e.course_code = sub.course_code
                    AND e.semester = sub.semester
                WHERE sub.teacher_id = %s
                AND e.student_id = %s
                ORDER BY sub.subject_name
            """, (
                self.teacher_id,
                student_id
            ))

            subjects = cursor.fetchall()

            cursor.close()
            conn.close()

            subject_combo.configure(
                values=[
                    f"{name} ({code})"
                    for code, name in subjects
                ]
            )

            if subjects:
                subject_combo.set(
                    f"{subjects[0][1]} ({subjects[0][0]})"
                )

        student_combo.bind(
            "<<ComboboxSelected>>",
            load_subjects
        )

        def calculate():

            try:

                internal = float(
                    internal_entry.get() or 0
                )

                external = float(
                    external_entry.get() or 0
                )

                if not 0 <= internal <= 40:
                    raise ValueError

                if not 0 <= external <= 60:
                    raise ValueError

                total = internal + external

                if total >= 90:
                    grade = "A+"
                elif total >= 80:
                    grade = "A"
                elif total >= 70:
                    grade = "B+"
                elif total >= 60:
                    grade = "B"
                elif total >= 50:
                    grade = "C"
                elif total >= 40:
                    grade = "D"
                else:
                    grade = "F"

                total_label.configure(
                    text=f"Total: {total:.2f}    Grade: {grade}"
                )

                return internal, external, total, grade

            except ValueError:

                total_label.configure(
                    text="Invalid marks"
                )

                return None

        internal_entry.bind(
            "<KeyRelease>",
            lambda e: calculate()
        )

        external_entry.bind(
            "<KeyRelease>",
            lambda e: calculate()
        )

        def add_marks():

            selected_student = student_combo.get()
            selected_subject = subject_combo.get()

            if not selected_student or not selected_subject:
                messagebox.showwarning(
                    "Missing Data",
                    "Please select student and subject."
                )
                return

            result = calculate()

            if not result:
                messagebox.showerror(
                    "Invalid Marks",
                    "Internal must be 0-40 and External must be 0-60."
                )
                return

            internal, external, total, grade = result

            student_id = selected_student.split("(")[-1].replace(")", "")
            subject_code = selected_subject.split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id
                FROM marks
                WHERE student_id=%s
                AND subject_code=%s
            """, (
                student_id,
                subject_code
            ))

            if cursor.fetchone():

                cursor.close()
                conn.close()

                messagebox.showwarning(
                    "Already Exists",
                    "Marks already exist for this student and subject."
                )

                return

            cursor.execute("""
                INSERT INTO marks
                (student_id, subject_code,
                 internal_marks, external_marks,
                 total_marks, grade)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                student_id,
                subject_code,
                internal,
                external,
                total,
                grade
            ))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Marks added successfully."
            )

            load_marks()

        def update_marks():

            if not self.selected_marks_id:
                messagebox.showwarning(
                    "Select Record",
                    "Please select a marks record."
                )
                return

            result = calculate()

            if not result:
                return

            internal, external, total, grade = result

            student_id = student_combo.get().split("(")[-1].replace(")", "")
            subject_code = subject_combo.get().split("(")[-1].replace(")", "")

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE marks
                SET student_id=%s,
                    subject_code=%s,
                    internal_marks=%s,
                    external_marks=%s,
                    total_marks=%s,
                    grade=%s
                WHERE id=%s
            """, (
                student_id,
                subject_code,
                internal,
                external,
                total,
                grade,
                self.selected_marks_id
            ))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Marks updated successfully."
            )

            load_marks()

        def delete_marks():

            if not self.selected_marks_id:
                messagebox.showwarning(
                    "Select Record",
                    "Please select a marks record."
                )
                return

            if not messagebox.askyesno(
                "Confirm",
                "Delete selected marks?"
            ):
                return

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM marks WHERE id=%s",
                (self.selected_marks_id,)
            )

            conn.commit()

            cursor.close()
            conn.close()

            self.selected_marks_id = None

            messagebox.showinfo(
                "Deleted",
                "Marks deleted successfully."
            )

            load_marks()

        buttons = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )
        buttons.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=15
        )

        ctk.CTkButton(
            buttons,
            text="Add",
            command=add_marks
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Update",
            command=update_marks
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Delete",
            command=delete_marks
        ).pack(side="left", padx=5)

        table = ctk.CTkScrollableFrame(
            self.content,
            fg_color="white"
        )
        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def load_marks():

            for widget in table.winfo_children():
                widget.destroy()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
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
                INNER JOIN students s
                    ON m.student_id = s.student_id
                INNER JOIN subjects sub
                    ON m.subject_code = sub.subject_code
                WHERE sub.teacher_id = %s
                ORDER BY s.full_name
            """, (self.teacher_id,))

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            headers = [
                "ID",
                "Student ID",
                "Student Name",
                "Subject",
                "Internal",
                "External",
                "Total",
                "Grade",
                "Action"
            ]

            for col, header in enumerate(headers):

                ctk.CTkLabel(
                    table,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                ).grid(
                    row=0,
                    column=col,
                    padx=8,
                    pady=10
                )

            for r, row in enumerate(rows, start=1):

                for c, value in enumerate(row):

                    ctk.CTkLabel(
                        table,
                        text=str(value)
                    ).grid(
                        row=r,
                        column=c,
                        padx=8,
                        pady=7
                    )

                ctk.CTkButton(
                    table,
                    text="View",
                    width=70,
                    command=lambda data=row: select_marks(data)
                ).grid(
                    row=r,
                    column=8,
                    padx=8,
                    pady=7
                )

        def select_marks(data):

            self.selected_marks_id = data[0]

            student_combo.set(
                f"{data[2]} ({data[1]})"
            )

            load_subjects()

            subject_combo.set(
                data[3]
            )

            internal_entry.delete(0, "end")
            internal_entry.insert(0, str(data[4]))

            external_entry.delete(0, "end")
            external_entry.insert(0, str(data[5]))

            calculate()

        load_marks()

    # =========================================================
    # TIMETABLE
    # =========================================================

    def show_timetable(self):

        self.page_title.configure(text="My Timetable")
        self.clear_content()

        top = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        search_entry = ctk.CTkEntry(
            top,
            placeholder_text="Search course, subject, teacher, day or room..."
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        table = ctk.CTkScrollableFrame(
            self.content,
            fg_color="white"
        )
        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def load_timetable():

            for widget in table.winfo_children():
                widget.destroy()

            search = search_entry.get().strip()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.day_of_week,
                    t.start_time,
                    t.end_time,
                    c.course_name,
                    t.course_code,
                    s.subject_name,
                    t.subject_code,
                    tr.full_name,
                    t.room_number,
                    t.semester
                FROM timetable t
                INNER JOIN courses c
                    ON t.course_code = c.course_code
                INNER JOIN subjects s
                    ON t.subject_code = s.subject_code
                INNER JOIN teachers tr
                    ON t.teacher_id = tr.teacher_id
                WHERE t.teacher_id = %s
                AND (
                    c.course_name LIKE %s
                    OR t.course_code LIKE %s
                    OR s.subject_name LIKE %s
                    OR t.subject_code LIKE %s
                    OR tr.full_name LIKE %s
                    OR t.day_of_week LIKE %s
                    OR t.room_number LIKE %s
                )
                ORDER BY
                    FIELD(
                        t.day_of_week,
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday',
                        'Sunday'
                    ),
                    t.start_time
            """, (
                self.teacher_id,
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            headers = [
                "Day",
                "Start",
                "End",
                "Course",
                "Course Code",
                "Subject",
                "Subject Code",
                "Teacher",
                "Room",
                "Semester"
            ]

            for col, header in enumerate(headers):

                ctk.CTkLabel(
                    table,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                ).grid(
                    row=0,
                    column=col,
                    padx=8,
                    pady=10
                )

            for r, row in enumerate(rows, start=1):

                for c, value in enumerate(row):

                    ctk.CTkLabel(
                        table,
                        text=str(value or "")
                    ).grid(
                        row=r,
                        column=c,
                        padx=8,
                        pady=7
                    )

        ctk.CTkButton(
            top,
            text="Search",
            command=load_timetable
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="Show All",
            command=lambda: [
                search_entry.delete(0, "end"),
                load_timetable()
            ]
        ).pack(
            side="left",
            padx=5
        )

        load_timetable()

    # =========================================================
    # ANNOUNCEMENTS
    # =========================================================

    def show_announcements(self):

        self.page_title.configure(text="Announcements")
        self.clear_content()

        # ---------------- TOP AREA ----------------

        top_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        top_frame.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        search_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Search announcements..."
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        # ---------------- NOTICE AREA ----------------

        notices_frame = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )
        notices_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        def load_announcements():

            for widget in notices_frame.winfo_children():
                widget.destroy()

            search = search_entry.get().strip()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    id,
                    title,
                    message,
                    target_audience,
                    announcement_date
                FROM announcements
                WHERE target_audience IN ('All', 'Teacher')
                AND (
                    title LIKE %s
                    OR message LIKE %s
                    OR target_audience LIKE %s
                )
                ORDER BY announcement_date DESC, id DESC
            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

            announcements = cursor.fetchall()

            cursor.close()
            conn.close()

            if not announcements:

                empty = ctk.CTkFrame(
                    notices_frame,
                    fg_color="white",
                    corner_radius=12
                )
                empty.pack(
                    fill="x",
                    padx=10,
                    pady=30
                )

                ctk.CTkLabel(
                    empty,
                    text="📢",
                    font=ctk.CTkFont(size=40)
                ).pack(pady=(25, 5))

                ctk.CTkLabel(
                    empty,
                    text="No announcements available",
                    font=ctk.CTkFont(
                        size=20,
                        weight="bold"
                    )
                ).pack(pady=5)

                ctk.CTkLabel(
                    empty,
                    text="New announcements from the administrator will appear here.",
                    font=ctk.CTkFont(size=13)
                ).pack(pady=(0, 25))

                return

            for announcement in announcements:

                card = ctk.CTkFrame(
                    notices_frame,
                    fg_color="white",
                    corner_radius=12
                )
                card.pack(
                    fill="x",
                    padx=10,
                    pady=8
                )

                # Header

                header = ctk.CTkFrame(
                    card,
                    fg_color="transparent"
                )
                header.pack(
                    fill="x",
                    padx=20,
                    pady=(18, 5)
                )

                ctk.CTkLabel(
                    header,
                    text="📢",
                    font=ctk.CTkFont(size=22)
                ).pack(side="left")

                ctk.CTkLabel(
                    header,
                    text=announcement["title"],
                    font=ctk.CTkFont(
                        size=18,
                        weight="bold"
                    )
                ).pack(
                    side="left",
                    padx=10
                )

                # Date

                ctk.CTkLabel(
                    header,
                    text=str(
                        announcement["announcement_date"]
                    ),
                    font=ctk.CTkFont(size=12)
                ).pack(
                    side="right"
                )

                # Message

                message_text = announcement["message"]

                if len(message_text) > 180:
                    message_text = message_text[:180] + "..."

                ctk.CTkLabel(
                    card,
                    text=message_text,
                    justify="left",
                    anchor="w",
                    wraplength=900,
                    font=ctk.CTkFont(size=14)
                ).pack(
                    fill="x",
                    padx=55,
                    pady=5
                )

                # Footer

                footer = ctk.CTkFrame(
                    card,
                    fg_color="transparent"
                )
                footer.pack(
                    fill="x",
                    padx=55,
                    pady=(5, 18)
                )

                ctk.CTkLabel(
                    footer,
                    text=f"Audience: {announcement['target_audience']}",
                    font=ctk.CTkFont(size=12)
                ).pack(side="left")

                ctk.CTkButton(
                    footer,
                    text="View Details",
                    width=110,
                    height=30,
                    command=lambda a=announcement:
                        show_details(a)
                ).pack(side="right")

        def show_details(announcement):

            dialog = ctk.CTkToplevel(self)
            dialog.title("Announcement Details")
            dialog.geometry("650x500")
            dialog.resizable(False, False)

            dialog.transient(self)
            dialog.grab_set()

            ctk.CTkLabel(
                dialog,
                text="📢 Announcement",
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            ).pack(
                pady=(25, 10)
            )

            ctk.CTkLabel(
                dialog,
                text=announcement["title"],
                font=ctk.CTkFont(
                    size=20,
                    weight="bold"
                ),
                wraplength=550
            ).pack(
                pady=10
            )

            info = (
                f"Date: {announcement['announcement_date']}\n"
                f"Audience: {announcement['target_audience']}"
            )

            ctk.CTkLabel(
                dialog,
                text=info,
                font=ctk.CTkFont(size=13)
            ).pack(pady=5)

            message_box = ctk.CTkTextbox(
                dialog,
                width=550,
                height=230,
                corner_radius=8
            )
            message_box.pack(
                padx=30,
                pady=15,
                fill="both",
                expand=True
            )

            message_box.insert(
                "1.0",
                announcement["message"]
            )

            message_box.configure(
                state="disabled"
            )

            ctk.CTkButton(
                dialog,
                text="Close",
                command=dialog.destroy,
                width=120
            ).pack(pady=(0, 20))

        ctk.CTkButton(
            top_frame,
            text="🔄 Refresh",
            width=100,
            command=load_announcements
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            top_frame,
            text="Show All",
            width=100,
            command=lambda: [
                search_entry.delete(0, "end"),
                load_announcements()
            ]
        ).pack(side="left", padx=5)

        load_announcements()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        if messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        ):

            self.destroy()

            try:

                from login import LoginWindow

                app = LoginWindow()
                app.mainloop()

            except Exception as e:
                print("Login error:", e)


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    app = TeacherDashboard(
        teacher_name="RK SIR",
        teacher_id="BCAB"
    )

    app.mainloop()

