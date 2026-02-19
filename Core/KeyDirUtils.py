import os, subprocess, LogUtils

class KeyDirUtils:

    def __init__(self, logger = None) -> None:
        if not logger:
            self.myLogger = LogUtils.LogUtils()
            self.myLogger.log("W", "Logger not given, created an instance just now.", "KeyDirUtils")
        else:
            self.myLogger = logger
        self.myLogger.log("I", "Instance of KeyDirUtils successfully created.", "KeyDirUtils")
    def generateKeyFileCache(self, keyFileDir = "./key/currentKeySet", cacheFileName = "keyCache.cache"):
        try:
            os.remove(keyFileDir + cacheFileName)
        except:
            pass
        try:
            with open(keyFileDir + cacheFileName, "w+") as myFile:
                for root, dirs, fileNames in os.walk(keyFileDir):
                    for fileName in fileNames:
                        if fileName.endswith(".pem"):
                            self.myLogger.log("V", "Key file detected:" + fileName)
                            myFile.write(fileName + ", " + self.__getSha1(keyFileDir, fileName) + "\n")
        except:
            pass
    
    def __getSha1(self, keyFileDir, fileName):
        if os.name == 'nt':
            subprocess.run(["py",
                            "./avbtool.py",
                            "extract_public_key",
                            "--key",
                            keyFileDir + fileName,
                            "--output",
                            keyFileDir + fileName.strip(".pem") + "_pub.bin"])
            return subprocess.run(["certutil",
                                   "-hashfile",
                                   keyFileDir + fileName.strip(".pem") + "_pub.bin",
                                   "sha1"],
                                   capture_output = True,
                                   text = True).stdout.split("\n")[1]
        else:
            subprocess.run(["python3",
                            "./avbtool.py",
                            "extract_public_key",
                            "--key",
                            keyFileDir + fileName,
                            "--output",
                            keyFileDir + fileName.strip(".pem") + "_bin.bin"])
            return subprocess.run(["sha1sum",
                                   keyFileDir + fileName.strip(".pem") + "_pub.bin"],
                                   capture_output = True,
                                   text = True).stdout.split("  ")[0]