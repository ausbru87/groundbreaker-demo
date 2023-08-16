#!/bin/bash

DATE_TAG=$(date +%Y%m%d%H%M)
REL_TAG=1.1
REPO_ROOT=$(pwd)
VER_TAG=1.1
FULL_TAG=${REL_TAG}

REGISTRY_ORG=quay.io/rhnspdev
SENSOR_IMAGE=${REGISTRY_ORG}/groundbreaker-sensor
PROCESSOR_IMAGE=${REGISTRY_ORG}/groundbreaker-processor
DOWNLINKER_IMAGE=${REGISTRY_ORG}/groundbreaker-downlinker
RECEIVER_IMAGE=${REGISTRY_ORG}/groundbreaker-receiver
FORWARDER_IMAGE=${REGISTRY_ORG}/groundbreaker-forwarder
S3UPLOADER_IMAGE=${REGISTRY_ORG}/groundbreaker-s3uploader


## BUILD IMAGES

# SENSOR
podman build --no-cache -t ${SENSOR_IMAGE}:${FULL_TAG} $REPO_ROOT/sensor
podman push ${SENSOR_IMAGE}:${FULL_TAG}

# PROCESSOR
podman build --no-cache -t ${PROCESSOR_IMAGE}:${FULL_TAG} $REPO_ROOT/processor
podman push ${PROCESSOR_IMAGE}:${FULL_TAG}

# DOWNLINKER
podman build --no-cache -t ${DOWNLINKER_IMAGE}:${FULL_TAG} $REPO_ROOT/downlinker
podman push ${DOWNLINKER_IMAGE}:${FULL_TAG}

# RECEIVER
podman build --no-cache -t ${RECEIVER_IMAGE}:${FULL_TAG} $REPO_ROOT/receiver
podman push ${RECEIVER_IMAGE}:${FULL_TAG}

# FORWARDER
podman build --no-cache -t ${FORWARDER_IMAGE}:${FULL_TAG} $REPO_ROOT/forwarder
podman push ${FORWARDER_IMAGE}:${FULL_TAG}

# S3UPLOADER
podman build --no-cache -t ${S3UPLOADER_IMAGE}:${FULL_TAG} $REPO_ROOT/s3uploader
podman push ${S3UPLOADER_IMAGE}:${FULL_TAG}

echo "NEW_TAG: ${FULL_TAG}"
echo "NEW_VERSION: ${VER_TAG}"
