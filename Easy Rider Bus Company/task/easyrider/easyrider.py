import json

FIELDS = [{"name": "bus_id",
           "type": "int",
           "required": True},
          {"name": "stop_id",
           "type": "int",
           "required": True},
          {"name": "stop_name",
           "type": "str",
           "min_length": 1,
           "required": True},
          {"name": "next_stop",
           "type": "int",
           "required": True},
          {"name": "stop_type",
           "type": "str",
           "max_length": 1,
           "required": False},
          {"name": "a_time",
           "type": "str",
           "min_length": 5,
           "required": True
           }]

errors = dict.fromkeys([x["name"] for x in FIELDS], 0)

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

test_str = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": 8.12
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "",
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
        "stop_id": "7",
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": "",
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": ""
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
        "next_stop": "0",
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
        "bus_id": "512",
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": 5,
        "a_time": "08:16"
    }
]
"""
# print(test)

v_arr = json.loads(input())
# print(json.dumps(json.loads(test_str)))
# v_arr = json.loads(test_str)

for r in v_arr:
    for f in FIELDS:
        value = r.get(f["name"])
        if value is not None:
            if str(type(value)) == ("<class '{0}'>".format(f["type"])):
                if f.get("max_length") and len(value) > f["max_length"]:
                    errors[f["name"]] = errors[f["name"]] + 1
                elif f.get("min_length") and len(value) < f["min_length"]:
                    errors[f["name"]] = errors[f["name"]] + 1
            else:
                errors[f["name"]] = errors[f["name"]] + 1
        elif f["required"]:
            errors[f["name"]] = errors[f["name"]] + 1
print("Type and required field validation: {} errors".format(sum(errors.values())))
print("\n".join([k + ": " + str(v)for k, v in errors.items()]))
