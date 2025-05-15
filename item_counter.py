import json
from glob import glob
from argparse import ArgumentParser


class ConfigParser:
    def __init__(self):
        self.parser = ArgumentParser()
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument('-p', '--path', required=True, type=str)

    def parse(self):
        return self.parser.parse_args()


def _list_files(path):
    return glob(f'{path}*.json')


class ItemCounter:
    def __init__(self, path):
        self.path = path

    def count_item(self):
        total = 0
        for file in _list_files(self.path):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                trackers = data.get('trackers', [])
                for item in trackers:
                    work_items = item.get('work_items')
                    if isinstance(work_items, list):
                        total += len(work_items)
            except Exception as e:
                print(f"ERROR reading {file}: {e}")
        return total


if __name__ == '__main__':
    config = ConfigParser()
    args = config.parse()
    item_counter = ItemCounter(args.path)
    total = item_counter.count_item()
    print(f"Number of work items found {total}")
