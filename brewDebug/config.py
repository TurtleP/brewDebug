class Config:

    def __init__(self, config):
        self.hac_path = config["hac"]
        self.ctr_path = config["ctr"]

    def get(self, console):
        return getattr(self, f"{console}_path")