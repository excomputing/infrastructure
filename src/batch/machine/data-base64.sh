#!/bin/bash

: << 'comment'
This script converts the user data script, data.txt, to a Base 64 format.
comment

base64 "src/batch/machine/data.txt" > "src/batch/machine/data-base64.txt"
