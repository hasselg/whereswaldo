# Overview
The Docker images and the source code contained in this project will consume list of files from an AWS S3 bucket, extract the EXIF data, and then cache it in a MongoDB store where it can later be queried by the image filename.

This is accomplished using a minimum of four containers. The first container, `s3_publisher`, runs publisher.py. This script retrieves the listing of images from the bucket and submits the URL for each one as a new process_photo task to the `huey` container. The `huey` container runs [Huey](https://github.com/coleifer/huey) for processing tasks and has a dependency on a Redis instance, provided by the `redishost` container. The process_photo tasks are responsible for downloading the image from the given URL, extracting the EXIF, and then inserting it into the MongoDB store, running in the `mongo` container.
![data flow diagram](https://github.com/hasselg/whereswaldo/raw/master/whereswaldo_flow_diagram.png "Data Flow Diagram")

# Dependencies
This project depends on Docker. The Docker images defined within this project themselves have external dependencies, however, those should be resolved by the images themselves when they are built.

# Usage
The expected usage is with docker-compose. From the project root directory, run 
```
$ docker-compose build
$ docker-compose up
```
