import os 
if not os.path.exists(os.path.join(os.getcwd(), "fileSpliter")):
        os.makedirs("fileSpliter")
else: 
        os.rmdir(os.path.join(os.getcwd(), "fileSpliter"))