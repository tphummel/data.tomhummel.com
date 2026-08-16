# data.tomhummel.com

Code and content behind [data.tomhummel.com](https://data.tomhummel.com) — personal data publishing and analysis.

## Setup

Install [Hugo](https://gohugo.io/installation/) (tested with v0.148+).

```
git clone git@github.com:tphummel/data.tomhummel.com.git
```

## Dev

```
hugo server -D -w
```

## Publish

```
rm -rf public/
hugo
aws s3 sync --delete public/ s3://my-bucket/
```
