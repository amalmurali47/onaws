# onaws

`onaws` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not. This has multiple applications:

- Continuous recon of assets
- Gather assets using a specific service (e.g. EC2)
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
