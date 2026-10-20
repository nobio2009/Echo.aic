import platform, shutil

def register(assistant):
    def status(_=""):
        lines=[f"Operating system: {platform.system()} {platform.release()}", f"Python: {platform.python_version()}"]
        try:
            import psutil
            lines += [f"CPU usage: {psutil.cpu_percent(interval=0.2)}%", f"RAM usage: {psutil.virtual_memory().percent}%"]
        except ImportError: lines.append("Install psutil for CPU/RAM statistics.")
        disk=shutil.disk_usage("/")
        lines.append(f"Disk free: {disk.free // (1024**3)} GiB")
        return "\n".join(lines)
    assistant.command("status", "Show basic computer and resource status.", status)
