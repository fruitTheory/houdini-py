Houdini
---
A repo for storing houdini pipeline scripts - currently: 
- Kitbash to Solaris 
- Textures to MaterialX HDA
- Megascan variations as variants
- Colorspace converter

---

### Running from shelf example  
from importlib import reload  
from solaris_utils import kitbash_convert as kc  
  
reload(kc)  
kit = kc.KitConvert()  
kit.convertAll() or kit.convert('KB3D_AOE')  
  
---
### Setup vscode
To work with hou library intellisense in vscode, install python extensions and use hython interpreter included in the Houdini package.  