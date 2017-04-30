import logging
import picamera
from gpiozero import MotionSensor
from datetime import datetime
from os import rename

logger = logging.getLogger(__name__)


class RpiCamera:
    def __init__(self, video_dir):
        self.video_dir = video_dir
        self.pir = MotionSensor(4)
        self.camera = picamera.PiCamera()
        self.stream = picamera.PiCameraCircularIO(self.camera, seconds=10)
        self.camera.start_recording(self.stream, format='h264')
        logger.info('Initiated RpiCamera with video directory being [%s]' % self.video_dir)

    def motion_detected(self):
        return self.pir.motion_detected

    def write_buffer_to_disk(self):
        file_name = self.video_dir + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + '.h264'
        temp_file_name = file_name + '.tmp'
        self.stream.copy_to(temp_file_name)
        rename(temp_file_name, file_name)

    def run(self):
        motion_in_progress = False
        try:
            while 1:
                self.camera.wait_recording(1)
                if self.motion_detected():
                    logger.info('ALERT!!! Motion detected :O')
                    motion_in_progress = True
                    # TODO Maybe snap a photo?
                    # TODO And surely send a notification of some sort...
                    self.write_buffer_to_disk()
                    self.camera.wait_recording(5)
                else:
                    if motion_in_progress:
                        logger.info('Back to normal!')
                        self.write_buffer_to_disk()
                        motion_in_progress = False
                    logger.info('No motion detected... you can relax!')
        finally:
            self.camera.stop_recording()
