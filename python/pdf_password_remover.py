import os
import pikepdf
import logging
import coloredlogs

# Import PasswordError from pikepdf
from pikepdf import PasswordError

#CHANGE PASSWORD HERE
pdf_password = "0"

#Logs to scriptName.log
scriptName = os.path.basename(__file__)
logging.basicConfig(level = logging.DEBUG,
                    filename = scriptName + ".log",
                    filemode = "a",
                    encoding = 'utf-8',
                    format = '[%(asctime)s] [%(levelname)s] %(message)s')

#Logs into console
mylogs = logging.getLogger(__name__)
stream = logging.StreamHandler()
mylogs.addHandler(stream)
coloredlogs.install(level=logging.DEBUG, 
                    logger=mylogs,
                    fmt='[%(asctime)s] [%(levelname)s] %(message)s')

rootdir = os.getcwd()
nb = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".pdf"):
            nb += 1
            mylogs.info(f"{nb}) File processing : {file} ({filepath})")
            #Check if the PDF is password locked
            try: 
                pdf = pikepdf.open(filepath)
                mylogs.info(f"{file} isn't locked with a password")
            except PasswordError:
                #If locked, try to unlock with password
                try:
                    pdf = pikepdf.open(filepath, password=pdf_password, allow_overwriting_input=True)
                    pdf.save(filepath)
                    mylogs.info(f"Successfully removed password on {file}")
                except PasswordError:
                    mylogs.error(f"Bad password for {file}")
                except Exception as e:
                    mylogs.error(f"Failed to remove password on {file}: {str(e)}")

# Replace Windows-specific pause with a cross-platform alternative
input("Press Enter to continue...")