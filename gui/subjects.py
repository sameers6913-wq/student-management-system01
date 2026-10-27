import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_connection


class SubjectsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#F5F7FA"
        )

        self.editing_subject_code = None

        self.course_map = {}

        self.create_widgets()

        self.load_courses()

        self.load_subjects()

    # =========================================================
    # UI
    # =========================================================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Subject Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#162B40"
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Manage academic subjects",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        )

        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # =====================================================
        # FORM
        # =====================================================

        form_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        form_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        form_frame.grid_columnconfigure(
            1,
            weight=1
        )

        form_frame.grid_columnconfigure(
            3,
            weight=1
        )

        # Subject Code

        ctk.CTkLabel(
            form_frame,
            text="Subject Code",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(20, 8),
            sticky="w"
        )

        self.subject_code_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter subject code"
        )

        self.subject_code_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=(20, 8),
            sticky="ew"
        )

        # Subject Name

        ctk.CTkLabel(
            form_frame,
            text="Subject Name",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=2,
            padx=(20, 10),
            pady=(20, 8),
            sticky="w"
        )

        self.subject_name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter subject name"
        )

        self.subject_name_entry.grid(
            row=0,
            column=3,
            padx=(10, 20),
            pady=(20, 8),
            sticky="ew"
        )

        # Course

        ctk.CTkLabel(
            form_frame,
            text="Course",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.course_combo = ctk.CTkComboBox(
            form_frame,
            values=["Loading..."]
        )

        self.course_combo.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="ew"
        )

        # Semester

        ctk.CTkLabel(
            form_frame,
            text="Semester",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=1,
            column=2,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.semester_combo = ctk.CTkComboBox(
            form_frame,
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

        self.semester_combo.set("3")

        self.semester_combo.grid(
            row=1,
            column=3,
            padx=(10, 20),
            pady=8,
            sticky="ew"
        )

        # Credits

        ctk.CTkLabel(
            form_frame,
            text="Credits",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.credits_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Example: 4"
        )

        self.credits_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8,
            sticky="ew"
        )

        # Description

        ctk.CTkLabel(
            form_frame,
            text="Description",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=2,
            column=2,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.description_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Subject description"
        )

        self.description_entry.grid(
            row=2,
            column=3,
            padx=(10, 20),
            pady=8,
            sticky="ew"
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            padx=20,
            pady=(10, 20),
            sticky="e"
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Subject",
            width=130,
            height=38,
            fg_color="#1769AA",
            hover_color="#12588E",
            command=self.save_subject
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            height=38,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        # =====================================================
        # SEARCH
        # =====================================================

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search subject code or subject name...",
            height=38,
            width=350
        )

        self.search_entry.pack(
            side="left"
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            height=38,
            command=self.search_subjects
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            search_frame,
            text="Show All",
            width=100,
            height=38,
            fg_color="#374151",
            hover_color="#1F2937",
            command=self.load_subjects
        ).pack(
            side="left"
        )

        # =====================================================
        # TABLE
        # =====================================================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        columns = (
            "subject_code",
            "subject_name",
            "course_code",
            "semester",
            "credits",
            "description"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "subject_code",
            text="Subject Code"
        )

        self.tree.heading(
            "subject_name",
            text="Subject Name"
        )

        self.tree.heading(
            "course_code",
            text="Course"
        )

        self.tree.heading(
            "semester",
            text="Semester"
        )

        self.tree.heading(
            "credits",
            text="Credits"
        )

        self.tree.heading(
            "description",
            text="Description"
        )

        self.tree.column(
            "subject_code",
            width=140,
            anchor="center"
        )

        self.tree.column(
            "subject_name",
            width=260
        )

        self.tree.column(
            "course_code",
            width=140,
            anchor="center"
        )

        self.tree.column(
            "semester",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "credits",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "description",
            width=300
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

        # =====================================================
        # ACTION BUTTONS
        # =====================================================

        action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        action_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        ctk.CTkButton(
            action_frame,
            text="Edit Selected",
            width=130,
            command=self.edit_subject
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            width=130,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete_subject
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            action_frame,
            text="Refresh",
            width=100,
            fg_color="#374151",
            hover_color="#1F2937",
            command=self.load_subjects
        ).pack(
            side="right"
        )

    # =========================================================
    # LOAD COURSES FROM LOCAL MYSQL
    # =========================================================

    def load_courses(self):

        connection = create_connection()

        if connection is None:

            self.course_combo.configure(
                values=["Database unavailable"]
            )

            return

        try:

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT course_code, course_name
                FROM courses
                ORDER BY course_name ASC
            """

            cursor.execute(query)

            courses = cursor.fetchall()

            self.course_map = {}

            display_values = []

            for course in courses:

                code = course.get(
                    "course_code",
                    ""
                )

                name = course.get(
                    "course_name",
                    ""
                )

                display = f"{code} - {name}"

                self.course_map[display] = code

                display_values.append(display)

            if display_values:

                self.course_combo.configure(
                    values=display_values
                )

                self.course_combo.set(
                    display_values[0]
                )

            else:

                self.course_combo.configure(
                    values=["No courses available"]
                )

                self.course_combo.set(
                    "No courses available"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load courses.\n\n{e}"
            )

        finally:

            try:
                cursor.close()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # LOAD SUBJECTS FROM LOCAL MYSQL
    # =========================================================

    def load_subjects(self):

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to local MySQL."
            )

            return

        try:

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    subject_code,
                    subject_name,
                    course_code,
                    semester,
                    credits,
                    description
                FROM subjects
                ORDER BY subject_code ASC
            """

            cursor.execute(query)

            subjects = cursor.fetchall()

            for item in self.tree.get_children():

                self.tree.delete(item)

            for subject in subjects:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        subject.get(
                            "subject_code",
                            ""
                        ),
                        subject.get(
                            "subject_name",
                            ""
                        ),
                        subject.get(
                            "course_code",
                            ""
                        ),
                        subject.get(
                            "semester",
                            ""
                        ),
                        subject.get(
                            "credits",
                            ""
                        ),
                        subject.get(
                            "description",
                            ""
                        )
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load subjects.\n\n{e}"
            )

        finally:

            try:
                cursor.close()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # SEARCH
    # =========================================================

    def search_subjects(self):

        query_text = (
            self.search_entry
            .get()
            .strip()
        )

        if not query_text:

            self.load_subjects()

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to local MySQL."
            )

            return

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            search_pattern = f"%{query_text}%"

            query = """
                SELECT
                    subject_code,
                    subject_name,
                    course_code,
                    semester,
                    credits,
                    description
                FROM subjects
                WHERE subject_code LIKE %s
                   OR subject_name LIKE %s
                ORDER BY subject_code ASC
            """

            cursor.execute(
                query,
                (
                    search_pattern,
                    search_pattern
                )
            )

            subjects = cursor.fetchall()

            for item in self.tree.get_children():

                self.tree.delete(item)

            for subject in subjects:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        subject.get(
                            "subject_code",
                            ""
                        ),
                        subject.get(
                            "subject_name",
                            ""
                        ),
                        subject.get(
                            "course_code",
                            ""
                        ),
                        subject.get(
                            "semester",
                            ""
                        ),
                        subject.get(
                            "credits",
                            ""
                        ),
                        subject.get(
                            "description",
                            ""
                        )
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Search failed.\n\n{e}"
            )

        finally:

            try:
                cursor.close()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # SAVE / UPDATE
    # =========================================================

    def save_subject(self):

        subject_code = (
            self.subject_code_entry
            .get()
            .strip()
        )

        subject_name = (
            self.subject_name_entry
            .get()
            .strip()
        )

        course_display = (
            self.course_combo
            .get()
            .strip()
        )

        semester = (
            self.semester_combo
            .get()
            .strip()
        )

        credits = (
            self.credits_entry
            .get()
            .strip()
        )

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not subject_code:

            messagebox.showwarning(
                "Missing Information",
                "Subject Code is required."
            )

            return

        if not subject_name:

            messagebox.showwarning(
                "Missing Information",
                "Subject Name is required."
            )

            return

        if course_display not in self.course_map:

            messagebox.showwarning(
                "Select Course",
                "Please select a valid course."
            )

            return

        if not semester:

            messagebox.showwarning(
                "Missing Information",
                "Semester is required."
            )

            return

        if not credits:

            messagebox.showwarning(
                "Missing Information",
                "Credits are required."
            )

            return

        try:

            semester_value = int(semester)
            credits_value = int(credits)

        except ValueError:

            messagebox.showwarning(
                "Invalid Input",
                "Semester and Credits must be numbers."
            )

            return

        course_code = self.course_map[
            course_display
        ]

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to local MySQL."
            )

            return

        try:

            cursor = connection.cursor()

            if self.editing_subject_code:

                query = """
                    UPDATE subjects
                    SET
                        subject_name = %s,
                        course_code = %s,
                        semester = %s,
                        credits = %s,
                        description = %s
                    WHERE subject_code = %s
                """

                cursor.execute(
                    query,
                    (
                        subject_name,
                        course_code,
                        semester_value,
                        credits_value,
                        description,
                        self.editing_subject_code
                    )
                )

                message = "Subject updated successfully."

            else:

                query = """
                    INSERT INTO subjects
                    (
                        subject_code,
                        subject_name,
                        course_code,
                        semester,
                        credits,
                        description
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """

                cursor.execute(
                    query,
                    (
                        subject_code,
                        subject_name,
                        course_code,
                        semester_value,
                        credits_value,
                        description
                    )
                )

                message = "Subject added successfully."

            connection.commit()

            messagebox.showinfo(
                "Success",
                message
            )

            self.clear_form()

            self.load_subjects()

        except Exception as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to save subject.\n\n{e}"
            )

        finally:

            try:
                cursor.close()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # EDIT
    # =========================================================

    def edit_subject(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Subject",
                "Please select a subject to edit."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.editing_subject_code = values[0]

        self.subject_code_entry.configure(
            state="normal"
        )

        self.subject_code_entry.delete(
            0,
            "end"
        )

        self.subject_code_entry.insert(
            0,
            values[0]
        )

        self.subject_name_entry.delete(
            0,
            "end"
        )

        self.subject_name_entry.insert(
            0,
            values[1]
        )

        course_code = values[2]

        for display, code in self.course_map.items():

            if code == course_code:

                self.course_combo.set(
                    display
                )

                break

        self.semester_combo.set(
            str(values[3])
        )

        self.credits_entry.delete(
            0,
            "end"
        )

        self.credits_entry.insert(
            0,
            values[4]
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.description_entry.insert(
            0,
            values[5]
        )

        self.subject_code_entry.configure(
            state="disabled"
        )

        self.save_button.configure(
            text="Update Subject"
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_subject(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Subject",
                "Please select a subject to delete."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        subject_code = values[0]

        confirm = messagebox.askyesno(
            "Delete Subject",
            f"Are you sure you want to delete "
            f"subject '{subject_code}'?"
        )

        if not confirm:

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to local MySQL."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                DELETE FROM subjects
                WHERE subject_code = %s
            """

            cursor.execute(
                query,
                (subject_code,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Subject deleted successfully."
            )

            self.clear_form()

            self.load_subjects()

        except Exception as e:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete subject.\n\n{e}"
            )

        finally:

            try:
                cursor.close()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.editing_subject_code = None

        self.subject_code_entry.configure(
            state="normal"
        )

        self.subject_code_entry.delete(
            0,
            "end"
        )

        self.subject_name_entry.delete(
            0,
            "end"
        )

        self.credits_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            0,
            "end"
        )

        self.semester_combo.set("3")

        if self.course_map:

            first_course = next(
                iter(self.course_map)
            )

            self.course_combo.set(
                first_course
            )

        self.save_button.configure(
            text="Add Subject"
        )


# =============================================================
# STANDALONE TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "Subject Management - Student Management System"
    )

    root.geometry(
        "1250x800"
    )

    root.minsize(
        1100,
        700
    )

    page = SubjectsPage(root)

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()