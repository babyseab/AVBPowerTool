import BaseUI
import os

class ExportConfigUI(BaseUI.BaseUI):

    def customizedInit(self):
        self.TAG = "ExportConfigUI"
        self.customizedFunction = {
            "E" : "Export a selected config",
            "A" : "Batch export configs as an archive",
            "S" : "Batch export configs as single archives",
        }
        self.myConfigManager = self._createInstance(self._importModule("ConfigManager"),
                                                    "ConfigManager",
                                                    self.myLogger)
    
    def callBackEnd(self, functionName: str):
        if functionName == self.customizedFunction["E"]:
            self.__handleSingleExportLogic()
        elif functionName == self.customizedFunction["A"]:
            self._inDevelopmentPlaceHolder()
        elif functionName == self.customizedFunction["S"]:
            self._inDevelopmentPlaceHolder()
    
    def __handleSingleExportLogic(self):
        configName = self.__selectConfigUI()
        if configName is None:
            print("User cancelled operation.")
        else:
            try:
                result = self.myConfigManager.exportSingleConfig(exportConfigFolderName = configName)
                if result:
                    print("Successfully exported selected config %s to root directory as an archive."%(configName))
                else:
                    print("Failed to export config!")
            except FileNotFoundError:
                print("Config folder not found!")
                self.myLogger.log("W",
                                "Config folder not found! Check system settings because config is already guaranteed exist in previous steps.",
                                self.TAG)
        self._pressEnterToContinue()

    def __selectConfigUI(self):
        configNames = self.myConfigManager.getAllConfigs()
        for i in range(len(configNames)):
            print(i + 1, configNames[i])
        print("Select a config with number. Enter -1 to cancel.")
        while 1:
            myInput = input("Your choice: ")
            try:
                inputNumber = int(myInput)
                if 0 < inputNumber <= len(configNames):
                    print("Import file: %s"%(configNames[inputNumber - 1]))
                    break
                elif inputNumber == -1:
                    return None
                else:
                    raise IndexError
            except Exception as e:
                print("Invalid input, try again.")
                self.myLogger.log("W", "Invalid input when selecting config: " + repr(e), self.TAG)
        print("Select this config? [y/N]", end = " ")
        if input().upper() == "Y":
            return configNames[inputNumber - 1]
        else:
            return None