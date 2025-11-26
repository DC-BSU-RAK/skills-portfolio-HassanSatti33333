import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(
    script_dir,
    "..",
    "Assessment 1 - Skills Portfolio",
    "A1 - Resources",
    "studentMarks.txt",
) #I asked ChatGPT to help me make the path work on my computer because for some reason it wasnt working 

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager System")

        self.dark_mode = False
        self.students = []
        self.sidebar_buttons = []

        self.center_window(1100, 650)
        self.root.configure(bg="#ecf0f1")

        self.create_layout()
        self.load_data()
        self.view_all_students()
        self.auto_save()

    def center_window(self, width, height):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def calculate_results(self, cw1, cw2, cw3, exam):
        total = cw1 + cw2 + cw3 + exam
        percent = (total / 160) * 100
        if percent >= 70:
            grade = "A"
        elif percent >= 60:
            grade = "B"
        elif percent >= 50:
            grade = "C"
        elif percent >= 40:
            grade = "D"
        else:
            grade = "F"
        return total, round(percent, 1), grade

    def load_data(self):
        self.students = []
        try:
            if not os.path.exists(FILE_NAME):
                messagebox.showerror("Error", f"File not found:\n{FILE_NAME}")
                return
            with open(FILE_NAME, "r") as f:
                lines = f.readlines()
            for line in lines[1:]:
                if not line.strip():
                    continue
                p = line.strip().split(",")
                if len(p) < 6:
                    continue
                code, name = p[0].strip(), p[1].strip()
                cw1, cw2, cw3, exam = map(int, p[2:6])
                total, percent, grade = self.calculate_results(cw1, cw2, cw3, exam)
                self.students.append(
                    {
                        "code": code,
                        "name": name,
                        "cw1": cw1,
                        "cw2": cw2,
                        "cw3": cw3,
                        "exam": exam,
                        "total": total,
                        "percent": percent,
                        "grade": grade,
                    }
                )
        except Exception as e:
            messagebox.showerror("Error", f"Load failed: {e}")

    def save_data(self):
        try:
            with open(FILE_NAME, "w") as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(
                        f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n"
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")

    def create_sidebar_button(self, parent, text, command, btn_style):
        btn = tk.Button(parent, text=text, command=command, **btn_style)
        btn.pack(pady=2)
        def on_enter(e):
            e.widget["bg"] = "#1abc9c"
        def on_leave(e):
            e.widget["bg"] = btn_style["bg"]
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        self.sidebar_buttons.append(btn)
        return btn

    def create_layout(self):
        self.control_frame = tk.Frame(self.root, bg="#2c3e50", width=250)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            self.control_frame,
            text="Student\nManager",
            bg="#2c3e50",
            fg="white",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=30)

        btn_style = {
            "bg": "#34495e",
            "fg": "white",
            "font": ("Segoe UI", 11),
            "bd": 0,
            "activebackground": "#1abc9c",
            "activeforeground": "white",
            "height": 2,
            "width": 25,
            "cursor": "hand2",
        }

        self.create_sidebar_button(self.control_frame, "1. View All Records", self.view_all_students, btn_style)
        self.create_sidebar_button(self.control_frame, "2. View Individual", self.find_student, btn_style)
        self.create_sidebar_button(self.control_frame, "3. Highest Score", self.show_highest, btn_style)
        self.create_sidebar_button(self.control_frame, "4. Lowest Score", self.show_lowest, btn_style)

        tk.Frame(self.control_frame, height=2, bg="#7f8c8d").pack(fill=tk.X, padx=20, pady=10)

        self.create_sidebar_button(self.control_frame, "5. Sort Records", self.sort_menu, btn_style)
        self.create_sidebar_button(self.control_frame, "6. Add Record", self.add_student_dialog, btn_style)
        self.create_sidebar_button(self.control_frame, "7. Delete Record", self.delete_student, btn_style)
        self.create_sidebar_button(self.control_frame, "8. Update Record", self.update_student_dialog, btn_style)
        self.create_sidebar_button(self.control_frame, "Toggle Dark Mode", self.toggle_theme, btn_style)

        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.header_label = tk.Label(
            self.content_frame,
            text="All Student Records",
            font=("Segoe UI", 18, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
        )
        self.header_label.pack(anchor="w", pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        self.search_frame.pack(anchor="e", pady=(0, 10), fill=tk.X)

        self.search_label = tk.Label(
            self.search_frame, text="Search (Name or ID):", font=("Segoe UI", 10), bg="#ecf0f1", fg="#2c3e50"
        )
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, font=("Segoe UI", 10), width=30)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self.live_search)

        cols = ("Code", "Name", "CW1", "CW2", "CW3", "Exam", "Total", "Percent", "Grade")
        self.tree = ttk.Treeview(self.content_frame, columns=cols, show="headings", selectmode="browse")

        headings = {
            "Code": "ID",
            "Name": "Student Name",
            "CW1": "CW1 (20)",
            "CW2": "CW2 (20)",
            "CW3": "CW3 (20)",
            "Exam": "Exam (100)",
            "Total": "Total (160)",
            "Percent": "Percentage",
            "Grade": "Grade",
        }

        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150 if col == "Name" else 70, anchor=tk.CENTER)

        self.tree.tag_configure("high", background="#d4efdf")
        self.tree.tag_configure("low", background="#f5b7b1")

        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

        self.footer_frame = tk.Frame(self.content_frame, bg="#bdc3c7")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.summary_label = tk.Label(
            self.footer_frame,
            text="Total Students: 0 | Average: 0%",
            font=("Segoe UI", 11, "bold"),
            bg="#bdc3c7",
            fg="#2c3e50",
        )
        self.summary_label.pack(pady=10)

    def apply_popup_theme(self, window):
        bg = "#1a1f24" if self.dark_mode else "#ecf0f1"
        fg = "#e6e6e6" if self.dark_mode else "#2c3e50"
        entry_bg = "#0f151a" if self.dark_mode else "white"
        entry_fg = "#e6e6e6" if self.dark_mode else "black"

        window.configure(bg=bg)
        for w in window.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=bg, fg=fg)
            elif isinstance(w, tk.Entry):
                w.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            elif isinstance(w, tk.Button):
                w.configure(bg="#161b22" if self.dark_mode else "#34495e", fg="white")

    def populate_tree(self, data_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for s in data_list:
            tag = "high" if s["percent"] >= 70 else "low" if s["percent"] < 40 else ""
            self.tree.insert(
                "",
                tk.END,
                values=(
                    s["code"],
                    s["name"],
                    s["cw1"],
                    s["cw2"],
                    s["cw3"],
                    s["exam"],
                    s["total"],
                    str(s["percent"]) + "%",
                    s["grade"],
                ),
                tags=tag,
            )
        count = len(data_list)
        if count:
            avg = sum(s["percent"] for s in data_list) / count
            self.summary_label.configure(text=f"Total Students: {count} | Class Average Percentage: {avg:.2f}%")
        else:
            self.summary_label.configure(text="No records found.")

    def live_search(self, event=None):
        q = self.search_var.get().lower()
        if not q:
            self.populate_tree(self.students)
            return
        results = [
            s for s in self.students if q in s["name"].lower() or q in str(s["code"]).lower()
        ]
        self.populate_tree(results)

    def view_all_students(self):
        self.header_label.configure(text="All Student Records")
        self.populate_tree(self.students)

    def find_student(self):
        q = simpledialog.askstring("Find", "Enter Student Name or ID:")
        if not q:
            return
        q = q.lower()
        results = [s for s in self.students if q in s["name"].lower() or q in s["code"]]
        if results:
            self.populate_tree(results)
        else:
            messagebox.showinfo("Not Found", "No student found.")

    def show_highest(self):
        if self.students:
            self.populate_tree([max(self.students, key=lambda x: x["total"])])

    def show_lowest(self):
        if self.students:
            self.populate_tree([min(self.students, key=lambda x: x["total"])])

    def sort_menu(self):
        win = tk.Toplevel(self.root)
        win.title("Sort Records")
        win.geometry("500x600")
        self.apply_popup_theme(win)

        tk.Label(win, text="Sort By:", font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))
        key_var = tk.StringVar(value="total")
        opts = [
            ("Student ID", "code"),
            ("Student Name", "name"),
            ("CW1", "cw1"),
            ("CW2", "cw2"),
            ("CW3", "cw3"),
            ("Exam", "exam"),
            ("Total", "total"),
            ("Percent", "percent"),
        ]
        for text, v in opts:
            tk.Radiobutton(win, text=text, variable=key_var, value=v).pack(anchor=tk.W, padx=50)

        tk.Label(win, text="Order:", font=("Segoe UI", 12, "bold")).pack(pady=10)
        order_var = tk.StringVar(value="desc")
        tk.Radiobutton(win, text="Ascending", variable=order_var, value="asc").pack(anchor=tk.W, padx=50)
        tk.Radiobutton(win, text="Descending", variable=order_var, value="desc").pack(anchor=tk.W, padx=50)

        def apply_sort():
            key = key_var.get()
            reverse = order_var.get() == "desc"
            sorted_list = sorted(
                self.students,
                key=lambda x: x[key] if not isinstance(x[key], str) else x[key].lower(),
                reverse=reverse,
            )
            self.populate_tree(sorted_list)
            win.destroy()

        tk.Button(win, text="Apply Sort", command=apply_sort, height=2, width=15).pack(pady=20)

    def add_student_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("Add Record")
        win.geometry("300x400")
        self.apply_popup_theme(win)

        fields = [
            "Code (1000-9999)",
            "Name",
            "CW1 (0-20)",
            "CW2 (0-20)",
            "CW3 (0-20)",
            "Exam (0-100)",
        ]
        entries = {}

        for f in fields:
            tk.Label(win, text=f).pack()
            e = tk.Entry(win)
            e.pack()
            entries[f] = e

        def save_new():
            try:
                code = entries["Code (1000-9999)"].get()
                name = entries["Name"].get()
                cw1 = int(entries["CW1 (0-20)"].get())
                cw2 = int(entries["CW2 (0-20)"].get())
                cw3 = int(entries["CW3 (0-20)"].get())
                exam = int(entries["Exam (0-100)"].get())

                if not (1000 <= int(code) <= 9999):
                    raise ValueError("Invalid code.")
                if not all(0 <= m <= 20 for m in [cw1, cw2, cw3]):
                    raise ValueError("CW must be 0–20.")
                if not (0 <= exam <= 100):
                    raise ValueError("Exam must be 0–100.")

                total, percent, grade = self.calculate_results(cw1, cw2, cw3, exam)
                self.students.append(
                    {
                        "code": code,
                        "name": name,
                        "cw1": cw1,
                        "cw2": cw2,
                        "cw3": cw3,
                        "exam": exam,
                        "total": total,
                        "percent": percent,
                        "grade": grade,
                    }
                )

                self.save_data()
                self.view_all_students()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Save Record", command=save_new).pack(pady=15)

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Error", "Select a student.")
            return
        item = self.tree.item(sel)
        code = item["values"][0]
        if messagebox.askyesno("Confirm", "Delete this student?"):
            self.students = [s for s in self.students if s["code"] != code]
            self.save_data()
            self.view_all_students()

    def update_student_dialog(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Error", "Select a student to update.")
            return

        item = self.tree.item(sel)
        code = item["values"][0]
        s = next((x for x in self.students if x["code"] == code), None)

        win = tk.Toplevel(self.root)
        win.title("Update Record")
        win.geometry("300x400")
        self.apply_popup_theme(win)

        entries = {}
        for label, v in {
            "Code": s["code"],
            "Name": s["name"],
            "CW1": s["cw1"],
            "CW2": s["cw2"],
            "CW3": s["cw3"],
            "Exam": s["exam"],
        }.items():
            tk.Label(win, text=label).pack()
            e = tk.Entry(win)
            e.insert(0, v)
            e.pack()
            entries[label] = e

        def update_record():
            try:
                new_code = entries["Code"].get()
                new_name = entries["Name"].get()
                cw1 = int(entries["CW1"].get())
                cw2 = int(entries["CW2"].get())
                cw3 = int(entries["CW3"].get())
                exam = int(entries["Exam"].get())

                total, percent, grade = self.calculate_results(cw1, cw2, cw3, exam)

                s.update(
                    {
                        "code": new_code,
                        "name": new_name,
                        "cw1": cw1,
                        "cw2": cw2,
                        "cw3": cw3,
                        "exam": exam,
                        "total": total,
                        "percent": percent,
                        "grade": grade,
                    }
                )

                self.save_data()
                self.view_all_students()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Update Record", command=update_record).pack(pady=15)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            root_bg = "#121212"
            sidebar_bg = "#0d1117"
            btn_bg = "#161b22"
            content_bg = "#1a1f24"
            text_main = "#e6e6e6"
            footer_bg = "#0d1117"
            entry_bg = "#0f151a"
            entry_fg = "#e6e6e6"
            tree_bg = "#0f151a"
            tree_fg = "#e6e6e6"
            tree_head_bg = "#161b22"
            tree_head_fg = "#e6e6e6"
        else:
            root_bg = "#ecf0f1"
            sidebar_bg = "#2c3e50"
            btn_bg = "#34495e"
            content_bg = "#ecf0f1"
            text_main = "#2c3e50"
            footer_bg = "#bdc3c7"
            entry_bg = "white"
            entry_fg = "black"
            tree_bg = "white"
            tree_fg = "black"
            tree_head_bg = "#d0d0d0"
            tree_head_fg = "black"

        self.root.configure(bg=root_bg)
        self.control_frame.configure(bg=sidebar_bg)
        for child in self.control_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=sidebar_bg, fg=text_main)
            elif isinstance(child, tk.Button):
                child.configure(bg=btn_bg, fg="white")

        self.content_frame.configure(bg=content_bg)
        self.header_label.configure(bg=content_bg, fg=text_main)
        self.search_frame.configure(bg=content_bg)
        self.search_label.configure(bg=content_bg, fg=text_main)
        self.search_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)

        self.footer_frame.configure(bg=footer_bg)
        self.summary_label.configure(bg=footer_bg, fg=text_main)

        style = ttk.Style()
        style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
        style.configure("Treeview.Heading", background=tree_head_bg, foreground=tree_head_fg)

        self.tree.tag_configure(
            "high",
            background="#1a3d2d" if self.dark_mode else "#d4efdf",
            foreground="white" if self.dark_mode else "black",
        )
        self.tree.tag_configure(
            "low",
            background="#3d1f1f" if self.dark_mode else "#f5b7b1",
            foreground="white" if self.dark_mode else "black",
        )

    def auto_save(self):
        self.save_data()
        self.root.after(10000, self.auto_save)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
