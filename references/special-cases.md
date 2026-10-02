# Special Cases

Route only when the input structure and Python rendering tools are available. Do not promise unsupported diagrams, fabricate geography, derive intersections, or infer flows. Explain missing requirements and offer a supported alternative. Confirm consequential dependencies before adding them.

| Case | Analysis-ready inputs | Design and validation |
| --- | --- | --- |
| Venn/set diagrams | Supplied set membership specification or exact intersection counts | Verify inclusive/exclusive count semantics and consistency; label counts. Use a visual table when accurate area cannot be represented. Do not calculate intersections in place of upstream analysis. |
| Tree/hierarchy | Supplied node IDs, labels, and parent/child links | Check roots, missing nodes, cycles, and declared multiple-parent policy. Use readable layout; do not infer hierarchy. |
| Process/relationship diagram | Supplied nodes and directed/undirected links | Verify endpoints and arrow meaning. Distinguish schematic layout from quantitative encoding. |
| Map | Authorized supplied geometry, region IDs, coordinate reference system, and mapped values | Require geometry already matched to values; no joins/geocoding. Check CRS, unmatched regions, missing-data encoding, and area bias. Require supplied rates for rate maps. Use an available Python geospatial renderer; offer a regional bar chart if unavailable. |
| Sankey/flow | Supplied source, target, weight, and units | Check endpoints, nonnegative weights, and conservation where required by the model. Explain leakage or gains supplied by the analyst. Keep widths proportional; never infer balancing flows. |

For all cases, export the exact displayed data to CSV with stable identifiers. If topology or geometry is also required for recreation, include it losslessly in CSV (for example, WKT geometry plus CRS), or explain that CSV alone cannot reproduce the graphic and resolve an appropriate representation before finalization. Do not silently replace the agreed CSV with another format.

Use Matplotlib when suitable; a different available Python renderer may be used when needed. Keep rendering separate from analytical processing. Do not fabricate a quantitative evidence dataset for purely schematic diagrams: export the supplied node/link specification with explanatory labels.
