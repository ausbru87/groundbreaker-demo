## Pre-Run Cleanup
STORAGE_VOL=groundbreaker-storage
SENSOR_NAME=sensor
PROCESSOR_NAME=processor
DOWNLINKER_NAME=downlinker
CURRENT_TAG="1.1"
FACILITY_A="https://receiver-groundbreaker-prod.apps.groundbreaker-edgefac1.rhtps.io"
FACILITY_B="https://receiver-groundbreaker-prod.apps.groundbreaker-edgefac2.rhtps.io"

podman rm -f ${SENSOR_NAME}
podman rm -f ${PROCESSOR_NAME}
podman rm -f ${DOWNLINKER_NAME}

podman volume rm ${STORAGE_VOL}

podman rmi --all --force

## Create Volume
podman volume create ${STORAGE_VOL}

## IMAGE SENSOR
SENSOR_PORT=8081
SENSOR_IMAGE=quay.io/rhnspdev/groundbreaker-sensor:${CURRENT_TAG}

echo "Starting ${SENSOR_NAME}"
podman run --name ${SENSOR_NAME} -d \
	-p ${SENSOR_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	${SENSOR_IMAGE}

## IMAGE PROCESSOR
PROCESSOR_PORT=8082
PROCESSOR_IMAGE=quay.io/rhnspdev/groundbreaker-processor:${CURRENT_TAG}

echo "Starting ${PROCESSOR_NAME}"
podman run --name ${PROCESSOR_NAME} -d \
	-p ${PROCESSOR_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	${PROCESSOR_IMAGE}

## IMAGE DOWNLINKER
DOWNLINKER_PORT=8083
DOWNLINKER_IMAGE=quay.io/rhnspdev/groundbreaker-downlinker:${CURRENT_TAG}

echo "Starting ${DOWNLINKER_NAME}"
podman run --name ${DOWNLINKER_NAME} -d \
	-p ${DOWNLINKER_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	-e "FACILITY_A=${FACILITY_A}" \
	-e "FACILITY_B=${FACILITY_B}" \
	${DOWNLINKER_IMAGE}