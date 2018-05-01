# Container API

This is a Docker image to do the following:

 - Connect to a Google Storage Singularity Registry
 - Compare the Containers in the Registry to the Local Record
 - For new containers, pull and update the metadata

The metadata, which maintains the same path as Google Cloud storage, is
served as a static json API on Github pages for researchers to take advantage of.


## Build

```bash
docker build -t vanessa/container-api .
```

## Generate or Update Database

```
export GOOGLE_STORAGE_BUCKET=singularityhub
# GOOGLE_APPLICATION_CREDENTIALS should be exported in environment

docker run --privileged -e GOOGLE_STORAGE_BUCKET \
                        -v $GOOGLE_APPLICATION_CREDENTIALS:/credentials.json \
                        vanessa/container-api
```

## Interactive Development

```
docker run --privileged -it -e GOOGLE_STORAGE_BUCKET \
                            -v $PWD/data:/data \
                            -v $GOOGLE_APPLICATION_CREDENTIALS:/credentials.json \
                            --entrypoint bash \
                            vanessa/container-api
```

## Run Locally
Note that you still have the requirements outlined in the Docker file! This is
what @vsoch uses sometimes because it's all set up and easy to update the database :)

 - spython=0.0.31
 - singularity 2.4.5
 - google-cloud-storage


```
export PATH=$PATH:../container-diff
export GOOGLE_STORAGE_BUCKET=singularityhub
# GOOGLE_APPLICATION_CREDENTIALS should be exported in environment
export API_DATABASE=$PWD/data

python generate.py
```
