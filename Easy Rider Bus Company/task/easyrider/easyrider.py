import json
import re

FIELDS = [{"name": "bus_id",
           "type": "int",
           "required": True,
           "regex": [r"^\d+$"],
           "need_to_validate": False
           },
          {"name": "stop_id",
           "type": "int",
           "required": True,
           "regex": [r"^\d+$"],
           "need_to_validate": False
           },
          {"name": "stop_name",
           "type": "str",
           "required": True,
           "regex": [r"^[A-Z].*\sRoad$",
                     r"^[A-Z].*\sAvenue$",
                     r"^[A-Z].*\sBoulevard$",
                     r"^[A-Z].*\sStreet$"
                     ],
           "need_to_validate": True
           },
          {"name": "next_stop",
           "type": "int",
           "required": True,
           "regex": [r"^\d+$"],
           "need_to_validate": False
           },
          {"name": "stop_type",
           "type": "str",
           # "max_length": 1,
           "required": False,
           "regex": [r"^[SOF]$",
                     r"$"
                     ],
           "need_to_validate": True
           },
          {"name": "a_time",
           "type": "str",
           "required": True,
           "regex": [r"^0\d:[0-5]\d$",
                     r"^1\d:[0-5]\d$",
                     r"^2[0-3]:[0-5]\d$"
                     ],
           "need_to_validate": True
           # "min_length": 5,
           }]

test = '[{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": ' \
       '8.12}, {"bus_id": 128, "stop_id": 3, "stop_name": "", "next_stop": 5, "stop_type": "", "a_time": "08:19"}, ' \
       '{"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": "O", ' \
       '"a_time": "08:25"}, {"bus_id": 128, "stop_id": "7", "stop_name": "Sesame Street", "next_stop": 0, ' \
       '"stop_type": "F", "a_time": "08:37"}, {"bus_id": "", "stop_id": 2, "stop_name": "Pilotow Street", ' \
       '"next_stop": 3, "stop_type": "S", "a_time": ""}, {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street", ' \
       '"next_stop": 6, "stop_type": "", "a_time": "09:45"}, {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset ' \
       'Boulevard", "next_stop": 7, "stop_type": "", "a_time": "09:59"}, {"bus_id": 256, "stop_id": 7, "stop_name": ' \
       '"Sesame Street", "next_stop": "0", "stop_type": "F", "a_time": "10:12"}, {"bus_id": 512, "stop_id": 4, ' \
       '"stop_name": "Bourbon Street", "next_stop": 6, "stop_type": "S", "a_time": "08:13"}, {"bus_id": "512", ' \
       '"stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": 5, "a_time": "08:16"}] '

test2 = '[{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Av.", "next_stop": 3, "stop_type": "S", "a_time": ' \
        '"08:12"}, {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "", ' \
        '"a_time": "8:19"}, {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": ' \
        '"OO", "a_time": "08:25"}, {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, ' \
        '"stop_type": "F", "a_time": "08:77"}, {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street", ' \
        '"next_stop": 3, "stop_type": "S", "a_time": "09:20"}, {"bus_id": 256, "stop_id": 3, "stop_name": "Elm", ' \
        '"next_stop": 6, "stop_type": "", "a_time": "09:45"}, {"bus_id": 256, "stop_id": 6, "stop_name": "Sunset ' \
        'Boulevard", "next_stop": 7, "stop_type": "A", "a_time": "09:59"}, {"bus_id": 256, "stop_id": 7, "stop_name": ' \
        '"Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "10.12"}, {"bus_id": 512, "stop_id": 4, ' \
        '"stop_name": "bourbon street", "next_stop": 6, "stop_type": "S", "a_time": "38:13"}, {"bus_id": 512, ' \
        '"stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}] '

test3 = '[{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": ' \
        '"08:12"}, {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "", ' \
        '"a_time": "08:19"}, {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": ' \
        '"O", "a_time": "08:25"}, {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, ' \
        '"stop_type": "F", "a_time": "08:37"}, {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street", ' \
        '"next_stop": 3, "stop_type": "S", "a_time": "09:20"}, {"bus_id": 256, "stop_id": 3, "stop_name": "Elm ' \
        'Street", "next_stop": 6, "stop_type": "", "a_time": "09:45"}, {"bus_id": 256, "stop_id": 6, "stop_name": ' \
        '"Sunset Boulevard", "next_stop": 7, "stop_type": "", "a_time": "09:59"}, {"bus_id": 256, "stop_id": 7, ' \
        '"stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "10:12"}, {"bus_id": 512, ' \
        '"stop_id": 4, "stop_name": "Bourbon Street", "next_stop": 6, "stop_type": "S", "a_time": "08:13"}, ' \
        '{"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", ' \
        '"a_time": "08:16"}] '

test4 = '[{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": ' \
        '"08:12"}, {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "", ' \
        '"a_time": "08:19"}, {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": ' \
        '"O", "a_time": "08:25"}, {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, ' \
        '"stop_type": "F", "a_time": "08:37"}, {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street", ' \
        '"next_stop": 6, "stop_type": "", "a_time": "08:13"}, {"bus_id": 512, "stop_id": 6, "stop_name": "Sunset ' \
        'Boulevard", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}] '

test5 = '[{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": ' \
        '"08:12"}, {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "", ' \
        '"a_time": "08:19"}, {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": ' \
        '"O", "a_time": "08:17"}, {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, ' \
        '"stop_type": "F", "a_time": "08:07"}, {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street", ' \
        '"next_stop": 3, "stop_type": "S", "a_time": "09:20"}, {"bus_id": 256, "stop_id": 3, "stop_name": "Elm ' \
        'Street", "next_stop": 6, "stop_type": "", "a_time": "09:45"}, {"bus_id": 256, "stop_id": 6, "stop_name": ' \
        '"Sunset Boulevard", "next_stop": 7, "stop_type": "", "a_time": "09:44"}, {"bus_id": 256, "stop_id": 7, ' \
        '"stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "10:12"}, {"bus_id": 512, ' \
        '"stop_id": 4, "stop_name": "Bourbon Street", "next_stop": 6, "stop_type": "S", "a_time": "08:13"}, ' \
        '{"bus_id": 512, "stop_id": 6, "stop_name": "Sunset Boulevard", "next_stop": 0, "stop_type": "F", ' \
        '"a_time": "08:16"}] '

test_str = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:17"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:07"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "",
        "a_time": "09:44"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
"""
# print(test)
# print(json.dumps(json.loads(test_str)))
# print(test4)
input_str = input()
# v_arr = json.loads(test_str)
if not input_str:
    input_str = test5

v_arr = json.loads(input_str)

errors = dict.fromkeys([x["name"] for x in FIELDS if x["need_to_validate"]], 0)

for r in v_arr:
    for f in [f for f in FIELDS if f["need_to_validate"]]:
        value = r.get(f["name"])
        if value is not None:
            if str(type(value)) == ("<class '{0}'>".format(f["type"])):
                if not any([re.match(x, str(value)) for x in f["regex"]]):
                    errors[f["name"]] = errors[f["name"]] + 1
            else:
                errors[f["name"]] = errors[f["name"]] + 1
        elif f["required"]:
            errors[f["name"]] = errors[f["name"]] + 1

# print("Type and required field validation: {} errors".format(sum(errors.values())))
# print("\n".join([k + ": " + str(v) for k, v in errors.items()]))

lines = dict()
stops = dict()  # {item["stop_id"]: item["stop_name"] for item in v_arr}
start_stops = set()
finish_stops = set()

for item in v_arr:
    bus_id = item.pop('bus_id')
    stop_id = item.pop("stop_id")

    line = lines[bus_id] = lines.get(bus_id,  {"start": None, "finish": None, "stops": dict()})
    stop = stops[stop_id] = stops.get(stop_id,  {"stop_name": item["stop_name"], "lines": []})

    line["stops"][stop_id] = item
    stop["lines"].append(bus_id)

    if item["stop_type"] == "S":
        if line["start"] is None:
            line["start"] = stop_id
            start_stops.add(item["stop_name"])
        else:
            print(f"Start point is duplicated for the line: {bus_id}")
            exit()
    elif item["stop_type"] == "F":
        if line["finish"] is None:
            line["finish"] = stop_id
            finish_stops.add(item["stop_name"])
        else:
            print(f"Final stop is duplicated for the line: {bus_id}")
            exit()

# print(lines)
# print(stops)

# print("Line names and number of stops:")
# print("\n".join(["bus_id: " + str(k) + ", stops: " + str(len(v)) for k, v in lines.items()]))

for bus_id, line in lines.items():
    if line['start'] is None or line['finish'] is None:
        print(f"There is no start or end stop for the line: {bus_id}")
        exit()

transfer_stops = [v["stop_name"] for v in stops.values() if len(v["lines"]) > 1]

# print("Start stops:", len(start_stops), sorted(start_stops))
# print("Transfer stops:", len(transfer_stops), sorted(transfer_stops))
# print("Finish stops:", len(finish_stops), sorted(finish_stops))

wrong_time_stops = dict()

for bus_id, line in lines.items():
    l_stops = line["stops"]
    cur_s = l_stops[line["start"]]
    while cur_s["next_stop"]:
        next_s = l_stops[cur_s["next_stop"]]
        if cur_s["a_time"] >= next_s["a_time"]:
            wrong_time_stops[bus_id] = next_s["stop_name"]
            break
        cur_s = next_s

# print(wrong_time_stops)

print("Arrival time test:")
if len(wrong_time_stops):
    for bus_id, stop in wrong_time_stops.items():
        print(f"bus_id line {bus_id}: wrong time on station {stop}")
else:
    print("OK")
