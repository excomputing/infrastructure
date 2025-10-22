#!/bin/bash

: << 'comment'
This program sets the keys for the ex-computing project.
comment

path=file://interface/services/secrets

aws secretsmanager create-secret --cli-input-json "$path/define.json"  --secret-string "$path/secret-string.json"
