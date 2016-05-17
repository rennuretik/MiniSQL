def hello():
    raise Exception("io error")

try:
    hello()
except Exception as e:
    print(e)
finally:
    print("hello")