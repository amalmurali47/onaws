# onaws

`onaws` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not. It uses the [AWS IP address ranges data](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) published by AWS to perform the search.

The tool could be used for:

- Continuous recon of assets
- Gathering assets using a specific service (e.g. EC2)
- Finding region information for S3 buckets
- ... etc.

![onaws](https://user-images.githubusercontent.com/3582096/123629032-684ff600-d831-11eb-8e22-7ab4bbac03e1.png)


# Install

```
pip install onaws
```

# Usage

## Given an IP:
```
onaws 52.219.47.34
```

## Given a hostname:

A domain or subdomain can be passed as input:

```
onaws example.com
```

You may also supply an S3 bucket hostname as input:

```
onaws dropbox.s3.amazonaws.com
```

## List of hostnames
`onaws` accepts line-delimited hosts on STDIN. This is helpful if you want to pipe the output of other tools to `onaws`:

```
$ cat hosts.txt
uber.s3.amazonaws.com
aws.com
google.com


$ cat hosts.txt | onaws
{
    "uber.s3.amazonaws.com": {
        "is_aws_ip": true,
        "ip_address": "52.218.46.121",
        "service": "S3",
        "region": "eu-west-1",
        "matched_subnet": "52.218.0.0/17",
        "hostname": "uber.s3.amazonaws.com"
    },
    "aws.com": {
        "is_aws_ip": true,
        "ip_address": "52.84.13.117",
        "service": "CLOUDFRONT",
        "region": "GLOBAL",
        "matched_subnet": "52.84.0.0/15",
        "hostname": "aws.com"
    },
    "google.com": {
        "is_aws_ip": false
    }
}

```

# Output

If the IP/hostname falls in the AWS IP range, `onaws` will return the service, region and other details in the output:

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

# Contribution
I welcome contributions from the public. If you find something that could be improved, please file an Issue or send a PR :)

# Credits

- Thanks to @TomNomNom for suggesting the name.
