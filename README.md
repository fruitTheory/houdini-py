Houdini
---
A repo for storing houdini scripts - currently: 
- Kitbash  to Solaris 
- Textures to MaterialX HDA
- Megascans toolset
- Colorspace converter

### Utility 

- Generalized ui Class
- Node class wrapper

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