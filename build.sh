#!/bin/bash

DATE_TAG=$(date +%Y%m%d%H)
VER_TAG=1.1
REPO_ROOT=$(pwd)

REGISTRY_ORG=quay.io/rhnspdev
SENSOR_IMAGE=${REGISTRY_ORG}/groundbreaker-sensor
PROCESSOR_IMAGE=${REGISTRY_ORG}/groundbreaker-processor
DOWNLINKER_IMAGE=${REGISTRY_ORG}/groundbreaker-downlinker
RECEIVER_IMAGE=${REGISTRY_ORG}/groundbreaker-receiver
FORWARDER_IMAGE=${REGISTRY_ORG}/groundbreaker-forwarder
S3UPLOADER_IMAGE=${REGISTRY_ORG}/groundbreaker-s3uploader


## BUILD IMAGES

# SENSOR
podman build --no-cache -t ${SENSOR_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/sensor
podman push ${SENSOR_IMAGE}:${VER_TAG}_${DATE_TAG}

# PROCESSOR
podman build --no-cache -t ${PROCESSOR_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/processor
podman push ${PROCESSOR_IMAGE}:${VER_TAG}_${DATE_TAG}

# DOWNLINKER
podman build --no-cache -t ${DOWNLINKER_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/downlinker
podman push ${DOWNLINKER_IMAGE}:${VER_TAG}_${DATE_TAG}

# RECEIVER
podman build --no-cache -t ${RECEIVER_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/receiver
podman push ${RECEIVER_IMAGE}:${VER_TAG}_${DATE_TAG}

# FORWARDER
podman build --no-cache -t ${FORWARDER_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/forwarder
podman push ${FORWARDER_IMAGE}:${VER_TAG}_${DATE_TAG}

# S3UPLOADER
podman build --no-cache -t ${S3UPLOADER_IMAGE}:${VER_TAG}_${DATE_TAG} $REPO_ROOT/s3uploader
podman push ${S3UPLOADER_IMAGE}:${VER_TAG}_${DATE_TAG}
