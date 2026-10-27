import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_connection


class TimetablePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F5F7FB"
        )

        # Maps displayed text -> database value
        self.course_data = {}
        self.subject_data = {}
        self.teacher_data = {}

        self.create_ui()

        self.load_courses()
        self.load_subjects()
        self.load_teachers()
        self.load_timetable()

    # =====================================================
    # USER INTERFACE
    # =====================================================

    def create_ui(self):

        # =================================================
        # HEADER
        # =================================================

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
            text="🕐 Timetable Management",
            font=("Arial", 26, "bold"),
            text_color="#111827"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            header,
            text="Create and manage class schedules",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        # =================================================
        # FORM
        # =================================================

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

        # =================================================
        # COURSE
        # =================================================

        ctk.CTkLabel(
            form,
            text="Course",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.course_combo = ctk.CTkComboBox(
            form,
            width=240,
            height=35,
            values=["Select Course"]
        )

        self.course_combo.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 12)
        )

        # =================================================
        # SUBJECT
        # =================================================

        ctk.CTkLabel(
            form,
            text="Subject",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.subject_combo = ctk.CTkComboBox(
            form,
            width=240,
            height=35,
            values=["Select Subject"]
        )

        self.subject_combo.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 12)
        )

        # =================================================
        # TEACHER
        # =================================================

        ctk.CTkLabel(
            form,
            text="Teacher",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.teacher_combo = ctk.CTkComboBox(
            form,
            width=240,
            height=35,
            values=["Select Teacher"]
        )

        self.teacher_combo.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 12)
        )

        # =================================================
        # DAY
        # =================================================

        ctk.CTkLabel(
            form,
            text="Day",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=3,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.day_combo = ctk.CTkComboBox(
            form,
            width=150,
            height=35,
            values=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ]
        )

        self.day_combo.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 12)
        )

        self.day_combo.set("Monday")

        # =================================================
        # START TIME
        # =================================================

        ctk.CTkLabel(
            form,
            text="Start Time",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.start_time_entry = ctk.CTkEntry(
            form,
            width=240,
            height=35,
            placeholder_text="HH:MM:SS"
        )

        self.start_time_entry.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        self.start_time_entry.insert(
            0,
            "09:00:00"
        )

        # =================================================
        # END TIME
        # =================================================

        ctk.CTkLabel(
            form,
            text="End Time",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.end_time_entry = ctk.CTkEntry(
            form,
            width=240,
            height=35,
            placeholder_text="HH:MM:SS"
        )

        self.end_time_entry.grid(
            row=3,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        self.end_time_entry.insert(
            0,
            "10:00:00"
        )

        # =================================================
        # ROOM
        # =================================================

        ctk.CTkLabel(
            form,
            text="Room Number",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.room_entry = ctk.CTkEntry(
            form,
            width=240,
            height=35,
            placeholder_text="Example: Lab 101"
        )

        self.room_entry.grid(
            row=3,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # =================================================
        # SEMESTER
        # =================================================

        ctk.CTkLabel(
            form,
            text="Semester",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=3,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.semester_combo = ctk.CTkComboBox(
            form,
            width=150,
            height=35,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8"
            ]
        )

        self.semester_combo.grid(
            row=3,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        self.semester_combo.set("3")

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add",
            width=100,
            height=35,
            command=self.add_timetable
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="✏ Update",
            width=100,
            height=35,
            command=self.update_timetable
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="🗑 Delete",
            width=100,
            height=35,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_timetable
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="🧹 Clear",
            width=100,
            height=35,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        # =================================================
        # SEARCH
        # =================================================

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
            placeholder_text="Search course, subject or teacher"
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
            command=self.search_timetable
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="🔄 Show All",
            width=100,
            command=self.load_timetable
        ).pack(
            side="left",
            padx=5
        )

        # =================================================
        # TABLE
        # =================================================

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
            "course",
            "subject",
            "teacher",
            "day",
            "start",
            "end",
            "room",
            "semester"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "course": "Course",
            "subject": "Subject",
            "teacher": "Teacher",
            "day": "Day",
            "start": "Start",
            "end": "End",
            "room": "Room",
            "semester": "Sem"
        }

        for column, heading in headings.items():

            self.tree.heading(
                column,
                text=heading
            )

        widths = {
            "id": 50,
            "course": 220,
            "subject": 220,
            "teacher": 180,
            "day": 100,
            "start": 90,
            "end": 90,
            "room": 100,
            "semester": 60
        }

        for column, width in widths.items():

            self.tree.column(
                column,
                width=width,
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
    # LOAD COURSES
    # =====================================================

    def load_courses(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT course_code, course_name
                FROM courses
                ORDER BY course_name
                """
            )

            rows = cursor.fetchall()

            self.course_data.clear()

            course_values = []

            for row in rows:

                course_code = row[0]
                course_name = row[1]

                # Display name + code
                display_text = f"{course_name} ({course_code})"

                course_values.append(
                    display_text
                )

                # Store database code
                self.course_data[display_text] = course_code

            if course_values:

                self.course_combo.configure(
                    values=course_values
                )

                self.course_combo.set(
                    "Select Course"
                )

            else:

                self.course_combo.configure(
                    values=["No courses saved"]
                )

                self.course_combo.set(
                    "No courses saved"
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
    # LOAD SUBJECTS
    # =====================================================

    def load_subjects(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT subject_code, subject_name
                FROM subjects
                ORDER BY subject_name
                """
            )

            rows = cursor.fetchall()

            self.subject_data.clear()

            subject_values = []

            for row in rows:

                subject_code = row[0]
                subject_name = row[1]

                # Display name + code
                display_text = f"{subject_name} ({subject_code})"

                subject_values.append(
                    display_text
                )

                # Store database code
                self.subject_data[display_text] = subject_code

            if subject_values:

                self.subject_combo.configure(
                    values=subject_values
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
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()

    # =====================================================
    # LOAD TEACHERS
    # =====================================================

    def load_teachers(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT teacher_id, full_name
                FROM teachers
                ORDER BY full_name
                """
            )

            rows = cursor.fetchall()

            self.teacher_data.clear()

            teacher_values = []

            for row in rows:

                teacher_id = row[0]
                teacher_name = row[1]

                # Display teacher name + ID
                display_text = f"{teacher_name} ({teacher_id})"

                teacher_values.append(
                    display_text
                )

                # Store database ID
                self.teacher_data[display_text] = teacher_id

            if teacher_values:

                self.teacher_combo.configure(
                    values=teacher_values
                )

                self.teacher_combo.set(
                    "Select Teacher"
                )

            else:

                self.teacher_combo.configure(
                    values=["No teachers saved"]
                )

                self.teacher_combo.set(
                    "No teachers saved"
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
    # ADD
    # =====================================================

    def add_timetable(self):

        course_display = self.course_combo.get()
        subject_display = self.subject_combo.get()
        teacher_display = self.teacher_combo.get()

        day = self.day_combo.get()

        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()

        room = self.room_entry.get().strip()

        semester = self.semester_combo.get()

        # Validate course
        if course_display not in self.course_data:

            messagebox.showwarning(
                "Invalid Course",
                "Please select a saved course."
            )

            return

        # Validate subject
        if subject_display not in self.subject_data:

            messagebox.showwarning(
                "Invalid Subject",
                "Please select a saved subject."
            )

            return

        # Validate teacher
        if teacher_display not in self.teacher_data:

            messagebox.showwarning(
                "Invalid Teacher",
                "Please select a saved teacher."
            )

            return

        # Get actual database values
        course_code = self.course_data[course_display]
        subject_code = self.subject_data[subject_display]
        teacher_id = self.teacher_data[teacher_display]

        if not start_time or not end_time:

            messagebox.showwarning(
                "Missing Time",
                "Please enter start and end time."
            )

            return

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO timetable
                (
                    course_code,
                    subject_code,
                    teacher_id,
                    day_of_week,
                    start_time,
                    end_time,
                    room_number,
                    semester
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    course_code,
                    subject_code,
                    teacher_id,
                    day,
                    start_time,
                    end_time,
                    room,
                    semester
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Timetable entry added successfully."
            )

            self.clear_form()
            self.load_timetable()

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
    # UPDATE
    # =====================================================

    def update_timetable(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select a timetable record."
            )

            return

        item = self.tree.item(
            selected[0]
        )

        record_id = item["values"][0]

        course_display = self.course_combo.get()
        subject_display = self.subject_combo.get()
        teacher_display = self.teacher_combo.get()

        day = self.day_combo.get()

        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()

        room = self.room_entry.get().strip()

        semester = self.semester_combo.get()

        if course_display not in self.course_data:

            messagebox.showwarning(
                "Invalid Course",
                "Please select a saved course."
            )

            return

        if subject_display not in self.subject_data:

            messagebox.showwarning(
                "Invalid Subject",
                "Please select a saved subject."
            )

            return

        if teacher_display not in self.teacher_data:

            messagebox.showwarning(
                "Invalid Teacher",
                "Please select a saved teacher."
            )

            return

        # Get actual database values
        course_code = self.course_data[course_display]
        subject_code = self.subject_data[subject_display]
        teacher_id = self.teacher_data[teacher_display]

        if not start_time or not end_time:

            messagebox.showwarning(
                "Missing Time",
                "Please enter start and end time."
            )

            return

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE timetable
                SET course_code = %s,
                    subject_code = %s,
                    teacher_id = %s,
                    day_of_week = %s,
                    start_time = %s,
                    end_time = %s,
                    room_number = %s,
                    semester = %s
                WHERE id = %s
                """,
                (
                    course_code,
                    subject_code,
                    teacher_id,
                    day,
                    start_time,
                    end_time,
                    room,
                    semester,
                    record_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Timetable entry updated successfully."
            )

            self.clear_form()
            self.load_timetable()

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
    # DELETE
    # =====================================================

    def delete_timetable(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select a timetable record."
            )

            return

        item = self.tree.item(
            selected[0]
        )

        record_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this timetable entry?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM timetable
                WHERE id = %s
                """,
                (record_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Timetable entry deleted successfully."
            )

            self.clear_form()
            self.load_timetable()

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
    # LOAD TIMETABLE
    # =====================================================

    def load_timetable(self):

        query = """
            SELECT
                t.id,

                CONCAT(
                    COALESCE(c.course_name, t.course_code),
                    ' (',
                    t.course_code,
                    ')'
                ),

                CONCAT(
                    COALESCE(s.subject_name, t.subject_code),
                    ' (',
                    t.subject_code,
                    ')'
                ),

                CONCAT(
                    COALESCE(tr.full_name, t.teacher_id),
                    ' (',
                    t.teacher_id,
                    ')'
                ),

                t.day_of_week,
                t.start_time,
                t.end_time,
                t.room_number,
                t.semester

            FROM timetable t

            LEFT JOIN courses c
                ON t.course_code = c.course_code

            LEFT JOIN subjects s
                ON t.subject_code = s.subject_code

            LEFT JOIN teachers tr
                ON t.teacher_id = tr.teacher_id

            ORDER BY
                FIELD(
                    t.day_of_week,
                    'Monday',
                    'Tuesday',
                    'Wednesday',
                    'Thursday',
                    'Friday',
                    'Saturday'
                ),
                t.start_time
        """

        self.load_table(query)

    # =====================================================
    # SEARCH
    # =====================================================

    def search_timetable(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_timetable()

            return

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    t.id,

                    CONCAT(
                        COALESCE(c.course_name, t.course_code),
                        ' (',
                        t.course_code,
                        ')'
                    ),

                    CONCAT(
                        COALESCE(s.subject_name, t.subject_code),
                        ' (',
                        t.subject_code,
                        ')'
                    ),

                    CONCAT(
                        COALESCE(tr.full_name, t.teacher_id),
                        ' (',
                        t.teacher_id,
                        ')'
                    ),

                    t.day_of_week,
                    t.start_time,
                    t.end_time,
                    t.room_number,
                    t.semester

                FROM timetable t

                LEFT JOIN courses c
                    ON t.course_code = c.course_code

                LEFT JOIN subjects s
                    ON t.subject_code = s.subject_code

                LEFT JOIN teachers tr
                    ON t.teacher_id = tr.teacher_id

                WHERE
                    t.course_code LIKE %s
                    OR c.course_name LIKE %s
                    OR t.subject_code LIKE %s
                    OR s.subject_name LIKE %s
                    OR t.teacher_id LIKE %s
                    OR tr.full_name LIKE %s

                ORDER BY
                    FIELD(
                        t.day_of_week,
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ),
                    t.start_time
                """,
                (
                    "%" + search_text + "%",
                    "%" + search_text + "%",
                    "%" + search_text + "%",
                    "%" + search_text + "%",
                    "%" + search_text + "%",
                    "%" + search_text + "%"
                )
            )

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=row
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
    # LOAD TABLE
    # =====================================================

    def load_table(self, query):

        connection = create_connection()

        if connection is None:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=row
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
    # CLEAR TABLE
    # =====================================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    # =====================================================
    # SELECT RECORD
    # =====================================================

    def select_record(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(
            selected[0]
        )

        values = item["values"]

        if not values:
            return

        # -------------------------------------------------
        # Course
        # -------------------------------------------------

        course_display = str(values[1])

        if course_display in self.course_data:

            self.course_combo.set(
                course_display
            )

        else:

            # Match using course code inside brackets
            course_code = str(values[1]).split("(")[-1].replace(")", "").strip()

            for display, code in self.course_data.items():

                if str(code) == course_code:

                    self.course_combo.set(
                        display
                    )

                    break

        # -------------------------------------------------
        # Subject
        # -------------------------------------------------

        subject_display = str(values[2])

        if subject_display in self.subject_data:

            self.subject_combo.set(
                subject_display
            )

        else:

            subject_code = str(values[2]).split("(")[-1].replace(")", "").strip()

            for display, code in self.subject_data.items():

                if str(code) == subject_code:

                    self.subject_combo.set(
                        display
                    )

                    break

        # -------------------------------------------------
        # Teacher
        # -------------------------------------------------

        teacher_display = str(values[3])

        if teacher_display in self.teacher_data:

            self.teacher_combo.set(
                teacher_display
            )

        else:

            teacher_id = teacher_display.split("(")[-1].replace(")", "").strip()

            for display, tid in self.teacher_data.items():

                if str(tid) == teacher_id:

                    self.teacher_combo.set(
                        display
                    )

                    break

        # -------------------------------------------------
        # Day
        # -------------------------------------------------

        self.day_combo.set(
            values[4]
        )

        # -------------------------------------------------
        # Start Time
        # -------------------------------------------------

        self.start_time_entry.delete(
            0,
            "end"
        )

        self.start_time_entry.insert(
            0,
            str(values[5])
        )

        # -------------------------------------------------
        # End Time
        # -------------------------------------------------

        self.end_time_entry.delete(
            0,
            "end"
        )

        self.end_time_entry.insert(
            0,
            str(values[6])
        )

        # -------------------------------------------------
        # Room
        # -------------------------------------------------

        self.room_entry.delete(
            0,
            "end"
        )

        if values[7]:

            self.room_entry.insert(
                0,
                str(values[7])
            )

        # -------------------------------------------------
        # Semester
        # -------------------------------------------------

        self.semester_combo.set(
            str(values[8])
        )

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.course_combo.set(
            "Select Course"
        )

        self.subject_combo.set(
            "Select Subject"
        )

        self.teacher_combo.set(
            "Select Teacher"
        )

        self.day_combo.set(
            "Monday"
        )

        self.start_time_entry.delete(
            0,
            "end"
        )

        self.start_time_entry.insert(
            0,
            "09:00:00"
        )

        self.end_time_entry.delete(
            0,
            "end"
        )

        self.end_time_entry.insert(
            0,
            "10:00:00"
        )

        self.room_entry.delete(
            0,
            "end"
        )

        self.semester_combo.set(
            "3"
        )


# =========================================================
# STANDALONE TEST
# =========================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title(
        "Timetable Management"
    )

    app.geometry(
        "1450x800"
    )

    page = TimetablePage(app)

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()