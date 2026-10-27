import customtkinter as ctk
from tkinter import messagebox

from gui.students import StudentsPage
from gui.teachers import TeachersPage
from gui.courses import CoursesPage
from gui.subjects import SubjectsPage
from gui.attendance import AttendancePage
from gui.marks import MarksPage
from gui.timetable import TimetablePage
from gui.announcements import AnnouncementsPage
from gui.reports import ReportsPage

from database import create_connection


class AdminDashboard(ctk.CTk):

    def __init__(self, full_name="System Administrator"):
        super().__init__()

        # =========================================================
        # WINDOW SETTINGS
        # =========================================================

        self.full_name = full_name

        self.title("Student Management System - Admin Dashboard")
        self.geometry("1450x850")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # =========================================================
        # MAIN COLORS
        # =========================================================

        self.sidebar_color = "#102A43"
        self.sidebar_hover = "#1D4E73"
        self.background_color = "#F4F7FA"
        self.card_color = "#FFFFFF"
        self.text_color = "#172B4D"
        self.secondary_text = "#6B7C93"

        self.configure(
            fg_color=self.background_color
        )

        # =========================================================
        # MAIN GRID
        # =========================================================

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # =========================================================
        # SIDEBAR
        # =========================================================

        self.create_sidebar()

        # =========================================================
        # MAIN AREA
        # =========================================================

        self.create_main_area()

        # =========================================================
        # SHOW DASHBOARD
        # =========================================================

        self.show_dashboard()

    # =============================================================
    # SIDEBAR
    # =============================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        self.sidebar.grid_rowconfigure(
            12,
            weight=1
        )

        # =========================================================
        # LOGO / TITLE
        # =========================================================

        self.logo_title = ctk.CTkLabel(
            self.sidebar,
            text="STUDENT\nMANAGEMENT",
            font=ctk.CTkFont(
                family="Arial",
                size=22,
                weight="bold"
            ),
            text_color="white",
            justify="center"
        )

        self.logo_title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(30, 5)
        )

        self.logo_subtitle = ctk.CTkLabel(
            self.sidebar,
            text="ADMIN PANEL",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#8FB3CC"
        )

        self.logo_subtitle.grid(
            row=1,
            column=0,
            pady=(0, 30)
        )

        # =========================================================
        # NAVIGATION BUTTONS
        # =========================================================

        self.create_nav_button(
            "Dashboard",
            self.show_dashboard,
            2
        )

        self.create_nav_button(
            "Students",
            self.show_students,
            3
        )

        self.create_nav_button(
            "Teachers",
            self.show_teachers,
            4
        )

        self.create_nav_button(
            "Courses",
            self.show_courses,
            5
        )

        self.create_nav_button(
            "Subjects",
            self.show_subjects,
            6
        )

        self.create_nav_button(
            "Attendance",
            self.show_attendance,
            7
        )

        self.create_nav_button(
            "Marks",
            self.show_marks,
            8
        )

        self.create_nav_button(
            "Timetable",
            self.show_timetable,
            9
        )

        self.create_nav_button(
            "Announcements",
            self.show_announcements,
            10
        )

        self.create_nav_button(
            "Reports",
            self.show_reports,
            11
        )

        # =========================================================
        # LOGOUT BUTTON
        # =========================================================

        self.logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            height=45,
            corner_radius=8,
            fg_color="#C0392B",
            hover_color="#962D22",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.logout
        )

        self.logout_button.grid(
            row=13,
            column=0,
            padx=20,
            pady=(10, 30),
            sticky="ew"
        )

    # =============================================================
    # CREATE NAVIGATION BUTTON
    # =============================================================

    def create_nav_button(
        self,
        text,
        command,
        row
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.sidebar_hover,
            text_color="white",
            anchor="w",
            font=ctk.CTkFont(
                size=14
            ),
            command=command
        )

        button.grid(
            row=row,
            column=0,
            padx=15,
            pady=3,
            sticky="ew"
        )

    # =============================================================
    # MAIN AREA
    # =============================================================

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.background_color
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_area.grid_rowconfigure(
            0,
            weight=1
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )

    # =============================================================
    # CLEAR MAIN AREA
    # =============================================================

    def clear_main_area(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    # =============================================================
    # DASHBOARD
    # =============================================================

    def show_dashboard(self):

        self.clear_main_area()

        dashboard_frame = ctk.CTkFrame(
            self.main_area,
            fg_color=self.background_color
        )

        dashboard_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        # =========================================================
        # HEADER
        # =========================================================

        welcome_label = ctk.CTkLabel(
            dashboard_frame,
            text=f"Welcome, {self.full_name}",
            font=ctk.CTkFont(
                family="Arial",
                size=30,
                weight="bold"
            ),
            text_color=self.text_color,
            anchor="w"
        )

        welcome_label.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            dashboard_frame,
            text="Here's an overview of your student management system.",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=self.secondary_text,
            anchor="w"
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 25)
        )

        # =========================================================
        # STATISTICS
        # =========================================================

        stats = self.get_statistics()

        cards_frame = ctk.CTkFrame(
            dashboard_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x"
        )

        for i in range(4):

            cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_stat_card(
            cards_frame,
            "Students",
            stats["students"],
            0
        )

        self.create_stat_card(
            cards_frame,
            "Teachers",
            stats["teachers"],
            1
        )

        self.create_stat_card(
            cards_frame,
            "Courses",
            stats["courses"],
            2
        )

        self.create_stat_card(
            cards_frame,
            "Subjects",
            stats["subjects"],
            3
        )

        # =========================================================
        # ATTENDANCE CARD
        # =========================================================

        attendance_card = ctk.CTkFrame(
            dashboard_frame,
            fg_color=self.card_color,
            corner_radius=15
        )

        attendance_card.pack(
            fill="x",
            pady=(30, 20)
        )

        attendance_title = ctk.CTkLabel(
            attendance_card,
            text="Overall Attendance",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.text_color
        )

        attendance_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        attendance_value = ctk.CTkLabel(
            attendance_card,
            text=f"{stats['attendance']:.1f}%",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#1976D2"
        )

        attendance_value.pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        progress = ctk.CTkProgressBar(
            attendance_card,
            height=12,
            corner_radius=6
        )

        progress.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        progress.set(
            stats["attendance"] / 100
            if stats["attendance"] > 0
            else 0
        )

        # =========================================================
        # RECENT ACTIVITIES
        # =========================================================

        activity_card = ctk.CTkFrame(
            dashboard_frame,
            fg_color=self.card_color,
            corner_radius=15
        )

        activity_card.pack(
            fill="both",
            expand=True
        )

        activity_title = ctk.CTkLabel(
            activity_card,
            text="Recent Activities",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.text_color
        )

        activity_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        activities = [
            "Student records updated",
            "Attendance records checked",
            "Marks information updated",
            "New course information available"
        ]

        for activity in activities:

            label = ctk.CTkLabel(
                activity_card,
                text="•  " + activity,
                font=ctk.CTkFont(
                    size=14
                ),
                text_color=self.secondary_text,
                anchor="w"
            )

            label.pack(
                fill="x",
                padx=25,
                pady=6
            )

    # =============================================================
    # STATISTICS CARD
    # =============================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=15,
            height=130
        )

        card.grid(
            row=0,
            column=column,
            padx=7,
            sticky="nsew"
        )

        card.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=14
            ),
            text_color=self.secondary_text
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.text_color
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

    # =============================================================
    # DATABASE STATISTICS
    # =============================================================

    def get_statistics(self):

        statistics = {
            "students": 0,
            "teachers": 0,
            "courses": 0,
            "subjects": 0,
            "attendance": 0
        }

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if connection is None:
                return statistics

            cursor = connection.cursor()

            # Students
            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )

            result = cursor.fetchone()

            if result:
                statistics["students"] = result[0]

            # Teachers
            cursor.execute(
                "SELECT COUNT(*) FROM teachers"
            )

            result = cursor.fetchone()

            if result:
                statistics["teachers"] = result[0]

            # Courses
            cursor.execute(
                "SELECT COUNT(*) FROM courses"
            )

            result = cursor.fetchone()

            if result:
                statistics["courses"] = result[0]

            # Subjects
            cursor.execute(
                "SELECT COUNT(*) FROM subjects"
            )

            result = cursor.fetchone()

            if result:
                statistics["subjects"] = result[0]

            # Attendance
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(
                        CASE
                            WHEN LOWER(status) = 'present'
                            THEN 1
                            ELSE 0
                        END
                    ) AS present
                FROM attendance
                """
            )

            result = cursor.fetchone()

            if result and result[0]:

                total = result[0]
                present = result[1] or 0

                statistics["attendance"] = (
                    present / total
                ) * 100

        except Exception as e:

            print(
                "Error loading dashboard statistics:",
                e
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

        return statistics

    # =============================================================
    # STUDENTS
    # =============================================================

    def show_students(self):

        self.clear_main_area()

        page = StudentsPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # TEACHERS
    # =============================================================

    def show_teachers(self):

        self.clear_main_area()

        page = TeachersPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # COURSES
    # =============================================================

    def show_courses(self):

        self.clear_main_area()

        page = CoursesPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # SUBJECTS
    # =============================================================

    def show_subjects(self):

        self.clear_main_area()

        page = SubjectsPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # ATTENDANCE
    # =============================================================

    def show_attendance(self):

        self.clear_main_area()

        page = AttendancePage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # MARKS
    # =============================================================

    def show_marks(self):

        self.clear_main_area()

        page = MarksPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # TIMETABLE
    # =============================================================

    def show_timetable(self):

        self.clear_main_area()

        page = TimetablePage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # ANNOUNCEMENTS
    # =============================================================

    def show_announcements(self):

        self.clear_main_area()

        page = AnnouncementsPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # REPORTS
    # =============================================================

    def show_reports(self):

        self.clear_main_area()

        page = ReportsPage(
            self.main_area
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =============================================================
    # LOGOUT
    # =============================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:

            self.destroy()

            try:

                from login import LoginApp

                login = LoginApp()

                login.mainloop()

            except Exception as e:

                print(
                    "Unable to reopen login:",
                    e
                )


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    app = AdminDashboard(
        full_name="System Administrator"
    )

    app.mainloop()