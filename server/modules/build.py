import os

os.chdir('scikit-image')
os.system('git' + " pull")
os.system('pip3 install' + ' -e .')
