# -*- coding: utf-8 -*-
import os
class Config():

    APPLICATION_NAME = "PyMemorium"
    PORT = 7777
    PROGRAM_VERSION = "0.1"
    SECRET_KEY = os.urandom(24)
    LOGS_PATH = "D:\\home\\projects\\pymemorium\\logs\\main.log"
    # SOURCE_PATH = "/home/template/Dropbox/notebook"
