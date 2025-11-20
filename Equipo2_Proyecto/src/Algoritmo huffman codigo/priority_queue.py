def delete(q):
    final_node = min(q, key=lambda node: node.frecuency)
    q.remove(final_node)
    return final_node
