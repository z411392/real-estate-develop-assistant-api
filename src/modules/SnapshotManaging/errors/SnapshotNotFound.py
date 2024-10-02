class SnapshotNotFound(Exception):
    def __init__(self):
        super().__init__(self, f"""SnapshotNotFound""")
