# Superpixels (SLIC) Web Service 

```
% export FLASK_APP=api.py
% flask run
```

Then try a query such as:

```
http://127.0.0.1:5000/api/superpixel?url=https://i.imgur.com/Q7xoeiA.png&n_segs=200
```

Where `n_segs` can range between 100 and 1000 inclusive. The return value is a JSON containing a list of Base64 encoded masks, each representing a superpixel.
