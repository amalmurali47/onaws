# awsipcheck

`awsipcheck` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not. This has multiple applications:

- Continuous recon of assets
- Gather assets using a specific service (e.g. EC2)
- Finding region information for S3 buckets
- ... and so on


![awsipcheck](https://user-images.githubusercontent.com/3582096/123551848-31c29e80-d791-11eb-87f1-98b1a9fb9512.png)


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
awsipcheck -hostname google.com
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

If the IP/hostname falls in the AWS IP range, `awsipcheck` will return the details:

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