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
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
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
        "a_time": "09:59"
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
# print(test2)
v_arr = json.loads(input())
# v_arr = json.loads(test_str)

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

bus_stat = dict()

for r in v_arr:
    new_set = bus_stat.get(r["bus_id"], set())
    new_set.add(r["stop_id"])
    bus_stat.update([(r["bus_id"], new_set)])

print("Line names and number of stops:")
print("\n".join(["bus_id: " + str(k) + ", stops: " + str(len(v)) for k, v in bus_stat.items()]))


