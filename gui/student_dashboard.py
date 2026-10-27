import customtkinter as ctk
from tkinter import messagebox
from database import create_connection


class StudentDashboard(ctk.CTk):

    def __init__(self, student_id=None, student_name="Student"):
        super().__init__()

        self.student_id = student_id
        self.student_name = student_name

        self.title("Student Dashboard - Student Management System")
        self.geometry("1450x850")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.setup_ui()
        self.show_dashboard()

    # =========================================================
    # MAIN UI
    # =========================================================

    def setup_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR =================

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="STUDENT PORTAL",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Student Management System",
            font=ctk.CTkFont(size=11)
        ).pack(pady=(0, 30))

        buttons = [
            ("🏠  Dashboard", self.show_dashboard),
            ("👤  My Profile", self.show_profile),
            ("📚  My Courses", self.show_courses),
            ("📖  My Subjects", self.show_subjects),
            ("📅  My Attendance", self.show_attendance),
            ("📊  My Marks", self.show_marks),
            ("🕐  My Timetable", self.show_timetable),
            ("📢  Announcements", self.show_announcements),
        ]

        for text, command in buttons:

            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=42,
                corner_radius=8,
                anchor="w",
                font=ctk.CTkFont(size=14)
            ).pack(
                fill="x",
                padx=15,
                pady=4
            )

        ctk.CTkButton(
            self.sidebar,
            text="🚪  Logout",
            command=self.logout,
            height=42,
            corner_radius=8,
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=ctk.CTkFont(size=14)
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        # ================= MAIN AREA =================

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

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_frame.grid_rowconfigure(
            1,
            weight=1
        )

        # ================= HEADER =================

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
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        self.page_title.pack(
            side="left",
            padx=30,
            pady=20
        )

        ctk.CTkLabel(
            self.header,
            text=f"Welcome, {self.student_name}",
            font=ctk.CTkFont(size=14)
        ).pack(
            side="right",
            padx=30
        )

        # ================= CONTENT =================

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

    def create_stat_card(
        self,
        parent,
        title,
        value,
        row,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12,
            height=130
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.page_title.configure(
            text="Student Dashboard"
        )

        self.clear_content()

        conn = self.get_connection()

        course_count = 0
        subject_count = 0
        attendance_percentage = 0
        marks_count = 0

        if conn:

            cursor = conn.cursor()

            try:

                cursor.execute("""
                    SELECT COUNT(DISTINCT course_code)
                    FROM enrollments
                    WHERE student_id = %s
                    AND status != 'Dropped'
                """, (self.student_id,))

                course_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(DISTINCT sub.subject_code)
                    FROM subjects sub
                    INNER JOIN enrollments e
                        ON sub.course_code = e.course_code
                        AND sub.semester = e.semester
                    WHERE e.student_id = %s
                    AND e.status != 'Dropped'
                """, (self.student_id,))

                subject_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT
                        COUNT(
                            CASE
                                WHEN status = 'Present'
                                THEN 1
                            END
                        ),
                        COUNT(*)
                    FROM attendance
                    WHERE student_id = %s
                """, (self.student_id,))

                present, total = cursor.fetchone()

                if total:
                    attendance_percentage = round(
                        (present / total) * 100,
                        2
                    )

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM marks
                    WHERE student_id = %s
                """, (self.student_id,))

                marks_count = cursor.fetchone()[0]

            except Exception as e:

                print(
                    "Dashboard error:",
                    e
                )

            finally:

                cursor.close()
                conn.close()

        ctk.CTkLabel(
            self.content,
            text=f"Welcome, {self.student_name}",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self.content,
            text="View your academic information, attendance, marks and timetable.",
            font=ctk.CTkFont(size=14)
        ).pack(
            anchor="w",
            padx=10,
            pady=(0, 20)
        )

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            padx=10
        )

        for i in range(4):

            cards.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_stat_card(
            cards,
            "My Courses",
            course_count,
            0,
            0
        )

        self.create_stat_card(
            cards,
            "My Subjects",
            subject_count,
            0,
            1
        )

        self.create_stat_card(
            cards,
            "Attendance",
            f"{attendance_percentage}%",
            0,
            2
        )

        self.create_stat_card(
            cards,
            "Marks Records",
            marks_count,
            0,
            3
        )

        quick = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )

        quick.pack(
            fill="x",
            padx=10,
            pady=20
        )

        ctk.CTkLabel(
            quick,
            text="Quick Access",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        quick_buttons = ctk.CTkFrame(
            quick,
            fg_color="transparent"
        )

        quick_buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        items = [
            ("📅 Attendance", self.show_attendance),
            ("📊 Marks", self.show_marks),
            ("🕐 Timetable", self.show_timetable),
            ("📢 Announcements", self.show_announcements)
        ]

        for i, (text, command) in enumerate(items):

            quick_buttons.grid_columnconfigure(
                i,
                weight=1
            )

            ctk.CTkButton(
                quick_buttons,
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

        self.page_title.configure(
            text="My Profile"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM students
            WHERE student_id = %s
        """, (self.student_id,))

        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if not student:

            ctk.CTkLabel(
                self.content,
                text="Student profile not found.",
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
            ("Student ID", student.get("student_id")),
            ("Full Name", student.get("full_name")),
            ("Email", student.get("email")),
            ("Phone", student.get("phone")),
            ("Gender", student.get("gender")),
            ("Date of Birth", student.get("date_of_birth")),
            ("Course", student.get("course")),
            ("Semester", student.get("semester")),
            ("Address", student.get("address")),
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
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(value or ""),
                anchor="w"
            ).pack(side="left")

    # =========================================================
    # COURSES
    # =========================================================

    def show_courses(self):

        self.page_title.configure(
            text="My Courses"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                e.course_code,
                c.course_name,
                c.duration,
                e.enrollment_date,
                e.semester,
                e.status
            FROM enrollments e
            LEFT JOIN courses c
                ON e.course_code = c.course_code
            WHERE e.student_id = %s
            ORDER BY e.semester
        """, (self.student_id,))

        courses = cursor.fetchall()

        cursor.close()
        conn.close()

        if not courses:

            ctk.CTkLabel(
                self.content,
                text="No course enrollments found.",
                font=ctk.CTkFont(size=18)
            ).pack(pady=50)

            return

        for course in courses:

            card = ctk.CTkFrame(
                self.content,
                fg_color="white",
                corner_radius=12
            )

            card.pack(
                fill="x",
                padx=15,
                pady=8
            )

            ctk.CTkLabel(
                card,
                text=course["course_name"] or course["course_code"],
                font=ctk.CTkFont(
                    size=19,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=20,
                pady=(18, 5)
            )

            info = (
                f"Course Code: {course['course_code']}    "
                f"Semester: {course['semester']}    "
                f"Duration: {course['duration'] or '-'}\n"
                f"Enrollment Date: {course['enrollment_date']}    "
                f"Status: {course['status']}"
            )

            ctk.CTkLabel(
                card,
                text=info,
                justify="left"
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 18)
            )

    # =========================================================
    # SUBJECTS
    # =========================================================

    def show_subjects(self):

        self.page_title.configure(
            text="My Subjects"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT DISTINCT
                sub.subject_code,
                sub.subject_name,
                sub.course_code,
                sub.semester,
                sub.credits,
                t.full_name AS teacher_name
            FROM subjects sub
            INNER JOIN enrollments e
                ON sub.course_code = e.course_code
                AND sub.semester = e.semester
            LEFT JOIN teachers t
                ON sub.teacher_id = t.teacher_id
            WHERE e.student_id = %s
            AND e.status != 'Dropped'
            ORDER BY sub.semester, sub.subject_name
        """, (self.student_id,))

        subjects = cursor.fetchall()

        cursor.close()
        conn.close()

        if not subjects:

            ctk.CTkLabel(
                self.content,
                text="No subjects found.",
                font=ctk.CTkFont(size=18)
            ).pack(pady=50)

            return

        for subject in subjects:

            card = ctk.CTkFrame(
                self.content,
                fg_color="white",
                corner_radius=12
            )

            card.pack(
                fill="x",
                padx=15,
                pady=7
            )

            ctk.CTkLabel(
                card,
                text=subject["subject_name"],
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=20,
                pady=(15, 5)
            )

            info = (
                f"Subject Code: {subject['subject_code']}    "
                f"Course: {subject['course_code']}    "
                f"Semester: {subject['semester']}    "
                f"Credits: {subject['credits'] or '-'}\n"
                f"Teacher: {subject['teacher_name'] or 'Not Assigned'}"
            )

            ctk.CTkLabel(
                card,
                text=info,
                justify="left"
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

    # =========================================================
    # ATTENDANCE
    # =========================================================

    def show_attendance(self):

        self.page_title.configure(
            text="My Attendance"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(
                    CASE
                        WHEN status = 'Present'
                        THEN 1
                        ELSE 0
                    END
                ) AS present
            FROM attendance
            WHERE student_id = %s
        """, (self.student_id,))

        summary = cursor.fetchone()

        total = summary["total"] or 0
        present = summary["present"] or 0

        percentage = 0

        if total:

            percentage = round(
                (present / total) * 100,
                2
            )

        summary_card = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )

        summary_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            summary_card,
            text="Overall Attendance",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            summary_card,
            text=f"{percentage}%",
            font=ctk.CTkFont(
                size=35,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        cursor.execute("""
            SELECT
                a.attendance_date,
                a.subject_code,
                s.subject_name,
                a.status
            FROM attendance a
            LEFT JOIN subjects s
                ON a.subject_code = s.subject_code
            WHERE a.student_id = %s
            ORDER BY a.attendance_date DESC
        """, (self.student_id,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

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

        headers = [
            "Date",
            "Subject Code",
            "Subject",
            "Status"
        ]

        for col, header in enumerate(headers):

            ctk.CTkLabel(
                table,
                text=header,
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=col,
                padx=15,
                pady=12
            )

        for r, row in enumerate(rows, start=1):

            values = [
                row["attendance_date"],
                row["subject_code"],
                row["subject_name"] or "",
                row["status"]
            ]

            for c, value in enumerate(values):

                ctk.CTkLabel(
                    table,
                    text=str(value)
                ).grid(
                    row=r,
                    column=c,
                    padx=15,
                    pady=8
                )

    # =========================================================
    # MARKS
    # =========================================================

    def show_marks(self):

        self.page_title.configure(
            text="My Marks"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                m.subject_code,
                s.subject_name,
                m.internal_marks,
                m.external_marks,
                m.total_marks,
                m.grade
            FROM marks m
            LEFT JOIN subjects s
                ON m.subject_code = s.subject_code
            WHERE m.student_id = %s
            ORDER BY s.subject_name
        """, (self.student_id,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

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

        headers = [
            "Subject Code",
            "Subject",
            "Internal / 40",
            "External / 60",
            "Total / 100",
            "Grade"
        ]

        for col, header in enumerate(headers):

            ctk.CTkLabel(
                table,
                text=header,
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=col,
                padx=12,
                pady=12
            )

        for r, row in enumerate(rows, start=1):

            values = [
                row["subject_code"],
                row["subject_name"] or "",
                row["internal_marks"],
                row["external_marks"],
                row["total_marks"],
                row["grade"]
            ]

            for c, value in enumerate(values):

                ctk.CTkLabel(
                    table,
                    text=str(value)
                ).grid(
                    row=r,
                    column=c,
                    padx=12,
                    pady=8
                )

    # =========================================================
    # TIMETABLE
    # =========================================================

    def show_timetable(self):

        self.page_title.configure(
            text="My Timetable"
        )

        self.clear_content()

        conn = self.get_connection()

        if not conn:
            return

        cursor = conn.cursor(
            dictionary=True
        )

        rows = []

        try:

            # =================================================
            # GET STUDENT'S CURRENT COURSE AND SEMESTER
            # =================================================

            cursor.execute("""
                SELECT
                    e.course_code,
                    e.semester,
                    c.course_name
                FROM enrollments e
                LEFT JOIN courses c
                    ON e.course_code = c.course_code
                WHERE e.student_id = %s
                AND e.status != 'Dropped'
                ORDER BY e.semester DESC
                LIMIT 1
            """, (self.student_id,))

            enrollment = cursor.fetchone()

            if not enrollment:

                self.show_empty_timetable(
                    "No Course Enrollment Found",
                    "You are not currently enrolled in any course."
                )

                return

            student_course = enrollment["course_code"]
            student_semester = enrollment["semester"]

            course_name = (
                enrollment["course_name"]
                or student_course
            )

            # =================================================
            # GET TIMETABLE FOR THAT COURSE AND SEMESTER
            # =================================================

            cursor.execute("""
                SELECT
                    t.day_of_week,
                    t.start_time,
                    t.end_time,

                    COALESCE(
                        c.course_name,
                        t.course_code
                    ) AS course_name,

                    t.course_code,

                    COALESCE(
                        s.subject_name,
                        t.subject_code
                    ) AS subject_name,

                    t.subject_code,

                    COALESCE(
                        tr.full_name,
                        t.teacher_id
                    ) AS teacher_name,

                    t.room_number,
                    t.semester

                FROM timetable t

                LEFT JOIN courses c
                    ON t.course_code = c.course_code

                LEFT JOIN subjects s
                    ON t.subject_code = s.subject_code

                LEFT JOIN teachers tr
                    ON t.teacher_id = tr.teacher_id

                WHERE t.course_code = %s
                AND t.semester = %s

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
                student_course,
                student_semester
            ))

            rows = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "Timetable Error",
                f"Unable to load timetable:\n\n{e}"
            )

            return

        finally:

            cursor.close()
            conn.close()

        # =====================================================
        # NO TIMETABLE
        # =====================================================

        if not rows:

            self.show_empty_timetable(
                "No Timetable Available",
                (
                    f"No timetable has been assigned for "
                    f"{course_name}, Semester {student_semester}."
                )
            )

            return

        # =====================================================
        # TIMETABLE HEADER
        # =====================================================

        ctk.CTkLabel(
            self.content,
            text="📅 My Class Timetable",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self.content,
            text=(
                f"{course_name}  •  "
                f"Semester {student_semester}"
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 5)
        )

        ctk.CTkLabel(
            self.content,
            text="Your scheduled classes",
            font=ctk.CTkFont(size=14)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        # =====================================================
        # TABLE
        # =====================================================

        table = ctk.CTkScrollableFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )

        table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        headers = [
            "Day",
            "Start",
            "End",
            "Course",
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
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=col,
                padx=12,
                pady=15,
                sticky="w"
            )

        # =====================================================
        # TABLE DATA
        # =====================================================

        for r, row in enumerate(rows, start=1):

            start_time = str(
                row["start_time"]
            )

            end_time = str(
                row["end_time"]
            )

            if len(start_time) >= 5:
                start_time = start_time[:5]

            if len(end_time) >= 5:
                end_time = end_time[:5]

            values = [
                row["day_of_week"],
                start_time,
                end_time,
                row["course_name"],
                row["subject_name"],
                row["subject_code"],
                row["teacher_name"],
                row["room_number"] or "-",
                row["semester"]
            ]

            for c, value in enumerate(values):

                ctk.CTkLabel(
                    table,
                    text=str(value or "-"),
                    font=ctk.CTkFont(size=13)
                ).grid(
                    row=r,
                    column=c,
                    padx=12,
                    pady=12,
                    sticky="w"
                )

    # =========================================================
    # EMPTY TIMETABLE
    # =========================================================

    def show_empty_timetable(
        self,
        title,
        message
    ):

        empty_card = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )

        empty_card.pack(
            fill="x",
            padx=20,
            pady=30
        )

        ctk.CTkLabel(
            empty_card,
            text="🕐",
            font=ctk.CTkFont(size=45)
        ).pack(
            pady=(30, 5)
        )

        ctk.CTkLabel(
            empty_card,
            text=title,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=5
        )

        ctk.CTkLabel(
            empty_card,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=700
        ).pack(
            pady=(0, 30)
        )

    # =========================================================
    # ANNOUNCEMENTS
    # =========================================================

    def show_announcements(self):

        self.page_title.configure(
            text="Announcements"
        )

        self.clear_content()

        top = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

        search_entry = ctk.CTkEntry(
            top,
            placeholder_text="Search announcements..."
        )

        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        notices = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )

        notices.pack(
            fill="both",
            expand=True,
            padx=10
        )

        def load_announcements():

            for widget in notices.winfo_children():
                widget.destroy()

            search = search_entry.get().strip()

            conn = self.get_connection()

            if not conn:
                return

            cursor = conn.cursor(
                dictionary=True
            )

            try:

                cursor.execute("""
                    SELECT
                        id,
                        title,
                        message,
                        target_audience,
                        announcement_date
                    FROM announcements
                    WHERE LOWER(
                        TRIM(target_audience)
                    ) IN (
                        'all',
                        'student',
                        'students'
                    )
                    AND (
                        title LIKE %s
                        OR message LIKE %s
                        OR target_audience LIKE %s
                    )
                    ORDER BY
                        announcement_date DESC,
                        id DESC
                """, (
                    f"%{search}%",
                    f"%{search}%",
                    f"%{search}%"
                ))

                announcements = cursor.fetchall()

            except Exception as e:

                print(
                    "Announcements error:",
                    e
                )

                announcements = []

            finally:

                cursor.close()
                conn.close()

            if not announcements:

                empty = ctk.CTkFrame(
                    notices,
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
                ).pack(
                    pady=(25, 5)
                )

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
                    text="New announcements will appear here.",
                    font=ctk.CTkFont(size=13)
                ).pack(
                    pady=(0, 25)
                )

                return

            for announcement in announcements:

                card = ctk.CTkFrame(
                    notices,
                    fg_color="white",
                    corner_radius=12
                )

                card.pack(
                    fill="x",
                    padx=10,
                    pady=8
                )

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
                    ),
                    wraplength=700
                ).pack(
                    side="left",
                    padx=10
                )

                ctk.CTkLabel(
                    header,
                    text=str(
                        announcement[
                            "announcement_date"
                        ]
                    ),
                    font=ctk.CTkFont(size=12)
                ).pack(side="right")

                message_text = (
                    announcement["message"] or ""
                )

                if len(message_text) > 200:

                    message_text = (
                        message_text[:200]
                        + "..."
                    )

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
                    text=(
                        f"Audience: "
                        f"{announcement['target_audience']}"
                    ),
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

            dialog.title(
                "Announcement Details"
            )

            dialog.geometry(
                "650x500"
            )

            dialog.resizable(
                False,
                False
            )

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

            ctk.CTkLabel(
                dialog,
                text=(
                    f"Date: "
                    f"{announcement['announcement_date']}\n"
                    f"Audience: "
                    f"{announcement['target_audience']}"
                ),
                font=ctk.CTkFont(size=13)
            ).pack(pady=5)

            message_box = ctk.CTkTextbox(
                dialog,
                width=550,
                height=230
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
            ).pack(
                pady=(0, 20)
            )

        ctk.CTkButton(
            top,
            text="🔄 Refresh",
            width=100,
            command=load_announcements
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            top,
            text="Show All",
            width=100,
            command=lambda: [
                search_entry.delete(0, "end"),
                load_announcements()
            ]
        ).pack(
            side="left",
            padx=5
        )

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

                from login import LoginApp

                app = LoginApp()
                app.mainloop()

            except Exception as e:

                print(
                    "Login error:",
                    e
                )


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    app = StudentDashboard(
        student_id="25BCAB706",
        student_name="SAMEER SHAIKH"
    )

    app.mainloop()