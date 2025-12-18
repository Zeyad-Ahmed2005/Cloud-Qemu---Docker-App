import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from managers.qemu_manager import QemuManager
from managers.docker_manager import DockerManager


class CloudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Management System (QEMU & Docker)")
        self.root.geometry("1000x800")

        self.qemu_manager = QemuManager()
        self.docker_manager = DockerManager()

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabs
        self.create_vm_tab()
        self.create_docker_tab()

    def create_vm_tab(self):
        vm_frame = ttk.Frame(self.notebook)
        self.notebook.add(vm_frame, text="QEMU VM Management")

        # Layout
        input_frame = ttk.LabelFrame(vm_frame, text="VM Configuration")
        input_frame.pack(fill="x", padx=10, pady=10)

        # CPU
        ttk.Label(input_frame, text="CPU Cores:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.cpu_var = tk.StringVar(value="2")
        ttk.Entry(input_frame, textvariable=self.cpu_var).grid(
            row=0, column=1, padx=5, pady=5
        )

        # RAM
        ttk.Label(input_frame, text="RAM (MB):").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.ram_var = tk.StringVar(value="2048")
        ttk.Entry(input_frame, textvariable=self.ram_var).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Disk Image
        ttk.Label(input_frame, text="Disk Image:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.disk_path_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.disk_path_var, width=50).grid(
            row=2, column=1, padx=5, pady=5
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_disk).grid(
            row=2, column=2, padx=5, pady=5
        )
        ttk.Button(
            input_frame, text="Create New Disk", command=self.show_create_disk_window
        ).grid(row=2, column=3, padx=5, pady=5)

        # ISO Image
        ttk.Label(input_frame, text="ISO (Optional):").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.iso_path_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.iso_path_var, width=50).grid(
            row=3, column=1, padx=5, pady=5
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_iso).grid(
            row=3, column=2, padx=5, pady=5
        )

        # Config Loader
        ttk.Button(
            input_frame, text="Load Config (JSON)", command=self.load_config
        ).grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        # Start Button
        ttk.Button(vm_frame, text="Start VM", command=self.start_vm).pack(pady=20)

    def load_config(self):
        filename = filedialog.askopenfilename(
            title="Select System Config",
            filetypes=(("JSON", "*.json"), ("All Files", "*.*")),
        )
        if filename:
            success, data = self.qemu_manager.load_vm_config(filename)
            if success:
                self.cpu_var.set(data.get("cpu", "2"))
                self.ram_var.set(data.get("ram", "2048"))
                self.disk_path_var.set(data.get("disk_path", ""))
                self.iso_path_var.set(data.get("iso_path", ""))
                messagebox.showinfo("Success", "Configuration loaded")
            else:
                messagebox.showerror("Error", f"Failed to load config: {data}")

    def create_docker_tab(self):
        docker_frame = ttk.Frame(self.notebook)
        self.notebook.add(docker_frame, text="Docker Management")

        # Sub-tabs for Docker (Images, Containers, Dockerfile)
        docker_notebook = ttk.Notebook(docker_frame)
        docker_notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # 1. Images Tab
        self.create_docker_images_tab(docker_notebook)
        # 2. Containers Tab
        self.create_docker_containers_tab(docker_notebook)
        # 3. Dockerfile Tab
        self.create_dockerfile_tab(docker_notebook)

    def create_docker_images_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Images")

        # Tools Frame
        tools_frame = ttk.Frame(frame)
        tools_frame.pack(fill="x", padx=5, pady=5)

        # List Images
        ttk.Button(
            tools_frame, text="Refresh Images", command=self.list_docker_images
        ).pack(side="left", padx=5)

        # Search Hub
        ttk.Label(tools_frame, text="Search Hub:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(tools_frame, textvariable=self.search_var).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Search", command=self.search_hub).pack(
            side="left", padx=5
        )

        # Pull Image
        ttk.Label(tools_frame, text="Pull Image:").pack(side="left", padx=5)
        self.pull_var = tk.StringVar()
        ttk.Entry(tools_frame, textvariable=self.pull_var).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Pull", command=self.pull_docker_image).pack(
            side="left", padx=5
        )

        # Build Image
        build_frame = ttk.LabelFrame(frame, text="Build Image")
        build_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(build_frame, text="Dockerfile:").pack(side="left", padx=5)
        self.build_dockerfile_path = tk.StringVar()
        ttk.Entry(build_frame, textvariable=self.build_dockerfile_path, width=40).pack(
            side="left", padx=5
        )
        ttk.Button(
            build_frame, text="Browse", command=self.browse_build_dockerfile
        ).pack(side="left", padx=5)

        ttk.Label(build_frame, text="Tag/Name:").pack(side="left", padx=5)
        self.build_tag = tk.StringVar()
        ttk.Entry(build_frame, textvariable=self.build_tag).pack(side="left", padx=5)
        ttk.Button(build_frame, text="Build", command=self.build_image).pack(
            side="left", padx=5
        )

        # Output Area
        self.images_output = scrolledtext.ScrolledText(frame, height=20)
        self.images_output.pack(expand=True, fill="both", padx=5, pady=5)

    def create_docker_containers_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Containers")

        # Tools
        tools_frame = ttk.Frame(frame)
        tools_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            tools_frame, text="Refresh Containers", command=self.list_docker_containers
        ).pack(side="left", padx=5)

        ttk.Label(tools_frame, text="Stop Container ID:").pack(side="left", padx=5)
        self.stop_id_var = tk.StringVar()
        ttk.Entry(tools_frame, textvariable=self.stop_id_var).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Stop", command=self.stop_container).pack(
            side="left", padx=5
        )

        self.containers_output = scrolledtext.ScrolledText(frame, height=20)
        self.containers_output.pack(expand=True, fill="both", padx=5, pady=5)

    def create_dockerfile_tab(self, parent):
        frame = ttk.Frame(parent)
        parent.add(frame, text="Create Dockerfile")

        # Save tools
        tools_frame = ttk.Frame(frame)
        tools_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            tools_frame, text="Save Dockerfile", command=self.save_dockerfile
        ).pack(side="left", padx=5)

        # Editor
        self.dockerfile_editor = scrolledtext.ScrolledText(frame)
        self.dockerfile_editor.pack(expand=True, fill="both", padx=5, pady=5)
        self.dockerfile_editor.insert(
            "1.0",
            '# Write your Dockerfile content here\nFROM python:3.9\nCMD ["python", "--version"]',
        )

    # --- VM Handlers ---
    def browse_disk(self):
        filename = filedialog.askopenfilename(
            title="Select Disk Image",
            filetypes=(("QCOW2", "*.qcow2"), ("IMG", "*.img"), ("All Files", "*.*")),
        )
        if filename:
            self.disk_path_var.set(filename)

    def browse_iso(self):
        filename = filedialog.askopenfilename(
            title="Select ISO Image", filetypes=(("ISO", "*.iso"), ("All Files", "*.*"))
        )
        if filename:
            self.iso_path_var.set(filename)

    def start_vm(self):
        success, msg = self.qemu_manager.start_vm(
            self.cpu_var.get(),
            self.ram_var.get(),
            self.disk_path_var.get(),
            self.iso_path_var.get(),
        )
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def show_create_disk_window(self):
        # Implementation for disk creation dialog
        create_win = tk.Toplevel(self.root)
        create_win.title("Create Disk Image")

        ttk.Label(create_win, text="Size (GB):").grid(row=0, column=0, padx=5, pady=5)
        size_var = tk.StringVar(value="10")
        ttk.Entry(create_win, textvariable=size_var).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Button(
            create_win,
            text="Create",
            command=lambda: self.do_create_disk(create_win, size_var.get()),
        ).grid(row=1, column=0, columnspan=2, pady=10)

    def do_create_disk(self, window, size):
        path = filedialog.asksaveasfilename(
            title="Save Disk Image", defaultextension=".qcow2"
        )
        if path:
            success, msg = self.qemu_manager.create_disk_image(size, path)
            if success:
                messagebox.showinfo("Success", "Disk created successfully")
                window.destroy()
            else:
                messagebox.showerror("Error", msg)

    # --- Docker Handlers ---
    def list_docker_images(self):
        success, output = self.docker_manager.list_images()
        self.images_output.delete("1.0", tk.END)
        self.images_output.insert(tk.END, output if success else f"Error: {output}")

    def search_hub(self):
        term = self.search_var.get()
        if not term:
            return
        success, output = self.docker_manager.search_hub(term)
        self.images_output.delete("1.0", tk.END)
        self.images_output.insert(tk.END, output if success else f"Error: {output}")

    def pull_docker_image(self):
        img = self.pull_var.get()
        if not img:
            return
        # This might take a while, GUI might freeze. For MVP, we accept this risk or could use threading.
        self.images_output.insert(tk.END, f"\nPulling {img}...\n")
        self.root.update()
        success, output = self.docker_manager.pull_image(img)
        self.images_output.insert(tk.END, output if success else f"Error: {output}")

    def browse_build_dockerfile(self):
        filename = filedialog.askopenfilename(
            title="Select Dockerfile",
            filetypes=(("Dockerfile", "Dockerfile"), ("All Files", "*.*")),
        )
        if filename:
            self.build_dockerfile_path.set(filename)

    def build_image(self):
        path = self.build_dockerfile_path.get()
        tag = self.build_tag.get()
        if not path or not tag:
            messagebox.showerror("Error", "Please provide Dockerfile path and Tag")
            return

        self.images_output.insert(tk.END, f"\nBuilding {tag}...\n")
        self.root.update()
        success, output = self.docker_manager.build_image(path, tag)
        self.images_output.insert(tk.END, output if success else f"Error: {output}")

    def list_docker_containers(self):
        success, output = self.docker_manager.list_containers()
        self.containers_output.delete("1.0", tk.END)
        self.containers_output.insert(tk.END, output if success else f"Error: {output}")

    def stop_container(self):
        cid = self.stop_id_var.get()
        if not cid:
            return
        success, output = self.docker_manager.stop_container(cid)
        self.containers_output.insert(
            tk.END, f"\n{output if success else 'Error: ' + output}\n"
        )
        # Refresh list
        self.list_docker_containers()

    def save_dockerfile(self):
        content = self.dockerfile_editor.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(
            title="Save Dockerfile", initialfile="Dockerfile"
        )
        if path:
            success, msg = self.docker_manager.create_dockerfile(path, content)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = CloudApp(root)
    root.mainloop()
