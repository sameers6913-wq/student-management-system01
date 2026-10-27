
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from database import create_connection


class AnnouncementsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F5F7FA")

        self.selected_id = None
        self.announcement_cards = []

        self.create_header()
        self.create_management_section()
        self.create_notice_board()

        self.load_announcements()

    # =========================
    # HEADER
    # =========================
    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="📢 Announcements",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Important notices and announcements",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 0)
        )

    # =========================
    # MANAGEMENT SECTION
    # =========================
    def create_management_section(self):

        self.management_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
        )

        self.management_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 10)
        )

        title = ctk.CTkLabel(
            self.management_frame,
            text="Manage Announcements",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(15, 10),
            sticky="w"
        )

        # Announcement title
        ctk.CTkLabel(
            self.management_frame,
            text="Title",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.title_entry = ctk.CTkEntry(
            self.management_frame,
            width=280,
            height=38,
            placeholder_text="Announcement title"
        )

        self.title_entry.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # Target audience
        ctk.CTkLabel(
            self.management_frame,
            text="Target Audience",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=1,
            column=1,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.audience_combo = ctk.CTkComboBox(
            self.management_frame,
            width=200,
            height=38,
            values=[
                "All",
                "Students",
                "Teachers",
                "Administrators"
            ]
        )

        self.audience_combo.set("All")

        self.audience_combo.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # Date
        ctk.CTkLabel(
            self.management_frame,
            text="Date",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=1,
            column=2,
            padx=15,
            pady=(5, 5),
            sticky="w"
        )

        self.date_entry = ctk.CTkEntry(
            self.management_frame,
            width=170,
            height=38
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )

        self.date_entry.grid(
            row=2,
            column=2,
            padx=15,
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            self.management_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=3,
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Add",
            width=100,
            height=38,
            command=self.add_announcement
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="✏️ Update",
            width=100,
            height=38,
            fg_color="#F39C12",
            hover_color="#D68910",
            command=self.update_announcement
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            width=100,
            height=38,
            fg_color="#C0392B",
            hover_color="#A93226",
            command=self.delete_announcement
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            button_frame,
            text="🔄 Clear",
            width=100,
            height=38,
            fg_color="#7F8C8D",
            hover_color="#626567",
            command=self.clear_form
        ).pack(
            side="left",
            padx=3
        )

        # Message
        ctk.CTkLabel(
            self.management_frame,
            text="Message",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 5),
            sticky="nw"
        )

        self.message_box = ctk.CTkTextbox(
            self.management_frame,
            height=90
        )

        self.message_box.grid(
            row=4,
            column=0,
            columnspan=4,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        self.management_frame.grid_columnconfigure(
            3,
            weight=1
        )

    # =========================
    # NOTICE BOARD
    # =========================
    def create_notice_board(self):

        board = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="white"
        )

        board.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20)
        )

        # Board header
        board_header = ctk.CTkFrame(
            board,
            fg_color="transparent"
        )

        board_header.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        board_title = ctk.CTkLabel(
            board_header,
            text="📌 Notice Board",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        board_title.pack(
            side="left"
        )

        self.search_entry = ctk.CTkEntry(
            board_header,
            width=280,
            height=36,
            placeholder_text="Search announcements..."
        )

        self.search_entry.pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            board_header,
            text="🔍 Search",
            width=90,
            height=36,
            command=self.search_announcements
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            board_header,
            text="📋 All",
            width=70,
            height=36,
            command=self.load_announcements
        ).pack(
            side="right",
            padx=5
        )

        # Scrollable area
        self.scroll_frame = ctk.CTkScrollableFrame(
            board,
            fg_color="#F8FAFC"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =========================
    # LOAD ANNOUNCEMENTS
    # =========================
    def load_announcements(self):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.announcement_cards.clear()

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id,
                       title,
                       message,
                       target_audience,
                       announcement_date
                FROM announcements
                ORDER BY announcement_date DESC, id DESC
            """)

            records = cursor.fetchall()

            if not records:

                empty_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text="📭 No announcements available.",
                    font=ctk.CTkFont(
                        size=17,
                        weight="bold"
                    ),
                    text_color="gray"
                )

                empty_label.pack(
                    pady=100
                )

            else:

                for record in records:
                    self.create_announcement_card(record)

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # CREATE ANNOUNCEMENT CARD
    # =========================
    def create_announcement_card(self, record):

        announcement_id = record[0]
        title = record[1]
        message = record[2]
        audience = record[3]
        announcement_date = record[4]

        card = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#D9E2EC"
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        # Top section
        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        title_label = ctk.CTkLabel(
            top,
            text=f"📢  {title}",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            anchor="w"
        )

        title_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        date_label = ctk.CTkLabel(
            top,
            text=f"📅 {announcement_date}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )

        date_label.pack(
            side="right"
        )

        # Audience
        audience_label = ctk.CTkLabel(
            card,
            text=f"🎯 Audience: {audience}",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#1F4E78",
            anchor="w"
        )

        audience_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        # Full message
        message_label = ctk.CTkLabel(
            card,
            text=message,
            font=ctk.CTkFont(
                size=14
            ),
            justify="left",
            anchor="w",
            wraplength=1050
        )

        message_label.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # Select button
        select_button = ctk.CTkButton(
            card,
            text="✏️ Select / Edit",
            width=120,
            height=32,
            fg_color="#1F4E78",
            hover_color="#2E6FA3",
            command=lambda i=announcement_id:
                self.select_announcement(i)
        )

        select_button.pack(
            anchor="e",
            padx=20,
            pady=(0, 15)
        )

        self.announcement_cards.append(
            card
        )

    # =========================
    # SELECT ANNOUNCEMENT
    # =========================
    def select_announcement(self, announcement_id):

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id,
                       title,
                       message,
                       target_audience,
                       announcement_date
                FROM announcements
                WHERE id = %s
            """, (announcement_id,))

            record = cursor.fetchone()

            if record:

                self.selected_id = record[0]

                self.title_entry.delete(
                    0,
                    "end"
                )

                self.title_entry.insert(
                    0,
                    record[1]
                )

                self.message_box.delete(
                    "1.0",
                    "end"
                )

                self.message_box.insert(
                    "1.0",
                    record[2]
                )

                self.audience_combo.set(
                    record[3]
                )

                self.date_entry.delete(
                    0,
                    "end"
                )

                self.date_entry.insert(
                    0,
                    str(record[4])
                )

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # ADD
    # =========================
    def add_announcement(self):

        title = self.title_entry.get().strip()

        message = self.message_box.get(
            "1.0",
            "end"
        ).strip()

        audience = self.audience_combo.get().strip()

        announcement_date = self.date_entry.get().strip()

        if not title:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement title."
            )
            return

        if not message:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement message."
            )
            return

        if not announcement_date:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement date."
            )
            return

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO announcements
                (
                    title,
                    message,
                    target_audience,
                    announcement_date
                )
                VALUES (%s, %s, %s, %s)
            """, (
                title,
                message,
                audience,
                announcement_date
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Announcement added successfully."
            )

            self.clear_form()
            self.load_announcements()

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # UPDATE
    # =========================
    def update_announcement(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an announcement first."
            )

            return

        title = self.title_entry.get().strip()

        message = self.message_box.get(
            "1.0",
            "end"
        ).strip()

        audience = self.audience_combo.get().strip()

        announcement_date = self.date_entry.get().strip()

        if not title or not message:

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields."
            )

            return

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE announcements
                SET title = %s,
                    message = %s,
                    target_audience = %s,
                    announcement_date = %s
                WHERE id = %s
            """, (
                title,
                message,
                audience,
                announcement_date,
                self.selected_id
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Announcement updated successfully."
            )

            self.clear_form()
            self.load_announcements()

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # DELETE
    # =========================
    def delete_announcement(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select an announcement first."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this announcement?"
        )

        if not answer:
            return

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM announcements
                WHERE id = %s
            """, (self.selected_id,))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Announcement deleted successfully."
            )

            self.clear_form()
            self.load_announcements()

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # SEARCH
    # =========================
    def search_announcements(self):

        search_text = self.search_entry.get().strip()

        if not search_text:

            self.load_announcements()
            return

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        conn = create_connection()

        if conn is None:
            return

        try:

            cursor = conn.cursor()

            value = f"%{search_text}%"

            cursor.execute("""
                SELECT id,
                       title,
                       message,
                       target_audience,
                       announcement_date
                FROM announcements
                WHERE title LIKE %s
                   OR message LIKE %s
                   OR target_audience LIKE %s
                ORDER BY announcement_date DESC, id DESC
            """, (
                value,
                value,
                value
            ))

            records = cursor.fetchall()

            if not records:

                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text="🔍 No matching announcements found.",
                    font=ctk.CTkFont(
                        size=16,
                        weight="bold"
                    ),
                    text_color="gray"
                )

                label.pack(
                    pady=100
                )

            else:

                for record in records:
                    self.create_announcement_card(record)

            cursor.close()

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                str(e)
            )

        finally:

            conn.close()

    # =========================
    # CLEAR
    # =========================
    def clear_form(self):

        self.selected_id = None

        self.title_entry.delete(
            0,
            "end"
        )

        self.message_box.delete(
            "1.0",
            "end"
        )

        self.audience_combo.set(
            "All"
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )


# =========================
# DIRECT TEST
# =========================
if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title(
        "Announcements Management"
    )

    app.geometry(
        "1450x850"
    )

    page = AnnouncementsPage(app)

    page.pack(
        fill="both",
        expand=True
    )

    app.mainloop()

