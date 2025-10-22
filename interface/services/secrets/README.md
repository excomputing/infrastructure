
<br>

### Notes

Instead of typing sensitive data along a client interface prompt, encode the details within a file beforehand.  Afterwards, destroy the file:[^risks]

```shell
shred -u $path
```

The variable `$path` excludes `file://`, but includes the file name and its extension.

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>

[^risks]: <a href="https://docs.aws.amazon.com/secretsmanager/latest/userguide/security_cli-exposure-risks.html" target="_blank">Mitigate</a> the risks of using the AWS CLI to store your AWS Secrets Manager secrets

<br>
<br>