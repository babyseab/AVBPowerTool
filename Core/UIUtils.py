import os
import LogUtils
import ConfigManager


class UIUtils:

    def __init__(self, logger=None) -> None:
        self.TAG = "UIUtils"
        if logger is None:
            self.myLogger = LogUtils.LogUtils(shouldAttachTime=True)
        else:
            self.myLogger = logger
        self.myConfigManager = ConfigManager.ConfigManager(
            logger=self.myLogger)
        self.myLogger.log(
            "I", "Successfully created UIUtils instance.", self.TAG)

    def selectFileUI(self, extensionName=".zip"):
        """
        Provide filename of zip archive selected. Will return None if user cancels.
        """
        print("Place zip file under root directory and press Enter to continue.")
        self.pressEnterToContinue()
        rootDir = os.getcwd()
        fileCanBeSelected = []
        for i in os.listdir(rootDir):
            if i.endswith(extensionName):
                fileCanBeSelected.append(i)
        for i in range(len(fileCanBeSelected)):
            print(i + 1, fileCanBeSelected[i])
        print("Select a file with number. Enter -1 to cancel.")
        while 1:
            myInput = input("Your choice: ")
            try:
                inputNumber = int(myInput)
                if 0 < inputNumber <= len(fileCanBeSelected):
                    print("Select file: %s" %
                          (fileCanBeSelected[inputNumber - 1]))
                    break
                elif inputNumber == -1:
                    return None
                else:
                    raise IndexError
            except Exception as e:
                print("Invalid input, try again.")
                self.myLogger.log(
                    "W", "Invalid input when selecting file: " + repr(e), self.TAG)
        if self.confirmOperation(prompt="Select this file?"):
            return fileCanBeSelected[inputNumber - 1]
        else:
            return None

    def pressEnterToContinue(self):
        input("Press Enter to continue.")

    def confirmOperation(self, prompt="Confirm operation?") -> bool:
        try:
            if input(prompt + " [y/N]: ").lower() == "y":
                return True
            else:
                return False
        except:
            return False

    def selectConfigUI(self):
        configNames = self.myConfigManager.getAllConfigs()
        for i in range(len(configNames)):
            print(i + 1, configNames[i])
        print("Select a config with number. Enter -1 to cancel.")
        while 1:
            myInput = input("Your choice: ")
            try:
                inputNumber = int(myInput)
                if 0 < inputNumber <= len(configNames):
                    print("Import file: %s" % (configNames[inputNumber - 1]))
                    break
                elif inputNumber == -1:
                    return None
                else:
                    raise IndexError
            except Exception as e:
                print("Invalid input, try again.")
                self.myLogger.log(
                    "W", "Invalid input when selecting config: " + repr(e), self.TAG)
        print("Select this config? [y/N]", end=" ")
        if input().upper() == "Y":
            return configNames[inputNumber - 1]
        else:
            return None
