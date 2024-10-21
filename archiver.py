import time
import random
from threading import Thread

class Archiver:
    _instance = None

    def __init__(self):
        self._status = "Waiting"
        self._progress = 0
        self._archive_file = None
        self._thread = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def status(self):
        return self._status

    def progress(self):
        return self._progress

    def run(self):
        if self._status == "Waiting":
            self._status = "Running"
            self._progress = 0
            self._archive_file = None
            self._thread = Thread(target=self._simulate_archiving)
            self._thread.start()

    def reset(self):
        if self._thread and self._thread.is_alive():
            # In a real implementation, we'd need a way to signal the thread to stop
            pass
        self._status = "Waiting"
        self._progress = 0
        self._archive_file = None
        self._thread = None

    def archive_file(self):
        return self._archive_file if self._status == "Complete" else None

    def _simulate_archiving(self):
        while self._progress < 1:
            time.sleep(0.5)  # Simulate work being done
            self._progress += random.uniform(0.1, 0.3)
            self._progress = min(self._progress, 1)
        
        self._status = "Complete"
        self._archive_file = "/path/to/archived_file.zip"

# Example usage
# if __name__ == "__main__":
#     archiver = Archiver.get()  # Get the Archiver instance for the current user
#     print(f"Initial status: {archiver.status()}")
    
#     archiver.run()
#     while archiver.status() != "Complete":
#         print(f"Status: {archiver.status()}, Progress: {archiver.progress():.2f}")
#         time.sleep(1)
    
#     print(f"Final status: {archiver.status()}")
#     print(f"Archive file: {archiver.archive_file()}")
    
#     archiver.reset()
#     print(f"After reset - Status: {archiver.status()}, Progress: {archiver.progress()}")

#     # Demonstrate that get() returns the same instance
#     another_archiver = Archiver.get()
#     print(f"Same instance: {archiver is another_archiver}")