import json
import re

from collections import Counter
from dataclasses import dataclass, fields


@dataclass
class Bus:
    """
    Keeps track of bus data
    """
    bus_id: int
    stop_id: int
    stop_name: str
    next_stop: int
    stop_type: str
    a_time: str

    @property
    def error_fields(self) -> dict[str, bool]:
        error_dict: dict[str, bool] = {field.name: True for field in fields(self)}
        optional_str_fields: list[str] = ["stop_type"]
        stop_name_pattern: str = r"([A-Z].*) (Road|Avenue|Boulevard|Street)$"
        stop_type_values: set = {'S', 'O', 'F', ""}
        a_time_pattern: str = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"

        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                """raise ValueError(f"Expected {field.name} to be {field.type}, got {repr(value)}")"""
            elif isinstance(value, str) and field.name not in optional_str_fields and value == "":
                """raise Exception("No empty strings")"""
            elif field.name == "stop_name" and not re.match(stop_name_pattern, value):
                """raise Exception("Incorrect format")"""
            elif field.name == "stop_type" and value not in stop_type_values:
                """raise Exception("Invalid type")"""
            elif field.name == "a_time" and not re.match(a_time_pattern, value):
                """raise Exception("Invalid time")"""
            else:
                error_dict[field.name] = False

        return error_dict


def input_json() -> list[dict]:
    return json.loads(input())


# Stage 1 & 2 Function
def print_error_count(list_of_data: list[Bus], relevant_fields: list[str]):
    data_error_counter: dict[str, int] = {field.name: 0 for field in fields(list_of_data[0])}

    for data in list_of_data:
        for key in data.error_fields:
            data_error_counter[key] += data.error_fields[key]

    total_errors: int = sum(data_error_counter.values())
    print(f"Format validation: {total_errors} errors")
    for field_name, error_count in data_error_counter.items():
        if field_name in relevant_fields:
            print(f"{field_name}: {error_count}")


# Stage 3 Function
def print_bus_line_info(bus_data: list[Bus]):
    print("Line names and number of stops:")
    bus_id_data: list[int] = [bus.bus_id for bus in bus_data]
    bus_id_counter = Counter(bus_id_data)
    for bus_id, stops in bus_id_counter.items():
        print(f"bus_id: {bus_id}, stops: {stops}")


def validate_stops(bus_data: list[Bus]) -> bool:
    all_bus_ids: set[int] = {bus.bus_id for bus in bus_data}
    bus_id_to_stop_types: dict[int, set[str]] = {bus_id: set() for bus_id in all_bus_ids}
    for bus in bus_data:
        bus_id_to_stop_types[bus.bus_id].add(bus.stop_type)

    for bus_id, stop_types in bus_id_to_stop_types.items():
        if not {'S', 'F'}.issubset(stop_types):
            print(f"There is no start or end stop for the line: {bus_id}.")
            return False

    return True


def print_special_stops(bus_data: list[Bus]):
    all_stop_ids: list[int] = [bus.stop_id for bus in bus_data]
    all_next_stops: list[int] = [bus.next_stop for bus in bus_data]
    start_stops: set[str] = {bus.stop_name for bus in bus_data if bus.stop_id not in all_next_stops}
    transfer_stops: set[str] = {bus.stop_name for bus in bus_data if all_stop_ids.count(bus.stop_id) > 1}
    finish_stops: set[str] = {bus.stop_name for bus in bus_data if bus.next_stop not in all_stop_ids}

    print("Start stops:", len(start_stops), sorted(start_stops))
    print("Transfer stops:", len(transfer_stops), sorted(transfer_stops))
    print("Finish stops:", len(finish_stops), sorted(finish_stops))


def main():
    buses: list[dict] = input_json()
    bus_data = [Bus(**bus) for bus in buses]
    # relevant_fields: list[str] = ["stop_name", "stop_type", "a_time"]
    if validate_stops(bus_data):
        print_special_stops(bus_data)


if __name__ == "__main__":
    main()
