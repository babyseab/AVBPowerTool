import subprocess
import os

for i in os.listdir("F:\\testImages"):
    result = subprocess.run(["python",
                             "F:\\GitHub\\AVBPowerTool\\Core\\avbtool.py",
                             "info_image",
                             "--image",
                             "F:\\testImages\\" + i], capture_output = True, text = True)
    print(result.stdout)