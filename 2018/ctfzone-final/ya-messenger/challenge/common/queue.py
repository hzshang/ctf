import queue

from threading import Lock


class Queues(object):
    def __init__(self):
        self.queues = {}
        self.lock = Lock()

    def get(self, entity_id, key):
        with self.lock:
            if entity_id not in self.queues:
                self.queues[entity_id] = {}

            if key not in self.queues[entity_id]:
                self.queues[entity_id][key] = queue.SimpleQueue()

            return self.queues[entity_id][key]

    def delete(self, entity_id, key):
        with self.lock:
            if entity_id in self.queues and \
                    key in self.queues[entity_id]:
                del self.queues[entity_id][key]

    def all_for_entity(self, entity_id):
        if entity_id not in self.queues:
            return []

        return self.queues[entity_id].values()
