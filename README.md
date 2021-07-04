# onaws

`onaws` is a simple tool to check if an IP/hostname belongs to the AWS IP space or not. It uses the [AWS IP address ranges data](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) published by AWS to perform the search.

The tool could be used for:

- Continuous recon of assets
- Gathering assets using a specific service (e.g. EC2)
- Finding region information for S3 buckets
- etc.

![onaws](https://user-images.githubusercontent.com/3582096/123629032-684ff600-d831-11eb-8e22-7ab4bbac03e1.png)

# Install

```shell
pip install onaws
```

# Usage

## Given an IP:
```shell
onaws 52.219.47.34
```

## Given a hostname:

A domain or subdomain can be passed as input:

```shell
onaws example.com
```

You may also supply an S3 bucket hostname as input:

```shell
onaws dropbox.s3.amazonaws.com
```

## Given an input list

### WARNING: onaws resolves each hostname individually, so if you're going to supply many hostnames, it's significantly faster to resolve them first with a tool like [MassDNS](https://github.com/blechschmidt/massdns)!

`onaws` accepts line-delimited hosts on STDIN. This is helpful if you want to pipe the output of other tools to `onaws`:

```shell
$ cat hosts.txt
uber.s3.amazonaws.com
aws.com
google.com
23.21.52.140


$ cat hosts.txt | onaws
{
    "is_aws_ip": true,
    "ip_address": "52.218.106.162",
    "service": "S3",
    "region": "eu-west-1",
    "matched_subnet": "52.218.0.0/17",
    "hostname": "uber.s3.amazonaws.com"
}
{
    "is_aws_ip": true,
    "ip_address": "143.204.225.9",
    "service": "CLOUDFRONT",
    "region": "GLOBAL",
    "matched_subnet": "143.204.0.0/16",
    "hostname": "aws.com"
}
{
    "is_aws_ip": false,
    "ip_address": "216.58.201.238",
    "hostname": "google.com"
}
{
    "is_aws_ip": true,
    "ip_address": "23.21.52.140",
    "service": "EC2",
    "region": "us-east-1",
    "matched_subnet": "23.20.0.0/14"
}
```

# Output

If the IP/hostname falls in the AWS IP range, `onaws` will return the service, region and other details in the output:

```json
{
    "is_aws_ip": true,
    "ip_address": "52.218.196.155",
    "service": "S3",
    "region": "us-west-2",
    "matched_subnet": "52.218.128.0/17",
    "hostname": "flaws.cloud"
}
```

For multiple inputs, the output format will be in JSONL:

```json
{
    "is_aws_ip": true,
    "ip_address": "143.204.225.9",
    "service": "CLOUDFRONT",
    "region": "GLOBAL",
    "matched_subnet": "143.204.0.0/16",
    "hostname": "aws.com"
}
{
    "is_aws_ip": false,
    "ip_address": "216.58.201.238",
    "hostname": "google.com"
}
{
    "is_aws_ip": true,
    "ip_address": "23.21.52.140",
    "service": "EC2",
    "region": "us-east-1",
    "matched_subnet": "23.20.0.0/14"
}
```

If you want to save the output to a file, you can use Bash redirection or `tee`:

```shell
cat hosts | onaws | tee -a output.json
```

## More examples

To get hosts that use EC2:

```shell
cat output.json | jq -scr '.[] | select(.service == "EC2") | .hostname'
```
Output:

```
groove.uber.com
photos.uber.com
photography.uber.com
...
```

To get a list of hosts that use AWS services:

```shell
cat output.json | jq -sc '.[] | select(.is_aws_ip == true ) | [.hostname, .ip_address, .service] | join (",")' 
```

Output:

```csv
assets-share.uber.com,52.84.13.77,CLOUDFRONT
groove.uber.com,3.223.41.171,EC2
devbuilds.uber.com,52.84.13.29,CLOUDFRONT
photos.uber.com,54.237.133.81,EC2
...
```

## Errors

If the input you provide is an invalid IP or is not resolvable, the output will indicate so:

```shell
$ onaws 'invalid.invalid'
{
    "hostname": "invalid.invalid",
    "resolvable": false
}
```

If, for some reason, the tool fails to fetch the AWS IP ranges, it will throw the following exception:

```shell
$ onaws
Failed to get AWS IP ranges
```

# Contribution

I welcome contributions from the public. If you find something that could be improved, please file an Issue or send a PR :)

# Credits

- Thanks to @TomNomNom for suggesting the name.
