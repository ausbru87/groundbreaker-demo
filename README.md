# Groundbreaker Demo

## Deployment Fabrics
- AWS
- Azure
- SNO (HPE EL8K)
- SNO (HPE EL8K)
- RHEL8.8 (HP EL8K)


## Deployments

### EdgeDevice
- Represents the low SWAP device edge running podman -- future will look at RHDE & MicroShift
- Components
  - image_sensor
    - Generates images with and without ships in them (ships = black rectangle)
  - image_processor
    - detects_ships in the images and if it does not contain a ship it discards the image
  - image_downlinker
    - downlinks all remaining images to the online edgefacility
    - monitors the API of the edgefacility-a and edgefacility-b and will pause and switch downlink locations if one is lost

### EdgeFacility
- Represents a remote edge processing facility with a minimal number of servers -- currently running Single Node OpenShift on two single blade servers
- Components
  - image_receiver
    - receives and stores the images downlinked from the edgedevice
  - image_processor
    - looks at the downlinked images and chips ships in the images to reduce the image data needing to be sent back to corefacility
  - image_forwarder
    - forwards all the chips to the corefacility

### CoreFacility
- Represents the core processing facilities that are used to do the heavy lifting. -- This is AWS and Azure for the demo
- Components
  - image_receiver
    - receives and stores the images that were forwarded from the edgefacility
  - image_processor
    - looks at the chips and wraps the ship in a green box and labels it with the word SHIP and stores them on the volume
  - s3_image_uploader
    - reads the image data iin the volume and copies it to an S3 bucket for future use or archive


