import os
import json
import importlib.util

class ModuleManager:
    def __init__(self, modules_path="./modules"):
        self.modules_path = modules_path
        self.registry = {}
        self.load_modules()

    def load_modules(self):
        for folder in os.listdir(self.modules_path):
            folder_path = os.path.join(self.modules_path, folder)
            if os.path.isdir(folder_path):
                config_path = os.path.join(folder_path, "config.json")
                module_path = os.path.join(folder_path, "module.py")
                try:
                    with open(config_path) as f:
                        config = json.load(f)
                    
                    spec = importlib.util.spec_from_file_location(folder, module_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    info = mod.register()
                    self.registry[info["module_id"]] = {
                        "module": mod,
                        "capabilities": info["capabilities"],
                        "config": config
                    }
                    print(f"Loaded module: {info['module_id']}")
                except Exception as e:
                    print(f"Failed to load {folder}: {e}")

    def execute_module(self, module_id, action, **kwargs):
        module_info = self.registry.get(module_id)
        if not module_info:
            print(f"Module {module_id} not found")
            return
        if action not in module_info["capabilities"]:
            print(f"Action {action} not supported by {module_id}")
            return
        try:
            module_info["module"].execute(action, **kwargs)
        except Exception as e:
            print(f"Error executing {module_id}: {e}")
