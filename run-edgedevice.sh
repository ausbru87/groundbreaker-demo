## Pre-Run Cleanup
STORAGE_VOL=groundbreaker-storage
SENSOR_NAME=sensor
PROCESSOR_NAME=processor
DOWNLINKER_NAME=downlinker

podman rm -f ${SENSOR_NAME}
podman rm -f ${PROCESSOR_NAME}
podman rm -f ${DOWNLINKER_NAME}

podman volume rm ${STORAGE_VOL}

## Create Volume
podman volume create ${STORAGE_VOL}

## IMAGE SENSOR
SENSOR_PORT=8081
SENSOR_IMAGE=quay.io/rhnspdev/groundbreaker-sensor:latest

echo "Starting ${SENSOR_NAME}"
podman run --name ${SENSOR_NAME} -d \
	-p ${SENSOR_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	${SENSOR_IMAGE}

## IMAGE PROCESSOR
PROCESSOR_PORT=8082
PROCESSOR_IMAGE=quay.io/rhnspdev/groundbreaker-processor:latest

echo "Starting ${PROCESSOR_NAME}"
podman run --name ${PROCESSOR_NAME} -d \
	-p ${PROCESSOR_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	${PROCESSOR_IMAGE}

## IMAGE DOWNLINKER
DOWNLINKER_PORT=8083
DOWNLINKER_IMAGE=quay.io/rhnspdev/groundbreaker-downlinker:latest

echo "Starting ${DOWNLINKER_NAME}"
podman run --name ${DOWNLINKER_NAME} -d \
	-p ${DOWNLINKER_PORT}:8080 \
	-v ${STORAGE_VOL}:/images \
	-e "FACILITY_A=https://imagereceiver-groundbreaker-edgefac1.apps.groundbreaker-edgefac1.rhtps.io" \
	-e "FACILITY_B=https://imagereceiver-groundbreaker-edgefac2.apps.groundbreaker-edgefac2.rhtps.io" \
	${DOWNLINKER_IMAGE}