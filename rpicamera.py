# https://github.com/achatain/rpi-cloud-cctv
#
# Copyright (C) 2017 Antoine Chatain (achatain [at] outlook [dot] com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import picamera
from gpiozero import MotionSensor
from datetime import datetime
from os import rename

logger = logging.getLogger(__name__)


class RpiCamera(object):
    """
    Class for controlling the Raspberry Pi Camera based on a PIR motion sensor input.
    Hold a ring buffer of 10 seconds of video footage. Whenever motion is detected, the buffer content is written
    to the disk, then 5 seconds long video are recorded and written to the disk until motion stops.
    """

    def __init__(self, video_dir='/home/pi/Videos', pin=4):
        """
        :param str video_dir:
            The path to the directory where video files are to be saved.
        
        :param int pin:
            The GPIO pin which the sensor is attached to.
        """
        self.video_dir = video_dir
        self.pir = MotionSensor(pin)
        self.camera = picamera.PiCamera()
        self.stream = picamera.PiCameraCircularIO(self.camera, seconds=10)
        self.camera.start_recording(self.stream, format='h264')
        logger.info('Initiated RpiCamera with video directory being [%s]' % self.video_dir)

    def motion_detected(self):
        return self.pir.motion_detected

    def build_timestamped_file_name(self):
        return self.video_dir + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + '.h264'

    def write_buffer_to_disk(self):
        file_name = self.build_timestamped_file_name()
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
                    else:
                        logger.debug('No motion detected... you can relax!')
        finally:
            self.camera.stop_recording()
