File: **cases.pkl**\
Count cases: **50 778**

How to load cases in python:
```python
import zlib
import pickle
import json

with open('cases.pkl', 'rb') as f:
    tmp = pickle.load(f)

data = json.loads(zlib.decompress(tmp))
print(data[0])
```
Example 1 case:
```json
{
    "request": {
                    "date": "01.01.2022", 
                    "amount": 5000, 
                    "rate": 0.0, 
                    "periods": 0
                },
    "response": {
                    "code": 400,
                    "date": null,
                    "sum": null,
                    "sum_s": null,
                    "sum_e": null
                },
    "id": 1
}
```