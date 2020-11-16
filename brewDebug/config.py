class Config:

    VALID_ENTRIES = ["hac", "ctr"]

    def __init__(self, config):
        self.entries = dict()

        for key, value in config.items():
            self.validate(key, value)

    def validate(self, key, value):
        for entry, _ in value.items():
            if entry in Config.VALID_ENTRIES:
                self.entries[key] = value
            else:
                raise Exception(f"config load error: unexpected entry '{entry}' for {key}")

    def get_first(self):
        keys = list(self.entries.keys())
        return keys[0]

    def get_len(self):
        return len(self.entries.keys())

    def get_entry(self, entry, console):
        return self.entries[entry][console]

    def get(self, console):
        entry = self.get_first()
        return self.get_entry(entry, console)
