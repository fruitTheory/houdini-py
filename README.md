A repo for storing houdini scripts - currently working on a kitbash to solaris setup. 

---
### Running from shelf button  
from importlib import reload  
from solaris_utils import solaris_script

reload(solaris_script)  
solaris_script.main()

---
### Setup vscode
To work with hou library intellisense in vscode, must have python extensions installed and use the hython interpreter included in the Houdini bin folder.
