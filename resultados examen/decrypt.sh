#!/bin/bash

for f in *.enc;
do
  openssl aes-256-cbc -d -a -pbkdf2 -in $f -out tirreau-${f}.pdf -k miclave;
done;
