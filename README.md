# awsipcheck

`awsipcheck` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not. This has multiple applications:

- Continuous recon of assets
- Gather assets using a specific service (e.g. EC2)
- Finding region information for S3 buckets
- ... etc.


![awsipcheck](https://user-images.githubusercontent.com/3582096/123559813-fe493980-d7bb-11eb-90f9-cd33942c0818.png)


# Install

```
pip install awsipcheck
```

# Usage

## Given an IP:
```
awsipcheck 52.219.47.34
```

## Given a hostname:

A domain or subdomain can be passed as input:

```
awsipcheck example.com
```

You may also supply an S3 bucket hostname as input:

```
awsipcheck dropbox.s3.amazonaws.com
```

# Output

If the IP/hostname falls in the AWS IP range, `awsipcheck` will return the service, region and other details in the output:

```
{
    "is_aws_ip": true,
    "ip_address": "52.218.196.155",
    "service": "S3",
    "region": "us-west-2",
    "matched_subnet": "52.218.128.0/17",
    "hostname": "flaws.cloud"
}
```