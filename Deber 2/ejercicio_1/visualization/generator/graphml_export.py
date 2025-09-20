import networkx as nx

def compute_tree_positions(parent_dict, x_spacing=200, y_spacing=120):
    # Construir mapa padres -> hijos y asegurar que cada nodo tiene una entrada
    children_map = {}
    for node in parent_dict:
        children_map.setdefault(node, [])
    for child, parent in parent_dict.items():
        if parent is not None:
            children_map.setdefault(parent, []).append(child)

    # Encontrar raíces (nodos cuyo parent es None)
    roots = [node for node, parent in parent_dict.items() if parent is None]
    if not roots:
        # Si no hay root explícito, elegir cualquier nodo como raíz (robustez)
        roots = [next(iter(parent_dict.keys()))]

    # Calcular profundidad para cada nodo (robusto ante parent faltante)
    def calc_depth(node):
        depth = 0
        curr = node
        while True:
            parent = parent_dict.get(curr)
            if parent is None:
                break
            curr = parent
            depth += 1
        return depth
    depth_map = {node: calc_depth(node) for node in parent_dict}

    # Lista de hojas (nodos sin hijos)
    leaves = [n for n, childs in children_map.items() if not childs]
    leaf_count = len(leaves)

    # Guardar posiciones x temporales (antes de centrar)
    node_x = {}

    # Índice de hoja (mutable para cerrar en nested function)
    next_leaf = [0]  # usar lista para mutabilidad en closure

    # Post-order traversal: asigna x a hojas cuando se encuentran, y a padres como promedio
    def assign_x(node):
        if node in node_x:
            return node_x[node]
        children = children_map.get(node, [])
        if not children:
            # Es hoja: asignarle la siguiente x disponible
            idx = next_leaf[0]
            node_x[node] = idx * x_spacing
            next_leaf[0] += 1
            return node_x[node]
        # No es hoja: procesar hijos primero
        xs = [assign_x(child) for child in children]
        # centrar entre hijos
        node_x[node] = (min(xs) + max(xs)) / 2.0
        return node_x[node]

    # Llamar assign_x para cada raíz en orden (asegura que todas las ramas se recorran)
    for r in roots:
        assign_x(r)

    # Si hay nodos que no pertenecen a ninguna rama recorrida (por seguridad), asignarlos también
    for node in parent_dict:
        if node not in node_x:
            # si no tiene hijos, lo tratamos como hoja; si tiene hijos, forzamos cálculo
            if not children_map.get(node):
                idx = next_leaf[0]
                node_x[node] = idx * x_spacing
                next_leaf[0] += 1
            else:
                # forzar cálculo de sus hijos (defensivo)
                assign_x(node)

    # Centrar horizontalmente el conjunto de hojas alrededor de x=0
    if leaf_count > 0:
        total_width = (leaf_count - 1) * x_spacing
        center_offset = total_width / 2.0
    else:
        center_offset = 0.0

    # Construir posiciones finales (x - center_offset, y = depth * y_spacing)
    node_pos = {}
    for node in parent_dict:
        x = node_x[node] - center_offset
        y = depth_map[node] * y_spacing
        node_pos[node] = (x, y)

    return node_pos

def export_search_tree(parent_dict, solution_path, filename="bfs_tree.graphml"):
    G = nx.DiGraph()

    # Definir colores como variables
    extra_color = "#8A9CEC"
    solution_color = "#664197"

    # Calcular posiciones centradas en forma de pirámide
    node_pos = compute_tree_positions(parent_dict)

    # Convertir el camino solución a set para marcar rápido
    solution_set = set(solution_path)

    # Añadir nodos con atributos
    for node in parent_dict:
        node_id = str(node.tiles)
        x, y = node_pos[node]
        color = solution_color if node in solution_set else extra_color
        G.add_node(node_id, x=x, y=y, color=color, label=node_id)

    # Añadir aristas y marcar las del camino solución
    solution_edges = set()
    for i in range(len(solution_path) - 1):
        src = str(solution_path[i].tiles)
        dst = str(solution_path[i + 1].tiles)
        solution_edges.add((src, dst))

    for child, parent in parent_dict.items():
        if parent is None:
            continue
        src = str(parent.tiles)
        dst = str(child.tiles)
        edge_color = solution_color if (src, dst) in solution_edges else extra_color
        G.add_edge(src, dst, color=edge_color)

    import os
    export_dir = os.path.join('Deber 2', 'ejercicio_1', 'visualization', 'export')
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, filename)
    nx.write_graphml(G, export_path)
    # Mostrar solo la ruta relativa desde visualization/export/
    displayed_path = os.path.join('visualization', 'export', filename)
    print(f"\nÁrbol exportado en: '{displayed_path}'")