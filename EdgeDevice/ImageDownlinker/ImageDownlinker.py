import time
import threading

class ImageDownlinker:
    def __init__(self, groundstation1, groundstation2):
        self.groundstation1 = groundstation1
        self.groundstation2 = groundstation2
        self.active_groundstation = groundstation1
        self.downlink_thread = None
        self.is_downlinking = False
        self.is_paused = False
        self.pause_event = threading.Event()

    def monitor_heartbeats(self):
        while True:
            if self.active_groundstation.is_heartbeat_received():
                print(f"Heartbeat received from {self.active_groundstation.name}.")
                if not self.is_downlinking:
                    self.start_downlink()
                elif self.is_paused:
                    self.resume_downlink()
            else:
                print(f"No heartbeat received from {self.active_groundstation.name}. Switching ground station.")
                self.switch_groundstation()

            time.sleep(5)  # Sleep for 5 seconds between heartbeat checks

    def switch_groundstation(self):
        if self.active_groundstation == self.groundstation1:
            self.active_groundstation = self.groundstation2
        else:
            self.active_groundstation = self.groundstation1

        if self.is_downlinking:
            self.pause_downlink()
            self.start_downlink()

    def start_downlink(self):
        self.is_downlinking = True
        self.downlink_thread = threading.Thread(target=self._downlink_images)
        self.downlink_thread.start()

    def _downlink_images(self):
        print(f"Starting satellite downlink to {self.active_groundstation.name}.")

        while self.is_downlinking:
            if not self.is_paused:
                # Perform the downlinking process here
                # You can add your actual implementation

                print(f"Downlinking image to {self.active_groundstation.name}.")
                time.sleep(1)  # Simulating downlinking one image

            self.pause_event.wait()

    def pause_downlink(self):
        if self.is_downlinking and not self.is_paused:
            self.is_paused = True
            self.pause_event.clear()
            print("Pausing downlinking process.")

    def resume_downlink(self):
        if self.is_downlinking and self.is_paused:
            self.is_paused = False
            self.pause_event.set()
            print(f"Resuming downlinking process to {self.active_groundstation.name}.")

# Rest of the code remains the same

# Example usage
gs1 = GroundStation("Ground Station 1")
gs2 = GroundStation("Ground Station 2")

downlinker = ImageDownlinker(gs1, gs2)
downlinker.monitor_heartbeats()
