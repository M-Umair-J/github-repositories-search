import json
import os

class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.getcwd()), 'repositoryData', 'config.json')
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
                self.TOTAL_PARTITIONS = config_data.get('TOTAL_PARTITIONS', 0)
        else:
            self.TOTAL_PARTITIONS = 0
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({'TOTAL_PARTITIONS': self.TOTAL_PARTITIONS}, f)

    def update_total_partitions(self, value: int) -> None:
        self.TOTAL_PARTITIONS = value
        self.save_config()

    def get_total_partitions(self) -> int:
        return self.TOTAL_PARTITIONS

# create singleton instance
config = Config()