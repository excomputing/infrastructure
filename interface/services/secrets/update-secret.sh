#!/bin/bash

: << 'comment'
This script updates the keys of the dispatches project.
comment

path=file://interface/services/secrets

aws secretsmanager update-secret --cli-input-json "$path/update.json" --secret-string "$path/secret-string.json"
