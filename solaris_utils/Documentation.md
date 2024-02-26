## Kitbash Convert

### Problem: 
Kitbash Cargo's Houdini 20.0 (beta) importer brings in 50+ shaders with no connection when brought into a Solaris context. Fortunately they are MaterialX based shaders <3 and work with a variety of renderers.

---
### Solution: 
A script that copys shaders over to Solaris context, and sets them as renderable. Then links them correctly with the sop imported geometry. It keeps the hierachy neat under the unique name of geometry. A cache USD can be added in the future for full USD benefits.  
