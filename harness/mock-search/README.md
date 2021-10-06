# Mock Search

This directory represents what a consumer would need to provide in order to run
the benchmark against a particular search tool.

The "search" (such as it is) is implemented in `tool.py`, and the `Dockerfile`
just adds `tool.py`. In normal use, the base image might be a
tool-specific image, which are fairly common at this point. However, if there is
no existing image for the tool in question, the benchmark-specific `Dockerfile`
(the one in this directory) could build / install it.

To build the container:

```
docker build -t psss-harness .
```

