import os
from utils.cmd_runner import run_command


class QemuManager:
    def __init__(self):
        pass

    def start_vm(self, cpu_cores, ram_mb, disk_path, iso_path=None):
        """
        Constructs and runs the QEMU command.
        """
        # Basic qemu command structure
        # qemu-system-x86_64 -m 1024 -smp 2 -hda disk.img -cdrom install.iso

        cmd_parts = ["qemu-system-x86_64"]

        # RAM
        if ram_mb:
            cmd_parts.append(f"-m {ram_mb}")

        # CPU
        if cpu_cores:
            cmd_parts.append(f"-smp {cpu_cores}")

        # Disk
        if disk_path and os.path.exists(disk_path):
            cmd_parts.append(f'-hda "{disk_path}"')
        else:
            return False, "Disk path does not exist or is invalid."

        # ISO (Optional)
        if iso_path:
            if os.path.exists(iso_path):
                cmd_parts.append(f'-cdrom "{iso_path}"')
            else:
                # We can warn here, but maybe proceed without ISO or fail
                return False, "ISO path provided but does not exist."

        # Enable acceleration if on compatible platform (optional, but good for performance)
        # cmd_parts.append("-enable-kvm") # Linux specific usually, might cause issues on generic Windows without HAXM/WHPX
        # For Windows, we might use -accel whpx if available, but let's stick to basic for compatibility first.

        full_command = " ".join(cmd_parts)

        # Since QEMU opens a GUI window, we might want to run it without blocking or capture output differently.
        # run_command waits for completion. For launching a VM, we probably don't want to block the GUI.
        # We should use subprocess.Popen directly for non-blocking UI launch if needed,
        # but let's use our runner for now and see if we can detach it.
        # Actually, if we use shell=True and don't wait, it might be better?
        # Let's try to run it. If it blocks, the UI freezes.
        # For this MVP, we will try to launch it.

        import subprocess

        try:
            subprocess.Popen(full_command, shell=True)
            return True, f"VM Launching: {full_command}"
        except Exception as e:
            return False, str(e)

    def create_disk_image(self, size_gb, location):
        """
        Creates a new qcov2 or raw disk image using qemu-img.
        qemu-img create -f qcow2 path.qcow2 10G
        """
        if not location.endswith(".qcow2") and not location.endswith(".img"):
            location += ".qcow2"

        command = f'qemu-img create -f qcow2 "{location}" {size_gb}G'
        return run_command(command)

    def load_vm_config(self, config_path):
        """
        Loads VM configuration from a JSON file.
        Expected format:
        {
            "cpu": "2",
            "ram": "2048",
            "disk_path": "path/to/disk.img",
            "iso_path": "path/to/install.iso"
        }
        """
        import json

        try:
            with open(config_path, "r") as f:
                return True, json.load(f)
        except Exception as e:
            return False, str(e)
