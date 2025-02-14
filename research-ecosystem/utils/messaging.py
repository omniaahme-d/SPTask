from queue import Queue
import threading

class MessageBus:
    def __init__(self):
        self.queues = {
            'research': Queue(),
            'analysis': Queue(),
            'innovation': Queue()
        }
        self.lock = threading.Lock()
    
    def post(self, channel, message):
        with self.lock:
            self.queues[channel].put(message)
    
    def get(self, channel):
        with self.lock:
            return self.queues[channel].get() if not self.queues[channel].empty() else None