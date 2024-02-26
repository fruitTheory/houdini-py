A repo for storing houdini scripts - currently contains a kitbash to solaris setup. 

---
### Running from shelf button  
from importlib import reload  
from solaris_utils import kitbash_convert as kc  
  
reload(kc)  
kit = kc.KitConvert()  
kit.convertAll() or kit.convert('KB3D_AOE')  
  
---
### Setup vscode
To work with hou library intellisense in vscode, must have python extensions installed and use the hython interpreter included in the Houdini bin folder.  