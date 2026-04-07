import os
import networkx as nx
from pyvis.network import Network
from graph_vault import load_vault
import webbrowser

def draw_interactive_timeline():
    print("🔭 Booting up interactive TVA monitor...")
    
    # 1. Load the current graph from your JSON file
    g = load_vault()

    if g.number_of_nodes() == 0:
        print("The Vault is empty. Nothing to visualize!")
        return

    # 2. Prep the data for Pyvis
    # We need to copy our 'relation' attribute into a 'label' attribute 
    # so Pyvis knows to draw the text on the arrows.
    for source, target, data in g.edges(data=True):
        if 'relation' in data:
            data['label'] = data['relation']  # Text visible on the arrow
            data['title'] = data['relation']  # Text visible when you hover

    # 3. Initialize the Pyvis Network Canvas
    # We give it a dark mode aesthetic (bgcolor) so it looks like a real monitor
    net = Network(
        height='800px', 
        width='100%', 
        bgcolor='#1a1a1a', 
        font_color='white', 
        directed=True # Ensures we keep our arrows!
    )

    # Pyvis has a built-in physics engine. This turns it on so nodes bounce and settle nicely.
    net.barnes_hut()

    # 4. Ingest the NetworkX graph
    net.from_nx(g)

    # 5. Save and open the HTML file
    output_file = 'tva_interactive_monitor.html'
    net.write_html(output_file)
    
    print(f"✅ Simulation rendered! Opening {output_file} in your web browser...")
    
    # Automatically open the generated HTML file in your default web browser
    webbrowser.open('file://' + os.path.realpath(output_file))

if __name__ == "__main__":
    draw_interactive_timeline()