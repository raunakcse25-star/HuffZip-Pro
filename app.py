import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import threading

from core.compressor import Compressor
from core.decompressor import Decompressor


class HuffZipApp:

    def __init__(self, root):
        self.root = root
        self.root.title("HuffZip Pro 🚀")
        self.root.geometry("500x380")
        self.root.resizable(False, False)

        self.selected_file = None

        self.setup_ui()

    # -------------------------
    # UI SETUP
    # -------------------------

    def setup_ui(self):

        title = tk.Label(
            self.root,
            text="HuffZip Pro Compression Tool",
            font=("Arial", 18, "bold"),
            fg="#333"
        )
        title.pack(pady=10)

        # File selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=5)

        tk.Button(
            file_frame,
            text="Select File",
            command=self.select_file,
            bg="#555",
            fg="white",
            width=15
        ).grid(row=0, column=0, padx=5)

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            fg="gray"
        )
        self.file_label.grid(row=0, column=1)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=350, mode="determinate")
        self.progress.pack(pady=15)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Compress",
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.start_compress_thread
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Decompress",
            width=15,
            bg="#2196F3",
            fg="white",
            command=self.start_decompress_thread
        ).grid(row=0, column=1, padx=10)

        # Result box
        self.result = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            justify="left"
        )
        self.result.pack(pady=10)

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief="sunken",
            anchor="w"
        )
        self.status.pack(side="bottom", fill="x")

    # -------------------------
    # FILE SELECTION
    # -------------------------

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file = path
            size = os.path.getsize(path)
            self.file_label.config(text=f"{os.path.basename(path)} ({size} bytes)")
            self.status.config(text="File selected")

    # -------------------------
    # THREAD WRAPPERS
    # -------------------------

    def start_compress_thread(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        threading.Thread(target=self.compress).start()

    def start_decompress_thread(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        threading.Thread(target=self.decompress).start()

    # -------------------------
    # PROGRESS SIMULATION
    # -------------------------

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    # -------------------------
    # COMPRESS
    # -------------------------

    def compress(self):
        try:
            self.status.config(text="Compressing...")

            self.update_progress(10)

            output = self.selected_file + ".hzip"

            comp = Compressor()

            self.update_progress(40)
            comp.compress_file(self.selected_file, output)

            self.update_progress(80)

            original = os.path.getsize(self.selected_file)
            compressed = os.path.getsize(output)

            saved = original - compressed
            ratio = compressed / original if original != 0 else 0
            percent = (saved / original * 100) if original != 0 else 0

            feedback = self.get_feedback(percent)

            self.update_progress(100)

            self.result.config(
                text=f"""
✅ Compression Complete

📁 Original : {original} bytes
📦 Compressed : {compressed} bytes
💾 Saved : {saved} bytes
📊 Ratio : {ratio:.2f}
🔥 Efficiency : {percent:.2f}%

👉 {feedback}
"""
            )

            self.status.config(text="Compression successful")
            messagebox.showinfo("Success", "File compressed successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error occurred")

        finally:
            self.update_progress(0)

    # -------------------------
    # DECOMPRESS
    # -------------------------

    def decompress(self):
        try:
            self.status.config(text="Decompressing...")

            self.update_progress(20)

            output = self.selected_file.replace(".hzip", "_decompressed.txt")

            decomp = Decompressor()

            self.update_progress(50)
            decomp.decompress_file(self.selected_file, output)

            self.update_progress(100)

            self.result.config(
                text=f"""
✅ Decompression Complete

📄 Output File:
{output}
"""
            )

            self.status.config(text="Decompression successful")
            messagebox.showinfo("Success", "File decompressed successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error occurred")

        finally:
            self.update_progress(0)

    # -------------------------
    # SMART FEEDBACK
    # -------------------------

    def get_feedback(self, percent):
        if percent > 60:
            return "Excellent compression 🚀"
        elif percent > 30:
            return "Good compression 👍"
        elif percent > 10:
            return "Average compression ⚖️"
        else:
            return "Low compression ⚠️ Try larger files"


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffZipApp(root)
    root.mainloop()
