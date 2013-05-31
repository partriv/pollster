DEBUG = False

HOST_NAME = "http://pollstruck.com:8000/"
PROJECT_DIR = "L:/eclipse_ws/pollster/"

FONTS_DIR = PROJECT_DIR + "fonts/"
MEDIA_ROOT = PROJECT_DIR + "resources/"

IMAGES_ROOT = MEDIA_ROOT + "i/"
CAPTCHA_IMAGES_ROOT = IMAGES_ROOT + "captchas/"
MEDIA_URL = HOST_NAME

DATABASE_NAME = 'pollster'
DATABASE_USER = 'pollster'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = '3306'

POLL_FILES_URL = "/poll-files/"
POLL_FILES_THUMBS_VIEW = "view_thumb/"
POLL_FILES_THUMBS_HOME = "home_thumb/"
UPLOAD_POLL_FILES_PATH = "L:/eclipse_ws/pollster/resources" + POLL_FILES_URL

USER_FILES_URL = "/user-files/"
USER_FILES_THUMBS_BIG = "big_thumb/"
USER_FILES_THUMBS_MEDIUM = "medium_thumb/"
USER_FILES_THUMBS_SMALL = "small_thumb/"
USER_FILES_THUMBS_TINY = "tiny_thumb/"
UPLOAD_USER_PIC_PATH = "L:/eclipse_ws/pollster/resources" + USER_FILES_URL


EMAIL_HOST = "localhost"
EMAIL_PORT = "1025"
#EMAIL_HOST_USER = ""
#EMAIL_HOST_PASSWORD = ""


TEMPLATE_DIRS = ("L:/eclipse_ws/pollster/com/pollster/templates",)

USE_DJANGO_TOOL_BAR = False 

LOG_FILE = "l:/pollster/etc/log.txt"

COOKIE_DOMAIN =".pollstruck.com"