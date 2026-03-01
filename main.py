import gradio as gr
import matplotlib.pyplot as plt

# ---------- NODE ----------
class Node:
    def __init__(self, value, low, high):
        self.value = value
        self.low = low
        self.high = high
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

# ---------- TREE LAYOUT ----------
def inorder_layout(node, depth=0, counter=[0]):
    if node is None:
        return
    inorder_layout(node.left, depth+1, counter)
    node.x = counter[0]
    node.y = -depth
    counter[0] += 1
    inorder_layout(node.right, depth+1, counter)

def collect(node, nodes=None, edges=None):
    if nodes is None: nodes = []
    if edges is None: edges = []
    if node:
        nodes.append(node)
        if node.left:
            edges.append((node, node.left))
            collect(node.left, nodes, edges)
        if node.right:
            edges.append((node, node.right))
            collect(node.right, nodes, edges)
    return nodes, edges

# ---------- DRAW ----------
def draw_tree(root, current):
    if root is None:
        return None

    inorder_layout(root, counter=[0])
    nodes, edges = collect(root)

    fig = plt.figure(figsize=(7,5))

    # edges
    for n1, n2 in edges:
        plt.plot(
            [n1.x, n2.x],
            [n1.y, n2.y],
            linewidth=2
        )

    # nodes
    for n in nodes:
        if n == current:
            color = "#2563eb"   # highlight blue
            size = 1600
        else:
            color = "#94a3b8"   # neutral gray
            size = 1200

        plt.scatter(
            n.x, n.y,
            s=size,
            zorder=3
        )

        plt.text(
            n.x, n.y,
            str(n.value),
            ha="center",
            va="center",
            fontsize=12,
            weight="bold",
            color="black"
        )

    plt.axis("off")
    plt.margins(0.2)
    return fig

# ---------- GAME ----------
def start_game():
    low, high = 0, 10
    mid = (low + high)//2
    root = Node(mid, low, high)
    return root, root, f"Is your number greater than {mid}?", draw_tree(root, root)

def step(is_greater, root, current):
    low, high = current.low, current.high
    mid = current.value

    if is_greater:
        low = mid + 1
    else:
        high = mid - 1

    if low > high:
        return root, current, "Inconsistent answers", draw_tree(root, current)

    if low == high:
        node = Node(low, low, high)
        if is_greater:
            current.right = node
        else:
            current.left = node
        return root, node, f"🎯 Your number is {low}", draw_tree(root, node)

    new_mid = (low + high)//2
    node = Node(new_mid, low, high)

    if is_greater:
        current.right = node
    else:
        current.left = node

    return root, node, f"Is your number greater than {new_mid}?", draw_tree(root, node)

# ---------- UI ----------
with gr.Blocks() as app:

    gr.Markdown("## 🌳 Binary Search Tree Visualizer")

    state_root = gr.State()
    state_current = gr.State()

    question = gr.Markdown("Click start to begin")
    tree_plot = gr.Plot()

    start_btn = gr.Button("Start")
    with gr.Row():
        greater_btn = gr.Button("Greater")
        not_greater_btn = gr.Button("Not Greater")

    start_btn.click(
        start_game,
        outputs=[state_root, state_current, question, tree_plot]
    )

    greater_btn.click(
        lambda r, c: step(True, r, c),
        inputs=[state_root, state_current],
        outputs=[state_root, state_current, question, tree_plot]
    )

    not_greater_btn.click(
        lambda r, c: step(False, r, c),
        inputs=[state_root, state_current],
        outputs=[state_root, state_current, question, tree_plot]
    )

app.launch()