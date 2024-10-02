class UserUnauthenticated(Exception):
    def __init__(self):
        super().__init__(self, f"""UserUnauthenticated""")
