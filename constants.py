# Mandatory environment variables
required_envs = {
    'video_dir': 'RPI_CLOUD_CCTV_VIDEO_DIR',
    'gcloud_bucket': 'RPI_CLOUD_CCTV_BUCKET',
    'gcloud_credentials': 'GOOGLE_APPLICATION_CREDENTIALS',
    'sendgrid_api_key': 'SENDGRID_API_KEY',
    'email_recipient': 'RPI_CLOUD_CCTV_EMAIL_RECIPIENT',
    'email_sender': 'RPI_CLOUD_CCTV_EMAIL_SENDER'
}

# Env variables keys
env_video_dir = 'video_dir'
env_gcloud_bucket = 'gcloud_bucket'
env_gcloud_credentials = 'gcloud_credentials'
env_sendgrid_api_key = 'sendgrid_api_key'
env_email_recipient = 'email_recipient'
env_email_sender = 'email_sender'

# Log properties
log_file_name = 'rpicloudcctv.log'
log_format = '%(asctime)s %(levelname)s [%(name)s] %(message)s'

# File properties
file_timestamp_prefix_format = '%Y-%m-%d_%H.%M.%S'
file_temp_extension = '.tmp'
file_video_extension = '.h264'
file_photo_extension = '.jpg'

# Default properties
default_video_dir = '/home/pi/Videos'
default_video_format = 'h264'

# Email properties
email_attachment_disposition = 'attachment'
email_content_type = 'text/html'
