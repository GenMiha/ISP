import create_serializer as serlib
ser = serlib.create_serializer("json")
with open("gg.json", "r") as fp:
    obj = ser.load(fp)
print(obj)
print(obj(1, 2))