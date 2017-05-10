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
import os
import constants
import sendgrid
import base64
from sendgrid.helpers.mail import *

logger = logging.getLogger(__name__)


class EmailClient(object):
    """
    Client for interacting with SendGrid API v3.
    """

    def __init__(self, default_recipient=None, default_sender=None):
        """
        :param str default_recipient:
            The recipient to be used if no other recipient is provided.
        """
        self.default_recipient = default_recipient if default_recipient is not None \
            else os.getenv(constants.env_email_recipient)
        self.default_sender = default_sender if default_sender is not None \
            else os.getenv(constants.env_email_sender)
        logger.info('Initiated EmailClient with default sender [%s] and default recipient [%s]'
                    % (self.default_sender, self.default_recipient))

    def send(self, subject, body, sender=None, recipient=None, attachment_path=None):
        """
        :param str subject:
            The subject of the email to be sent.

        :param str body:
            The body of the email to be sent.

        :param str sender:
            The sender of the email to be sent.

        :param str recipient:
            The recipient of the email to be sent
        
        :param str attachment_path:
            Path to an image to attach
        """
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get(constants.env_sendgrid_api_key))
        from_email = Email(self.default_sender if sender is None else sender)
        to_email = Email(self.default_recipient if recipient is None else recipient)
        content = Content(constants.email_content_type, body)
        email = Mail(from_email, subject, to_email, content)

        if attachment_path is not None:
            attachment = Attachment()

            with open(attachment_path, 'rb') as image_file:
                data = image_file.read()
                image_file.close()
                data_b64 = base64.b64encode(data)
                attachment.content = data_b64

            parts = attachment_path.split('/')
            attachment.filename = parts[len(parts) - 1].rstrip(constants.file_temp_extension)
            attachment.disposition = constants.email_attachment_disposition
            email.add_attachment(attachment)

        sg.client.mail.send.post(request_body=email.get())
