class TenantNameConflict(Exception):
    def __init__(self):
        super().__init__(self, f"""TenantNameConflict""")
