import customtkinter as ctk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import urllib.parse
import json


API_BASE = (
    "https://sameer-student-api-2026-ezbsexeqhyh5dbhe."
    "eastasia-01.azurewebsites.net/api"
)


def api_request(endpoint, method="GET", data=None):

    url = API_BASE + endpoint

    try:
        body = None

        if data is not None:
            body = json.dumps(data).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=body,
            method=method
        )

        request.add_header(
            "Content-Type",
            "application/json"
        )

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as e:

        try:
            return json.loads(
                e.read().decode("utf-8")
            )
        except Exception:

            return {
                "status": "error",
                "message": f"HTTP Error {e.code}"
            }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class EnrollmentsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#F5F7FA"
        )

        self.editing_id = None

        self.student_map = {}
        self.course_map = {}

        self.create_widgets()

        self.load_students()
        self.load_courses()
        self.load_enrollments()

    # =========================================================
    # UI
    # =========================================================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Enrollment Management",
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
            text="Manage student course enrollments",
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

        form = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        form.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        form.grid_columnconfigure(
            1,
            weight=1
        )

        form.grid_columnconfigure(
            3,
            weight=1
        )

        # Student

        ctk.CTkLabel(
            form,
            text="Student",
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

        self.student_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."]
        )

        self.student_combo.grid(
            row=0,
            column=1,
            padx=10,
            pady=(20, 8),
            sticky="ew"
        )

        # Course

        ctk.CTkLabel(
            form,
            text="Course",
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

        self.course_combo = ctk.CTkComboBox(
            form,
            values=["Loading..."]
        )

        self.course_combo.grid(
            row=0,
            column=3,
            padx=(10, 20),
            pady=(20, 8),
            sticky="ew"
        )

        # Enrollment Date

        ctk.CTkLabel(
            form,
            text="Enrollment Date",
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

        self.date_entry = ctk.CTkEntry(
            form,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="ew"
        )

        # Semester

        ctk.CTkLabel(
            form,
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
            form,
            values=[
                "1", "2", "3", "4",
                "5", "6", "7", "8"
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

        # Status

        ctk.CTkLabel(
            form,
            text="Status",
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

        self.status_combo = ctk.CTkComboBox(
            form,
            values=[
                "Active",
                "Completed",
                "Dropped"
            ]
        )

        self.status_combo.set("Active")

        self.status_combo.grid(
            row=2,
            column=1,
            padx=10,
            pady=8,
            sticky="ew"
        )

        # Buttons

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=20,
            pady=8,
            sticky="e"
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Enrollment",
            width=140,
            height=38,
            fg_color="#1769AA",
            hover_color="#12588E",
            command=self.save_enrollment
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
            placeholder_text="Search student ID or course...",
            width=350,
            height=38
        )

        self.search_entry.pack(
            side="left"
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            height=38,
            command=self.search_enrollments
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
            command=self.load_enrollments
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
            "id",
            "student_id",
            "course_code",
            "enrollment_date",
            "semester",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "student_id": "Student ID",
            "course_code": "Course",
            "enrollment_date": "Enrollment Date",
            "semester": "Semester",
            "status": "Status"
        }

        widths = {
            "id": 70,
            "student_id": 180,
            "course_code": 150,
            "enrollment_date": 170,
            "semester": 100,
            "status": 130
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
        # ACTIONS
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
            command=self.edit_enrollment
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
            command=self.delete_enrollment
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
            command=self.load_enrollments
        ).pack(
            side="right"
        )

    # =========================================================
    # LOAD STUDENTS
    # =========================================================

    def load_students(self):

        result = api_request("/students")

        if result.get("status") != "success":

            self.student_combo.configure(
                values=["Unable to load students"]
            )

            return

        self.student_map = {}

        values = []

        for student in result.get(
            "students",
            []
        ):

            student_id = student.get(
                "student_id",
                ""
            )

            name = student.get(
                "full_name",
                ""
            )

            display = f"{student_id} - {name}"

            self.student_map[display] = student_id

            values.append(display)

        if values:

            self.student_combo.configure(
                values=values
            )

            self.student_combo.set(
                values[0]
            )

        else:

            self.student_combo.configure(
                values=["No students"]
            )

    # =========================================================
    # LOAD COURSES
    # =========================================================

    def load_courses(self):

        result = api_request("/courses")

        if result.get("status") != "success":

            self.course_combo.configure(
                values=["Unable to load courses"]
            )

            return

        self.course_map = {}

        values = []

        for course in result.get(
            "courses",
            []
        ):

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

            values.append(display)

        if values:

            self.course_combo.configure(
                values=values
            )

            self.course_combo.set(
                values[0]
            )

        else:

            self.course_combo.configure(
                values=["No courses"]
            )

    # =========================================================
    # LOAD ENROLLMENTS
    # =========================================================

    def load_enrollments(self):

        result = api_request("/enrollments")

        if result.get("status") != "success":

            messagebox.showerror(
                "Error",
                result.get(
                    "message",
                    "Unable to load enrollments."
                )
            )

            return

        self.display_enrollments(
            result.get(
                "enrollments",
                []
            )
        )

    # =========================================================
    # DISPLAY
    # =========================================================

    def display_enrollments(
        self,
        enrollments
    ):

        for item in self.tree.get_children():

            self.tree.delete(item)

        for enrollment in enrollments:

            self.tree.insert(
                "",
                "end",
                values=(
                    enrollment.get("id", ""),
                    enrollment.get(
                        "student_id",
                        ""
                    ),
                    enrollment.get(
                        "course_code",
                        ""
                    ),
                    enrollment.get(
                        "enrollment_date",
                        ""
                    ),
                    enrollment.get(
                        "semester",
                        ""
                    ),
                    enrollment.get(
                        "status",
                        ""
                    )
                )
            )

    # =========================================================
    # SEARCH
    # =========================================================

    def search_enrollments(self):

        query = self.search_entry.get().strip()

        if not query:

            self.load_enrollments()

            return

        result = api_request(
            "/enrollments"
        )

        if result.get("status") != "success":

            messagebox.showerror(
                "Error",
                result.get(
                    "message",
                    "Search failed."
                )
            )

            return

        query = query.lower()

        filtered = []

        for enrollment in result.get(
            "enrollments",
            []
        ):

            student_id = str(
                enrollment.get(
                    "student_id",
                    ""
                )
            )

            course_code = str(
                enrollment.get(
                    "course_code",
                    ""
                )
            )

            if (
                query in student_id.lower()
                or query in course_code.lower()
            ):

                filtered.append(
                    enrollment
                )

        self.display_enrollments(
            filtered
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save_enrollment(self):

        student_display = (
            self.student_combo
            .get()
            .strip()
        )

        course_display = (
            self.course_combo
            .get()
            .strip()
        )

        enrollment_date = (
            self.date_entry
            .get()
            .strip()
        )

        semester = (
            self.semester_combo
            .get()
            .strip()
        )

        status = (
            self.status_combo
            .get()
            .strip()
        )

        if student_display not in self.student_map:

            messagebox.showwarning(
                "Select Student",
                "Please select a valid student."
            )

            return

        if course_display not in self.course_map:

            messagebox.showwarning(
                "Select Course",
                "Please select a valid course."
            )

            return

        if not enrollment_date:

            messagebox.showwarning(
                "Missing Information",
                "Enrollment date is required."
            )

            return

        if not semester:

            messagebox.showwarning(
                "Missing Information",
                "Semester is required."
            )

            return

        data = {
            "student_id": self.student_map[
                student_display
            ],
            "course_code": self.course_map[
                course_display
            ],
            "enrollment_date": enrollment_date,
            "semester": int(semester),
            "status": status
        }

        if self.editing_id:

            result = api_request(
                f"/enrollments/{self.editing_id}",
                method="PUT",
                data=data
            )

        else:

            result = api_request(
                "/enrollments",
                method="POST",
                data=data
            )

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                result.get(
                    "message",
                    "Enrollment saved successfully."
                )
            )

            self.clear_form()
            self.load_enrollments()

        else:

            messagebox.showerror(
                "Error",
                result.get(
                    "message",
                    "Unable to save enrollment."
                )
            )

    # =========================================================
    # EDIT
    # =========================================================

    def edit_enrollment(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Enrollment",
                "Please select an enrollment."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.editing_id = values[0]

        student_id = values[1]

        for display, code in self.student_map.items():

            if code == student_id:

                self.student_combo.set(
                    display
                )

                break

        course_code = values[2]

        for display, code in self.course_map.items():

            if code == course_code:

                self.course_combo.set(
                    display
                )

                break

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            values[3]
        )

        self.semester_combo.set(
            str(values[4])
        )

        self.status_combo.set(
            values[5]
        )

        self.save_button.configure(
            text="Update Enrollment"
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_enrollment(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Enrollment",
                "Please select an enrollment."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        enrollment_id = values[0]

        confirm = messagebox.askyesno(
            "Delete Enrollment",
            "Are you sure you want to delete "
            "this enrollment?"
        )

        if not confirm:

            return

        result = api_request(
            f"/enrollments/{enrollment_id}",
            method="DELETE"
        )

        if result.get("status") == "success":

            messagebox.showinfo(
                "Success",
                result.get(
                    "message",
                    "Enrollment deleted successfully."
                )
            )

            self.load_enrollments()

        else:

            messagebox.showerror(
                "Error",
                result.get(
                    "message",
                    "Unable to delete enrollment."
                )
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self):

        self.editing_id = None

        self.date_entry.delete(
            0,
            "end"
        )

        self.semester_combo.set(
            "3"
        )

        self.status_combo.set(
            "Active"
        )

        if self.student_map:

            self.student_combo.set(
                next(
                    iter(
                        self.student_map
                    )
                )
            )

        if self.course_map:

            self.course_combo.set(
                next(
                    iter(
                        self.course_map
                    )
                )
            )
        self.save_button.configure(
            text="Add Enrollment"
        )


# =============================================================
# STANDALONE TEST
# =============================================================

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    root.title(
        "Enrollment Management - Student Management System"
    )

    root.geometry(
        "1250x800"
    )

    root.minsize(
        1100,
        700
    )

    page = EnrollmentsPage(root)

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()