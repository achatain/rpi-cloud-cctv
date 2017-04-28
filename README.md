Raspberry Pi Cloud CCTV
=========================

https://github.com/achatain/rpi-cloud-cctv

## What is it?

A homemade CCTV based on a Raspberry Pi, its camera module and a PIR (Passive Infrared) motion sensor.

## Notes for installation

- create an env variable *GOOGLE_APPLICATION_CREDENTIALS* pointing to a json keyfile with Google Cloud Storage admin permission
- create an env variable *RPI_CLOUD_CCTV_BUCKET*
- create an env variable *RPI_CLOUD_CCTV_VIDEO_DIR* with trailing file separator
- create a dedicated user who owns and launches the app
- more to come ...