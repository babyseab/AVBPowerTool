'''
ConfigManager provides useful functions for config management, including import, export and delete.
Batch operation are also supported.

Config files are placed in child folders of `configSet` and `key` folders.

This module will export zip files with flag file as exported config.

When using batch export, it will create a "super" zip that contains small zip packages.

:todo: reconstruct import part to avoid using CLI rename function.
'''

import os, zipfile, time, shutil
import LogUtils

class ConfigManager:

    TAG = "ConfigManager"

    def __init__(self, logger = None) -> None:
        if not logger:
            self.myLogger = LogUtils.LogUtils()
            self.myLogger.log("W", "Logger not given, created an instance just now.", "ConfigManager")
        else:
            self.myLogger = logger
        self.myLogger.log("I", "Instance of ConfigManager successfully created.", "ConfigManager")

    def saveAsPersistentConfig(self, configName) -> bool:
        try:
            for i in os.listdir("./currentConfigs/" + configName):
                shutil.copy("./currentConfigs",
                            "./configSet/" + configName + "/" + i)
            for i in os.listdir("./key/currentKeySet/" + configName):
                shutil.copy("./key/currentKeySet",
                            "./key/" + configName + "/" + i)
            return True
        except Exception as e:
            self.myLogger.log("W", "Failed to save config: ", self.TAG)
            self.myLogger.log("W", str(e), self.TAG)
            return False

    def setConfigActive(self, configName) -> bool:
        try:
            self.setConfigDeactivate()
            for i in os.listdir("./configSet/" + configName):
                shutil.copy("./configSet/" + configName + "/" + i,
                            "./currentConfigs")
            for i in os.listdir("./key/" + configName):
                shutil.copy("./key/" + configName + "/" + i,
                            "./key/currentKeySet")
            return True
        except Exception as e:
            self.myLogger.log("W", "Failed to switch config " + configName + " active: ", self.TAG)
            self.myLogger.log("W", str(e), self.TAG)
            return False
    
    def setConfigDeactivate(self) -> bool:
        try:
            for i in os.listdir("./currentConfigs"):
                os.remove("./currentConfigs/" + i)
            for i in os.listdir("./key/currentKeySet"):
                os.remove("./key/currentKeySet/" + i)
            return True
        except Exception as e:
            self.myLogger.log("W", "Failed to deactivate current config: ", self.TAG)
            self.myLogger.log("W", str(e), self.TAG)
            return False
            

    def removeSingleConfig(self, configName) -> bool:
        try:
            shutil.rmtree("./configSet/" + configName)
            shutil.rmtree("./key/" + configName)
            return True
        except Exception as e:
            self.myLogger.log("W", "Failed to remove config: " + configName, self.TAG)
            self.myLogger.log("W", str(e), self.TAG)
            return False

    def batchImportConfig(self, importFromDir = "./", importFromFileName = "myBatchConfig.zip"):
        EXTRACT_ZIP_TO = "./temp/extractedConfigZips"
        with zipfile.ZipFile(importFromDir + importFromFileName, 'r') as myZip:
            fileInfoList = myZip.infolist()
            fileNameList = []
            isBatchConfigValid = False
            isSingleConfigFlagExist = False
            for i in fileInfoList:
                if i.filename == "BATCH_CONFIG_AVBPOWERTOOL":
                    isBatchConfigValid = True
                elif i.filename == "this_is_a_config_file_of_avbpowertool":
                    isSingleConfigFlagExist = True 
                else:
                    fileNameList.append(i.filename)
            if isBatchConfigValid:
                self.myLogger.log("V", "Valid batch config.", self.TAG)
            else:
                self.myLogger.log("W", "Invalid zip file!", self.TAG)
                if isSingleConfigFlagExist:
                    self.myLogger.log("W", "Attempting to import a single config zip.", self.TAG)
                return
            myZip.extractall(path = EXTRACT_ZIP_TO)
            configList = os.listdir(EXTRACT_ZIP_TO)
            os.remove(EXTRACT_ZIP_TO + "/" + "BATCH_CONFIG_AVBPOWERTOOL")
            for i in configList:
                self.importSingleConfig(importFromDir = EXTRACT_ZIP_TO,
                                        importFromFileName = i)
            shutil.rmtree(EXTRACT_ZIP_TO)
    
    def batchExportConfig(self,
                          exportToDir = "./",
                          exportToFileName = "myBatchConfig.zip",
                          selectedConfigs = ["current"]):
        SINGLE_CONFIG_EXPORT_TO = "./temp/exportSingleConfigZips"
        with zipfile.ZipFile(exportToDir + exportToFileName, 'w') as myZip:
            for i in selectedConfigs:
                self.exportSingleConfig(exportConfigFolderName = i,
                                        exportToDir = SINGLE_CONFIG_EXPORT_TO,
                                        exportToFileName = i + ".zip")
            for root, dirs, fileNames in os.walk(SINGLE_CONFIG_EXPORT_TO):
                for fileName in fileNames:
                    filePath = os.path.join(root, fileName)
                    arcName = os.path.relpath(filePath, os.path.dirname(i))
                    myZip.write(filePath, arcName)
                    self.myLogger.log("V", filePath, self.TAG)
            with open(SINGLE_CONFIG_EXPORT_TO + "/" + "BATCH_CONFIG_AVBPOWERTOOL", "w") as myFile:
                myFile.write("Batch config of AVBPowerTool.")
            myZip.write(SINGLE_CONFIG_EXPORT_TO + "/" + "BATCH_CONFIG_AVBPOWERTOOL")
        shutil.rmtree(SINGLE_CONFIG_EXPORT_TO)

    def importSingleConfig(self,
                           importFromDir = "./",
                           importFromFileName = "myConfig.zip"):
        '''
        Import a *valid* config zip file.
        
        It will require a rename if flag file `RENAME_REQUIRED` is found in archive.

        :param importFromDir: Where should the method find config archive.
        :param importFromFileName: Which config file should the method use.
        :return: None
        '''

        EXTRACT_TO = "./temp/unZippedConfig"
        with zipfile.ZipFile(importFromDir + importFromFileName, 'r') as myZip:
            fileInfoList = myZip.infolist()
            fileNameList = []
            renameBeforeImport = False
            isValidConfig = False
            for i in fileInfoList:
                if i.filename == "RENAME_REQUIRED":
                    renameBeforeImport = True
                elif i.filename == "this_is_a_config_file_of_avbpowertool":
                    isValidConfig = True
                else:
                    fileNameList.append(i.filename)
            if not isValidConfig:
                self.myLogger.log("W", "Invalid zip file.", self.TAG)
                return
            else:
                self.myLogger.log("V", "Config is valid.", self.TAG)
            configName = importFromFileName.strip(".zip")
            if renameBeforeImport:
                configName = self.__getNewConfigName()
            try:
                shutil.rmtree(EXTRACT_TO)
            except:
                pass
            myZip.extractall(path = EXTRACT_TO)
            try:
                os.remove(EXTRACT_TO + "/" + "RENAME_REQUIRED")
                os.remove(EXTRACT_TO + "/" + "this_is_a_config_file_of_avbpowertool")
            except:
                pass
            self.myLogger.log("V", "Successfully extracted config to temporary folder.", self.TAG)
            # default configs will be extracted to ./temp/unZippedConfig/currentConfigs
            # and ./temp/unZippedConfig/currentKeySet
            if renameBeforeImport:
                # rename one, copy one at once, and then remove.
                # config folder goes first.
                os.rename(EXTRACT_TO + "/" + "currentConfigs",
                          EXTRACT_TO + "/" + configName)
                shutil.copytree(EXTRACT_TO + "/" + configName,
                                "./configSet/" + configName)
                shutil.rmtree(EXTRACT_TO + "/" + configName)
                # then process keySet folder
                os.rename(EXTRACT_TO + "/" + "currentKeySet",
                          EXTRACT_TO + "/" + configName)
                shutil.copytree(EXTRACT_TO + "/" + configName,
                                "./key/" + configName)
                shutil.rmtree(EXTRACT_TO + "/" + configName)
            else:
                # check the availability of config name first
                if not self.__isConfigAvailable(configName):
                    # if not available, request a new config name.
                    # call to self.__getNewConfigName() should be avoided at frontend to avoid troubles when switching to GUI.
                    tmpFileName = os.listdir("./temp/unZippedConfig/configSet")[0]
                    configName = self.__getNewConfigName()
                    # rename one, copy one at once, and then remove.
                    # config folder goes first.
                    os.rename(EXTRACT_TO + "/configSet/" + tmpFileName,
                            EXTRACT_TO + "/configSet/" + configName)
                    shutil.copytree(EXTRACT_TO + "/configSet/" + configName,
                                    "./configSet/" + configName)
                    shutil.rmtree(EXTRACT_TO + "/configSet/" + configName)
                    # then process keySet folder
                    os.rename(EXTRACT_TO + "/key/" + tmpFileName,
                            EXTRACT_TO + "/key/" + configName)
                    shutil.copytree(EXTRACT_TO + "/key/" + configName,
                                    "./key/" + configName)
                    shutil.rmtree(EXTRACT_TO + "/key/" + configName)
                else:
                    # if available, copy them directly.
                    # we should keep this control flow only in the final version.
                    shutil.copytree(EXTRACT_TO + "/configSet/" + configName,
                                    "./configSet/" + configName)
                    shutil.rmtree(EXTRACT_TO + "/configSet/" + configName)
                    shutil.copytree(EXTRACT_TO + "/key/" + configName,
                                    "./key/" + configName)
                    shutil.rmtree(EXTRACT_TO + "/key/" + configName)
            self.myLogger.log("V", "Successfully copied config to target folder.", self.TAG)
        shutil.rmtree(EXTRACT_TO)
        self.myLogger.log("V", "Successfully removed temp folder.", self.TAG)

    def __isConfigAvailable(self, configName : str):
        '''
        __isConfigAvailable checks name of configs to avoid overriding existing files.
        
        :param configName: the name of your config.
        :return: True when config name available, False when config name is taken by another existing config.
        '''
        configNameInUse = ["currentConfigs", "current"]
        for folderName in os.listdir("./configSet"):
            configNameInUse.append(folderName)
        return not configName in configNameInUse

    def __getNewConfigName(self):
        '''
        Private method to get a new config name when rename is required during import.
        
        Will let user type another name when attempting to use name `currentConfigs` and provide a autogenerated name after 3 unsuccessful attempts.

        :return: Config name string
        '''
        print("To avoid overriding existing files, please provide another config name to continue import process.")
        count = 0
        while count < 3:
            newConfigName = input("New config name: ")
            if self.__isConfigAvailable(newConfigName) and len(newConfigName) > 0:
                return newConfigName
            else:
                print("Illegal config name, try another name instead.")
                count += 1
        else:
            newConfigName = "AutoRenamedConfig_" + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
            print("Using a autogenerated config name to complete import: " + newConfigName)
            return newConfigName

    def exportSingleConfig(self,
                           exportConfigFolderName = "current",
                           exportToDir = "./",
                           exportToFileName = "myConfig.zip") -> None:
        """
        Export a single config as a zip file (with *valid* flag) to the directory you assigned.
        
        In the archive exported you will find a file named `this_is_a_config_file_of_avbpowertool`, which indicates the validity of this file.
        
        If you decided to let this method export the config that is used currently, it will additionally add a flag file named `RENAME_REQUIRED` to tell the program that we need a rename before importing it to avoid overriding config.
        (recommended to let users rename it before exporting in order to avoid forgetting the use of this config.)

        :param exportConfigFolderName: Determine which config folder you want to export. Set to `current` (case-sensitive) or ignore it will use folder `currentConfigs`.
        :param exportToDir: Determine where you want to save the exported zip file, keep it empty if you want to save it to the project's **root** folder.
        :param exportToFileName: Determine the filename of zip file, default value is `myConfig.zip`
        :return: None
        :raise FileNotFoundError: Config folder assigned not exist.
        """
        
        if exportConfigFolderName == "current":
            foldersRequired = ("./currentConfigs", "./key/currentKeySet")
        else:
            foldersRequired = ("./configSet/" + exportConfigFolderName,
                               "./key/" + exportConfigFolderName)
        
        if not exportToFileName.endswith(".zip"):
            self.myLogger.log("W", "Attempting to use other file extension name while exporting config.", self.TAG)

        if (not os.path.exists(foldersRequired[0])) or (not os.path.exists(foldersRequired[1])):
            raise FileNotFoundError("Assigning a config folder that does not exist.")
        

        with zipfile.ZipFile(exportToDir + exportToFileName, 'w') as myZip:
            for i in foldersRequired:
                for root, dirs, fileNames in os.walk(i):
                    for fileName in fileNames:
                        filePath = os.path.join(root, fileName)
                        arcName = os.path.relpath(filePath, os.path.dirname(i))
                        myZip.write(filePath, arcName)
                        self.myLogger.log("V", filePath, self.TAG)
            with open("this_is_a_config_file_of_avbpowertool", "w") as myTempFile:
                myTempFile.write("This is a file that indicates the zip archive is a valid config file of AVBPowerTool.")
            myZip.write("this_is_a_config_file_of_avbpowertool")
            os.remove("this_is_a_config_file_of_avbpowertool")
            if exportConfigFolderName == "current":
                with open("RENAME_REQUIRED", "w") as myTempFile:
                    myTempFile.write("Please rename this config before import.")
                myZip.write("RENAME_REQUIRED")
                os.remove("RENAME_REQUIRED")

if __name__ == "__main__":
    myConfigManager = ConfigManager()
    myConfigManager.importSingleConfig()