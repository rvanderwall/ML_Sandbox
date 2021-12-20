#!/bin/bash

cd ..

gunicorn -w 1 -b 127.0.0.1:4041 "CryptoCurrency.app:create_app()" &
gunicorn -w 1 -b 127.0.0.1:4042 "CryptoCurrency.app:create_app()" &
