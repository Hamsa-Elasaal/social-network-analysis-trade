"""Reproducible Python analysis for the 2024 South Asia–Southern Africa trade SNA project."""
from pathlib import Path
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = Path(__file__).resolve().parent / 'outputs'
FIG = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

nodes = pd.read_csv(DATA / 'SASA_NODES.csv', encoding='utf-8-sig')
edges = pd.read_csv(DATA / 'SASA_EDGES.csv', encoding='utf-8-sig')
edges.columns = edges.columns.str.strip()
required_nodes = {'id', 'label'}
required_edges = {'Source', 'Target', 'Weight', 'Type', 'Type label'}
assert required_nodes.issubset(nodes.columns)
assert required_edges.issubset(edges.columns)
assert not nodes.isna().any().any() and not edges.isna().any().any()
assert (edges['Weight'] >= 0).all()

G = nx.DiGraph()
for row in nodes.itertuples(index=False):
    G.add_node(str(row.id), label=row.label)
for _, row in edges.iterrows():
    G.add_edge(str(row['Source']), str(row['Target']), weight=float(row['Weight']))
U = G.to_undirected()

metrics = pd.DataFrame(index=list(G.nodes))
metrics['country'] = [G.nodes[n]['label'] for n in metrics.index]
metrics['in_degree'] = dict(G.in_degree())
metrics['out_degree'] = dict(G.out_degree())
metrics['total_degree'] = dict(G.degree())
metrics['weighted_in_degree'] = dict(G.in_degree(weight='weight'))
metrics['weighted_out_degree'] = dict(G.out_degree(weight='weight'))
metrics['weighted_total_degree'] = dict(G.degree(weight='weight'))
metrics['eigenvector_centrality'] = nx.eigenvector_centrality(G.reverse(), weight='weight', max_iter=2000)
metrics['closeness_centrality'] = nx.closeness_centrality(G)
metrics['betweenness_centrality'] = nx.betweenness_centrality(G)
metrics['pagerank'] = nx.pagerank(G, weight='weight')
hubs, authorities = nx.hits(G, max_iter=1000, normalized=True)
metrics['hits_hub'] = hubs
metrics['hits_authority'] = authorities
metrics['clustering_directed'] = nx.clustering(G)
metrics['clustering_undirected'] = nx.clustering(U)
metrics = metrics.sort_values('weighted_out_degree', ascending=False)
metrics.to_csv(OUT / 'node_metrics.csv', index_label='node_id')

summary = {
    'nodes': G.number_of_nodes(), 'directed_edges': G.number_of_edges(),
    'directed_density': nx.density(G), 'reciprocity': nx.reciprocity(G),
    'weakly_connected_components': nx.number_weakly_connected_components(G),
    'strongly_connected_components': nx.number_strongly_connected_components(G),
    'undirected_projection_density': nx.density(U),
    'directed_average_clustering_unweighted': nx.average_clustering(G),
    'directed_average_clustering_weighted': nx.average_clustering(G, weight='weight'),
    'undirected_average_clustering': nx.average_clustering(U),
    'undirected_transitivity': nx.transitivity(U),
    'undirected_diameter': nx.diameter(U),
    'undirected_average_shortest_path_length': nx.average_shortest_path_length(U),
}
pd.Series(summary, name='value').to_csv(OUT / 'network_summary.csv', header=True)
communities = nx.community.louvain_communities(U, weight='weight', seed=42)
community_map = {n: i + 1 for i, group in enumerate(communities) for n in group}
metrics['louvain_community_undirected'] = pd.Series(community_map)
metrics.to_csv(OUT / 'node_metrics.csv', index_label='node_id')
pd.DataFrame({'community': list(community_map.values()), 'node_id': list(community_map.keys()),
              'country': [G.nodes[n]['label'] for n in community_map]}).to_csv(OUT / 'communities.csv', index=False)

india = next(n for n, d in G.nodes(data=True) if d['label'] == 'India')
def largest_weak_component_size(graph):
    return max((len(c) for c in nx.weakly_connected_components(graph)), default=0) if graph.number_of_nodes() else 0
H = G.copy()
robust = [{'removed': 0, 'removed_country': 'None', 'remaining_nodes': H.number_of_nodes(),
           'largest_weak_component': largest_weak_component_size(H),
           'weak_components': nx.number_weakly_connected_components(H)}]
order = [india] + [n for n in sorted(G, key=lambda x: G.degree(x), reverse=True) if n != india]
for step, n in enumerate(order, 1):
    H.remove_node(n)
    robust.append({'removed': step, 'removed_country': G.nodes[n]['label'],
                   'remaining_nodes': H.number_of_nodes(),
                   'largest_weak_component': largest_weak_component_size(H),
                   'weak_components': nx.number_weakly_connected_components(H) if H.number_of_nodes() else 0})
pd.DataFrame(robust).to_csv(OUT / 'robustness_fixed_order.csv', index=False)

pos = nx.spring_layout(U, seed=42, weight='weight')
fig, ax = plt.subplots(figsize=(13, 10))
sizes = [220 + 1200 * metrics.loc[n, 'weighted_out_degree'] / metrics.weighted_out_degree.max() for n in G]
nx.draw_networkx_nodes(G, pos, node_size=sizes, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=.35, arrows=True, arrowsize=12, width=.8, ax=ax)
nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G}, font_size=8, ax=ax)
ax.set_title('Directed, weighted trade network (node size scaled by weighted exports)')
ax.axis('off'); fig.tight_layout(); fig.savefig(FIG / 'trade_network.png', dpi=220); plt.close(fig)

for col, title, filename in [
 ('weighted_in_degree','Weighted in-degree (recorded imports received)','weighted_in_degree.png'),
 ('weighted_out_degree','Weighted out-degree (recorded exports sent)','weighted_out_degree.png'),
 ('eigenvector_centrality','Eigenvector centrality (reverse graph; incoming influence)','eigenvector_centrality.png'),
 ('closeness_centrality','Directed closeness centrality','closeness_centrality.png')]:
    d = metrics.sort_values(col)
    fig, ax = plt.subplots(figsize=(10,7)); ax.barh(d.country,d[col]); ax.set_title(title)
    fig.tight_layout(); fig.savefig(FIG/filename,dpi=220); plt.close(fig)

reciprocal = {(u,v) for u,v in G.edges if G.has_edge(v,u)}
fig, ax = plt.subplots(figsize=(13,10))
nx.draw_networkx_nodes(G,pos,node_size=500,ax=ax)
nx.draw_networkx_edges(G,pos,edgelist=[(u,v) for u,v in G.edges if (u,v) not in reciprocal],alpha=.35,arrows=True,ax=ax)
nx.draw_networkx_edges(G,pos,edgelist=[(u,v) for u,v in reciprocal if str(u)<str(v)],width=2.2,arrows=True,ax=ax,connectionstyle='arc3,rad=0.12')
nx.draw_networkx_labels(G,pos,labels={n:G.nodes[n]['label'] for n in G},font_size=8,ax=ax)
ax.set_title(f'Reciprocal relationships highlighted (reciprocity = {summary["reciprocity"]:.3f})')
ax.axis('off'); fig.tight_layout(); fig.savefig(FIG/'reciprocity.png',dpi=220); plt.close(fig)

robust_df=pd.DataFrame(robust)
fig,ax=plt.subplots(figsize=(9,5)); ax.plot(robust_df.removed,robust_df.largest_weak_component,marker='o')
ax.set_xlabel('Number of nodes removed (fixed initial degree order)')
ax.set_ylabel('Largest weakly connected component size')
ax.set_title('Targeted node-removal robustness (fixed attack order)')
fig.tight_layout(); fig.savefig(FIG/'robustness.png',dpi=220); plt.close(fig)
print(summary)
