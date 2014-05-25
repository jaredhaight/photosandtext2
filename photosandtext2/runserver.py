import os
import sys
sys.path.append(os.getcwd())
print os.getcwd()
from photosandtext2 import app
from photosandtext2 import views

if __name__ == "__main__":
    app.run()