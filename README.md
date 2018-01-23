# data.tomhummel.com
[![Build Status](https://travis-ci.org/tphummel/data.tomhummel.com.svg?branch=master)](https://travis-ci.org/tphummel/data.tomhummel.com)

### setup

```
brew update
brew install hugo
```

### dev

```
hugo server -D -w
```

### publish

```
rm -rf public/
hugo
aws s3 sync --delete public/ s3://my-bucket/
```
