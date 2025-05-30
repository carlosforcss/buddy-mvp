class Logger:
    def __init__(self, name: str):
        self.name = name

    def info(self, message: str):
        print(f"[INFO] {self.name}: {message}")

    def error(self, message: str):
        print(f"[ERROR] {self.name}: {message}")

    def debug(self, message: str):
        print(f"[DEBUG] {self.name}: {message}")
