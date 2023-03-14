# django-ninja-benchmarks

### Requirements

 - Python3
 - Docker + docker-compose
 - ab 

###

Run 

```
python run_test.py
```

### Results

```text
Framework               :        1        2        4        8       16       32       64
drf_uwsgi               :     9.37    18.95    37.15    70.35   123.77   209.73   234.63
fastapi_gunicorn        :     9.57    17.52    36.13    52.74   113.62   208.13   262.85
fastapi_uvicorn         :     9.50    17.94    31.52    55.63   118.94   167.54   194.12
flask_marshmallow_uwsgi :     9.53    18.75    37.04    72.74   131.16   229.92   326.55
ninja_gunicorn          :   240.49   278.57   317.09   309.32   285.71   246.44   256.98
ninja_uvicorn           :   265.31   289.09   280.00   305.05   247.62   237.71   212.58
ninja_uwsgi             :     9.29    18.56    36.04    68.98   128.32   180.89   182.31
Columns indicate the number of workers in each run
Values are in requests per second - higher is better.
```