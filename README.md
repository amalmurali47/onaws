# awsipcheck

`awsipcheck` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not.

![awsipcheck](https://user-images.githubusercontent.com/3582096/123546169-219ec500-d779-11eb-8fc6-7ed6ecd990bd.png)

# Install

```
pip install awsipcheck
```

# Usage

## Given an IP:
```
awsipcheck -ip 52.219.47.34
```

## Given a hostname:

```
awsipcheck dropbox.s3.amazonaws.com
```

## Given a bucket name:

You can also supply an S3 bucket name as input:

```
awsipcheck -bucket dropbox
```

Or the full bucket URL:

```
awsipcheck -bucket http://dropbox.s3.amazonaws.com
```

# Output

If the IP falls in the AWS IP range, `awsipcheck` will return the details:

```
52.219.47.34 is an AWS IP. Details:
{
    "ip_prefix": "52.219.44.0/22",
    "region": "eu-central-1",
    "service": "AMAZON",
    "network_border_group": "eu-central-1"
}
```

If you only require the region in the output, you can specify the `-only-region` flag like so:

```
awsipcheck -bucket dropbox -only-region
```

And it will print just the region (and `False` otherwise):

```
eu-central-1
```