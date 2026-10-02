# Choose a Graph Format

Choose from the communication relationship, data grain, precision required, and medium. Do not choose solely from numeric data type. State the choice in one sentence; offer alternatives only for meaningful tradeoffs. Respect a requested format unless it distorts or cannot represent the supplied data.

| Relationship | Route |
| --- | --- |
| Parts of a meaningful whole | `proportions.md` |
| Compare quantities or ranks across categories | `quantitative-and-ranking.md` |
| Change over an ordered dimension; association between variables | `lines-and-scatter.md` |
| Components contributing to totals; upstream running totals | `composition-and-cumulative.md` |
| Sets, hierarchies, geography, processes, flows | `special-cases.md` |

Percentages need ordinary bars or lines when comparing independent rates rather than parts of one whole. Stacked displays show composition, not necessarily running totals. Do not calculate missing analytical quantities to enable a preferred chart.

For distributions outside these families, use suitable shared narrative guidance: require upstream bins, densities, quantiles, or summaries where those are needed. If no route fits, explain the gap and propose a supported representation rather than forcing the data.

Revisit selection when the intended relationship changes. Skip reselection for typography, spacing, color, or label revisions.
