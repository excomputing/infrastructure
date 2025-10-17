#!/bin/bash

: << 'comment'
Deletes a secret key.
comment

aws secretsmanager delete-secret --cli-input-json file://interface/services/secrets/delete.json
