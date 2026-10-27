import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class CoursesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F5F7FB"
        )

        self.create_ui()
        self.load_courses()

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
            text="📚 Course Management",
            font=("Arial", 26, "bold"),
            text_color="#111827"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 2)
        )

        ctk.CTkLabel(
            header,
            text="Add, update, delete and search courses",
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

        # Course Code
        ctk.CTkLabel(
            form,
            text="Course Code",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.course_code_entry = ctk.CTkEntry(
            form,
            width=220,
            height=35,
            placeholder_text="Enter course code"
        )

        self.course_code_entry.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Course Name
        ctk.CTkLabel(
            form,
            text="Course Name",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.course_name_entry = ctk.CTkEntry(
            form,
            width=280,
            height=35,
            placeholder_text="Enter course name"
        )

        self.course_name_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # Duration
        ctk.CTkLabel(
            form,
            text="Duration",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=(18, 5),
            sticky="w"
        )

        self.duration_entry = ctk.CTkEntry(
            form,
            width=180,
            height=35,
            placeholder_text="e.g. 3 Years"
        )

        self.duration_entry.grid(
            row=1,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=1,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add",
            width=90,
            height=35,
            command=self.add_course
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="✏ Update",
            width=90,
            height=35,
            command=self.update_course
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
            command=self.delete_course
        ).pack(
            side="left",
            padx=3
        )

        # Description
        ctk.CTkLabel(
            form,
            text="Description",
            font=("Arial", 12, "bold")
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="nw"
        )

        self.description_entry = ctk.CTkEntry(
            form,
            height=35,
            placeholder_text="Enter course description"
        )

        self.description_entry.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=15,
            pady=(0, 18),
            sticky="ew"
        )

        # -------------------------------------------------
        # SEARCH BAR
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
            width=320,
            height=35,
            placeholder_text="Search course code or name"
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
            height=35,
            command=self.search_courses
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            search_frame,
            text="🔄 Refresh",
            width=100,
            height=35,
            command=self.load_courses
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
            "course_code",
            "course_name",
            "duration",
            "description"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "course_code",
            text="Course Code"
        )

        self.tree.heading(
            "course_name",
            text="Course Name"
        )

        self.tree.heading(
            "duration",
            text="Duration"
        )

        self.tree.heading(
            "description",
            text="Description"
        )

        self.tree.column(
            "course_code",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "course_name",
            width=260
        )

        self.tree.column(
            "duration",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=450
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
            self.select_course
        )

    # =====================================================
    # LOAD COURSES FROM LOCAL MYSQL
    # =====================================================

    def load_courses(self):

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
                    course_code,
                    course_name,
                    duration,
                    description
                FROM courses
                ORDER BY course_code ASC
            """

            cursor.execute(query)

            courses = cursor.fetchall()

            self.clear_table()

            for course in courses:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        course.get("course_code", ""),
                        course.get("course_name", ""),
                        course.get("duration", ""),
                        course.get("description", "")
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load courses.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # ADD COURSE
    # =====================================================

    def add_course(self):

        course_code = (
            self.course_code_entry
            .get()
            .strip()
        )

        course_name = (
            self.course_name_entry
            .get()
            .strip()
        )

        duration = (
            self.duration_entry
            .get()
            .strip()
        )

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not course_code:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the course code."
            )

            return

        if not course_name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the course name."
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

            # Check duplicate course code
            check_query = """
                SELECT course_code
                FROM courses
                WHERE course_code = %s
                LIMIT 1
            """

            cursor.execute(
                check_query,
                (course_code,)
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Duplicate Course",
                    "Course code already exists."
                )

                return

            query = """
                INSERT INTO courses
                (
                    course_code,
                    course_name,
                    duration,
                    description
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
                    course_code,
                    course_name,
                    duration,
                    description
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Course added successfully."
            )

            self.clear_form()
            self.load_courses()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add course.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # UPDATE COURSE
    # =====================================================

    def update_course(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Course",
                "Please select a course from the table."
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
            return

        old_course_code = str(
            values[0]
        )

        course_code = (
            self.course_code_entry
            .get()
            .strip()
        )

        course_name = (
            self.course_name_entry
            .get()
            .strip()
        )

        duration = (
            self.duration_entry
            .get()
            .strip()
        )

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not course_code:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the course code."
            )

            return

        if not course_name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the course name."
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

            # Check duplicate only if course code changed
            if course_code != old_course_code:

                check_query = """
                    SELECT course_code
                    FROM courses
                    WHERE course_code = %s
                    LIMIT 1
                """

                cursor.execute(
                    check_query,
                    (course_code,)
                )

                existing = cursor.fetchone()

                if existing:

                    messagebox.showwarning(
                        "Duplicate Course",
                        "Course code already exists."
                    )

                    return

            query = """
                UPDATE courses
                SET
                    course_code = %s,
                    course_name = %s,
                    duration = %s,
                    description = %s
                WHERE course_code = %s
            """

            cursor.execute(
                query,
                (
                    course_code,
                    course_name,
                    duration,
                    description,
                    old_course_code
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Course updated successfully."
            )

            self.clear_form()
            self.load_courses()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update course.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # DELETE COURSE
    # =====================================================

    def delete_course(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Course",
                "Please select a course from the table."
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
            return

        course_code = str(
            values[0]
        )

        course_name = str(
            values[1]
        )

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n"
            f"{course_code} - {course_name}?"
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
                DELETE FROM courses
                WHERE course_code = %s
            """

            cursor.execute(
                query,
                (course_code,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Course deleted successfully."
            )

            self.clear_form()
            self.load_courses()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete course.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # SEARCH COURSES
    # =====================================================

    def search_courses(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        if not search_text:

            self.load_courses()

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
                    course_code,
                    course_name,
                    duration,
                    description
                FROM courses
                WHERE
                    course_code LIKE %s
                    OR course_name LIKE %s
                ORDER BY course_code ASC
            """

            cursor.execute(
                query,
                (
                    search_value,
                    search_value
                )
            )

            courses = cursor.fetchall()

            self.clear_table()

            for course in courses:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        course.get("course_code", ""),
                        course.get("course_name", ""),
                        course.get("duration", ""),
                        course.get("description", "")
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search courses.\n\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # =====================================================
    # SELECT COURSE
    # =====================================================

    def select_course(self, event=None):

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

        if len(values) < 4:
            return

        self.course_code_entry.delete(
            0,
            "end"
        )

        self.course_code_entry.insert(
            0,
            values[0]
        )

        self.course_name_entry.delete(
            0,
            "end"
        )

        self.course_name_entry.insert(
            0,
            values[1]
        )

        self.duration_entry.delete(
            0,
            "end"
        )

        self.duration_entry.insert(
            0,
            values[2]
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.description_entry.insert(
            0,
            values[3]
        )

    # =====================================================
    # CLEAR TABLE
    # =====================================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.course_code_entry.delete(
            0,
            "end"
        )

        self.course_name_entry.delete(
            0,
            "end"
        )

        self.duration_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.search_entry.delete(
            0,
            "end"
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
        "Course Management"
    )

    app.geometry(
        "1200x700"
    )

    app.minsize(
        1100,
        650
    )

    page = CoursesPage(
        app
    )

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()