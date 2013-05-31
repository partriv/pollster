'''
Created on Mar 11, 2009

@author: par
'''

from pollster.utils.string import StringUtils
from PIL import Image
from random import randint
from pollster.consts import consts
import logging
import os

class FileUtils():
    
    @staticmethod
    def uploadFile(file, upload_path=None, thumbnails=None):
        uploadPath = upload_path
        uploadPath = StringUtils.addTrailingSlash(uploadPath)
        uploadPath += file.name.lower()
        uploadPath = FileUtils.getUniqueFileName(uploadPath)
        
        # get extension
        ext = uploadPath[uploadPath.rfind('.'):]
        #pathtupe ROCKS
        pathTuple = os.path.split(uploadPath)

        # check whitelists!
        if consts.IMAGES_WHITE_LIST.count(ext.lower()) > 0 or consts.OTHER_FILES_WHITE_LIST.count(ext.lower()) > 0:
            
            # write file
            destination = open(uploadPath, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

            # if it's an image let's make a thumbnail YAY!!!!!!!!!
            if consts.IMAGES_WHITE_LIST.count(ext) > 0:
                for path, width, height in thumbnails:
                    thumbPath = pathTuple[0] + "/" + path + pathTuple[1]

                    # create thumbnails
                    img = Image.open(uploadPath)
                    img.thumbnail((width, height), Image.ANTIALIAS)
                    img.save(thumbPath)
                                
        else:
            logging.getLogger("FileUtils").warning("invalid file type attempting to be uploaded: " + str(ext))
            return None
            
        return pathTuple[1]
    
    @staticmethod
    def getUniqueFileName(filepath):
        path = filepath[0:filepath.rfind('.')]
        ext = filepath[filepath.rfind('.'):]        
        path += str(randint(0,999999))
        filepath = path + ext
        if os.path.exists(filepath):
            return FileUtils.getUniqueFileName(filepath)
        else:
            return filepath