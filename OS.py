import os
import shutil
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("700x500")
        self.base_dir = os.getcwd()
        self.current_dir = self.base_dir

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=6, font=("Helvetica", 10))
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, 'bold'))

        self.create_widgets()
        self.update_file_list()

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_label = tk.Label(top_frame, text=self.current_dir, font=("Helvetica", 10), anchor="w")
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.file_tree = ttk.Treeview(self.root, columns=("Name", "Type"), show='headings')
        self.file_tree.heading("Name", text="Name")
        self.file_tree.heading("Type", text="Type")
        self.file_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.file_tree.bind('<Double-1>', self.on_item_double_click)

        toolbar = tk.Frame(self.root, bg="#d9d9d9")
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="Create File", command=self.create_file).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="Create Folder", command=self.create_folder).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="Move", command=self.move_item).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="Copy", command=self.copy_item).pack(side=tk.LEFT, padx=3)

    def update_file_list(self):
        self.file_tree.delete(*self.file_tree.get_children())
        self.path_label.config(text=self.current_dir)

        for item in os.listdir(self.current_dir):
            item_path = os.path.join(self.current_dir, item)
            item_type = "Folder" if os.path.isdir(item_path) else "File"
            self.file_tree.insert("", tk.END, values=(item, item_type))

    def on_item_double_click(self, event):
        selected_item = self.file_tree.selection()
        if selected_item:
            item_name = self.file_tree.item(selected_item)["values"][0]
            selected_path = os.path.join(self.current_dir, item_name)
            if os.path.isdir(selected_path):
                self.current_dir = selected_path
                self.update_file_list()

    def create_file(self):
        file_name = simpledialog.askstring("Create File", "Enter file name:")
        if file_name:
            open(os.path.join(self.current_dir, file_name), 'w').close()
            self.update_file_list()

    def create_folder(self):
        folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            os.makedirs(os.path.join(self.current_dir, folder_name), exist_ok=True)
            self.update_file_list()

    def delete_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            item_name = self.file_tree.item(selected_item)["values"][0]
            selected_path = os.path.join(self.current_dir, item_name)
            if os.path.isfile(selected_path):
                os.remove(selected_path)
            elif os.path.isdir(selected_path):
                shutil.rmtree(selected_path)
            self.update_file_list()

    def select_destination_folder(self):
        
        dest_window = tk.Toplevel(self.root)
        dest_window.title("Select Destination Folder")
        dest_window.geometry("400x300")
        
        dest_tree = ttk.Treeview(dest_window, columns=("Name"), show='tree')
        dest_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        def populate_tree(parent, path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = dest_tree.insert(parent, 'end', text=item, values=(item_path,))
                    populate_tree(node, item_path)

        populate_tree('', self.base_dir)

        selected_dest = {"path": None}

        def confirm_selection():
            selected_item = dest_tree.selection()
            if selected_item:
                selected_dest["path"] = dest_tree.item(selected_item)["values"][0]
                dest_window.destroy()

        ttk.Button(dest_window, text="Select", command=confirm_selection).pack(pady=5)

        dest_window.transient(self.root)
        dest_window.grab_set()
        self.root.wait_window(dest_window)

        return selected_dest["path"]

    def move_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            item_name = self.file_tree.item(selected_item)["values"][0]
            src_path = os.path.join(self.current_dir, item_name)
            dst_path = self.select_destination_folder()
            if dst_path:
                shutil.move(src_path, dst_path)
                self.update_file_list()

    def copy_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            item_name = self.file_tree.item(selected_item)["values"][0]
            src_path = os.path.join(self.current_dir, item_name)
            dst_path = self.select_destination_folder()
            if dst_path:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, os.path.join(dst_path, os.path.basename(src_path)))
                else:
                    shutil.copy2(src_path, dst_path)
                self.update_file_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerGUI(root)
    root.mainloop()
