# data.tomhummel.com
[![Build Status](https://travis-ci.org/tphummel/data.tomhummel.com.svg?branch=master)](https://travis-ci.org/tphummel/data.tomhummel.com)

## what? why?

This repo is the code and content behind [data.tomhummel.com](https://data.tomhummel.com). This blog exists to publish data of and adjacent to [Tom Hummel](https://tomhummel.com). And more generally, it exists to publish techniques for exfiltrating and analyzing personal data.

## setup

1. download [Hugo 0.34](https://github.com/gohugoio/hugo/releases/download/v0.34/hugo_0.34_macOS-64bit.tar.gz)
1. expand the downloaded tar.gz
1. move it to a directory in your $PATH

```
git clone git@github.com:tphummel/data.tomhummel.com.git
```

## dev

```
hugo server -D -w
```

## publish

```
rm -rf public/
hugo
aws s3 sync --delete public/ s3://my-bucket/
```
