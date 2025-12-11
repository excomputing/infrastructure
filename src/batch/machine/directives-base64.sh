#!/bin/bash

: << 'comment'
This script converts the user data script, data.txt, to a Base 64 format.
comment

base64 "src/batch/machine/directives.txt" > "src/batch/machine/directives-base64.txt"
