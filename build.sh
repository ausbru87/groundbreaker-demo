#!/bin/bash

DATE_TAG=$(date +%Y%m%d)
LATEST_TAG=latest
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
podman build --no-cache -t ${SENSOR_IMAGE}:${DATE_TAG} $REPO_ROOT/sensor
podman tag ${SENSOR_IMAGE}:${DATE_TAG} ${SENSOR_IMAGE}:${LATEST_TAG}
podman push ${SENSOR_IMAGE}:${DATE_TAG}
podman push ${SENSOR_IMAGE}:${LATEST_TAG}

# PROCESSOR
podman build --no-cache -t ${PROCESSOR_IMAGE}:${DATE_TAG} $REPO_ROOT/processor
podman tag ${PROCESSOR_IMAGE}:${DATE_TAG} ${PROCESSOR_IMAGE}:${LATEST_TAG}
podman push ${PROCESSOR_IMAGE}:${DATE_TAG}
podman push ${PROCESSOR_IMAGE}:${LATEST_TAG}

# DOWNLINKER
podman build --no-cache -t ${DOWNLINKER_IMAGE}:${DATE_TAG} $REPO_ROOT/downlinker
podman tag ${DOWNLINKER_IMAGE}:${DATE_TAG} ${DOWNLINKER_IMAGE}:${LATEST_TAG}
podman push ${DOWNLINKER_IMAGE}:${DATE_TAG}
podman push ${DOWNLINKER_IMAGE}:${LATEST_TAG}

# RECEIVER
podman build --no-cache -t ${RECEIVER_IMAGE}:${DATE_TAG} $REPO_ROOT/receiver
podman tag ${RECEIVER_IMAGE}:${DATE_TAG} ${RECEIVER_IMAGE}:${LATEST_TAG}
podman push ${RECEIVER_IMAGE}:${DATE_TAG}
podman push ${RECEIVER_IMAGE}:${LATEST_TAG}

# FORWARDER
podman build --no-cache -t ${FORWARDER_IMAGE}:${DATE_TAG} $REPO_ROOT/forwarder
podman tag ${FORWARDER_IMAGE}:${DATE_TAG} ${FORWARDER_IMAGE}:${LATEST_TAG}
podman push ${FORWARDER_IMAGE}:${DATE_TAG}
podman push ${FORWARDER_IMAGE}:${LATEST_TAG}

# S3UPLOADER
podman build --no-cache -t ${S3UPLOADER_IMAGE}:${DATE_TAG} $REPO_ROOT/s3uploader
podman tag ${S3UPLOADER_IMAGE}:${DATE_TAG} ${S3UPLOADER_IMAGE}:${LATEST_TAG}
podman push ${S3UPLOADER_IMAGE}:${DATE_TAG}
podman push ${S3UPLOADER_IMAGE}:${LATEST_TAG}