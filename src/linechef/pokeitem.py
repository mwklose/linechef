import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Pokeitem:
    ...

    @staticmethod
    def read_items_from_file(filename: Path, level_cap: int) -> List["Pokeitem"]:

        if not filename.exists():
            raise Exception(f"[Pokeitem] Could not find file {filename}")

        item_return_list = []
        with open(filename, "r") as f:
            for row in csv.reader(f, delimiter=","):
                print(row)

                if str(row[1]).isdigit() and int(row[1]) < level_cap:
                    item_return_list.append(row[0])

        return item_return_list
