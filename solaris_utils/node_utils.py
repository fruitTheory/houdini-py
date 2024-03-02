import hou


# May not be used, only develop further if reusing same stuff too much
class NodeUtils:

    def create_nodes(self, _context, _node_to_create, _node_name):

        context = _context
        node_to_create = _node_to_create
        node_name = _node_name
  
        created_node = context.createNode(node_to_create, node_name)

        return created_node