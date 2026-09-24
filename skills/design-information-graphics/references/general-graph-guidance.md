# General Graph Guidance

Apply this guidance before choosing detailed styling. It synthesizes the perception-and-cognition framework and the framework, label, and title construction guidance in Chapters 1 and 3 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), adapted for rigorous Python graphics.

## Begin with the communication task

Write the question the reader should be able to answer. Identify the audience's knowledge, the intended comparison, and the level of precision required. Include neither less evidence than the question needs nor unrelated detail.

Treat a graph as four coordinated systems:

- **Framework:** axes, scales, panels, and spatial organization establish how values can be compared.
- **Content:** marks encode the measurements and relationships.
- **Labels:** words and numbers identify meanings, units, categories, and values.
- **Optional components:** annotations, keys, reference lines, uncertainty, notes, and other aids appear only when they help the task.

## Apply the eight perceptual principles

1. **Relevance:** show all and only what the communication task needs. Necessary units, denominators, uncertainty, qualifications, and sources are relevant evidence.
2. **Appropriate knowledge:** use formats, symbols, terminology, and abbreviations the audience can understand. Explain unavoidable unfamiliar terms near the display.
3. **Salience:** make the most visually prominent feature correspond to the most important evidence. Reserve strong color, weight, contrast, or annotation for that role.
4. **Discriminability:** ensure marks, colors, line styles, labels, and differences are large and distinct enough to perceive in the intended output size and medium.
5. **Perceptual organization:** use proximity, similarity, alignment, enclosure, continuation, and shared direction to group related items. Put compared values and their labels close together.
6. **Compatibility:** make appearance agree with meaning. Greater values should normally appear as greater position, length, count, or intensity; spatial and temporal order should match the represented order.
7. **Informative changes:** every visible change will be interpreted as meaningful. Keep the same treatment for the same role, and vary a property only when it encodes or emphasizes a real distinction.
8. **Capacity limitations:** minimize memory-dependent lookup and mental arithmetic. Prefer direct labels, familiar forms, small multiples, and locally available comparisons. Split a panel when it contains more perceptual units than can be understood together; four is a useful warning threshold, not a mechanical mark limit.

## Construct the framework

- Make axes and baselines detectable but subordinate to data.
- Connect or align framework elements so they read as a coherent unit.
- Choose the aspect ratio to make material differences visible without exaggeration. For line charts, inspect whether the ratio creates misleading apparent slopes.
- Put the independent variable central to the message on the categorical or horizontal axis. If importance is equal, favor a continuous variable or the arrangement that produces fewer, simpler perceptual units.
- Order interval and ordinal values naturally. Order nominal categories to place intended comparisons together; otherwise use a purposeful progression such as value order.
- Preserve spatial compatibility: left/right, above/below, chronological order, and other meaningful positions should match what they represent.
- Use comparable scales across panels when comparison is intended. If scales differ, make the difference unmistakable.

## Set scales without distorting the evidence

- When length encodes magnitude, as in ordinary bars, use a meaningful zero baseline unless the chart explicitly encodes deviation from another stated baseline.
- Position encodings such as lines, dots, and intervals may use a narrowed range when it is necessary to reveal the relevant variation. State the range clearly and never conceal a break or imply a larger proportional change than the question supports.
- Include the relevant data range with modest breathing room. Do not extend the range merely to flatten meaningful variation or crop it to manufacture drama.
- Use linear scales by default. Use logarithmic or transformed scales only when the analytical meaning requires them, and name the transformation plainly.
- Place positive and negative values around a visible zero reference when sign matters.
- Use regularly spaced ticks that match the scale. Give labeled ticks greater visual weight than minor ticks; omit ticks that do not aid reading.
- Use gridlines when readers must recover or compare precise point values. Keep them lighter than the marks.
- Avoid dual axes. Use them only when two closely related measures must be compared in one display; distinguish and directly associate each measure with its axis, and prefer separate panels when feasible.

## Write labels and titles

- Use familiar, highly legible fonts available in the execution environment. Report and substitute for missing brand fonts rather than embedding or downloading them.
- Keep typography consistent. Change font, size, weight, or color only to signal hierarchy or a meaningful role.
- Keep multiword labels together and place each label closest to what it identifies.
- Prefer horizontal text. Avoid rotated labels when a horizontal format, shorter wording, or direct labeling can solve the space problem.
- Use the same terminology in the display, surrounding narrative, exported data, and metadata.
- Always state units and clarify denominators where needed. Format numbers consistently and at no more precision than the evidence supports.
- Prefer direct labels to legends. Use a compact key only when direct labels would collide, become unreadable, or repeat excessively across panels.
- Write a title that helps the reader understand the question or evidenced conclusion. In explanatory work, a supported takeaway title is appropriate; in exploratory work, use a neutral question or subject title.
- Make the title visually distinct and place it where it begins the intended reading path. Keep qualifications close to the claim they limit.

## Pre-render check

Before coding, verify that the planned framework makes the intended comparison local, the strongest visual emphasis matches the most important evidence, every change has meaning, labels can be read at final size, and no design decision implies unsupported precision or causality.

