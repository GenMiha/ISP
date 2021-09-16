import create_serializer as serlib
ser = serlib.create_serializer("json")
def g(a, b):
   return a+b
with open("gg.json","w") as fp:
   ser.dump(g, fp)
