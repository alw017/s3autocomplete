Warning: this plugin overrides all default completion behavior for a command.

This autocompletion script will try to complete any argument given as an s3 URI. (s3://\<bucket\>/\<object\>)

To set a custom list of buckets to autocomplete, set the `S3ACPL_BUCKETS` environment variable as a single space delimited string of bucket names. E.g. "bucket1 bucket2 bucket3"

You can also use the `.s3autocomplete_cfg` located in your home directory. Example: BUCKETS=bucket1 bucket2 bucket3

# To Install:

This script requires boto3. Use `pip install boto3` to install.

Setup your aws credentials. You can either use `aws configure` or add it manually in the default location `.aws/credentials`.

This is at minimum what a credentials file should have:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Next, in your .bashrc file source the script `s3autocomplete`. In the file `s3autocomplete`, change the name of `devtest` to any command of your choosing.`
