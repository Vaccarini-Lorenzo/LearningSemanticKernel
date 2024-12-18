class DS:
    def __init__(self):
        self.curr_storage = None

    def update_storage(self, new_storage):
        self.curr_storage = new_storage

    def get_storage(self):
        return self.curr_storage

    def is_ready(self):
        return self.curr_storage is not None
