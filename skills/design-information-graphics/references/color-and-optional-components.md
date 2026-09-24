# Color and Optional Components

Read this after the selected format-specific reference and before final rendering whenever the graphic uses color, texture, fills, gridlines, legends, captions, backgrounds, or multiple panels. It synthesizes Chapter 7 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), adapted for current accessibility and static Python practice.

## Color

- Use color to encode categories, group corresponding elements, establish hierarchy, or emphasize supported evidence. Do not add hue merely for variety.
- Separate adjacent colors by both hue and lightness. Check the rendered result for common color-vision deficiencies and grayscale reproduction.
- Use a restrained palette. More than about five categorical hues is a warning that direct comparison or grouping may be overloaded.
- Assign the strongest saturation, contrast, or warm accent to the most important content only. Keep guides and comparison context quieter.
- Prefer cool, low-salience colors for background context and warm or high-contrast colors for focal foreground marks, while respecting brand semantics and accessibility.
- Avoid red and blue as touching regions when their boundary becomes visually unstable. Avoid relying on blue alone when monochrome reproduction is expected.
- Do not use unordered hue to represent ordered quantity. Use position or length first; if color must carry order, use a perceptually ordered lightness or saturation scale with sufficient contrast.
- Do not vary hue, saturation, and lightness independently to encode separate variables. Their interactions are difficult to separate and can create accidental hierarchy.
- Preserve the same semantic color mapping across panels and across a project collection.

## Hatching, texture, and shading

- Use texture when color is unavailable, when grayscale reproduction matters, or as a redundant accessibility cue.
- Ensure adjacent patterns differ enough to be discriminable at final size. For line hatching, orientations separated by roughly 30 degrees and spacings differing by about 2:1 are useful starting checks, not guarantees.
- Avoid dense patterns that produce visual vibration or moire at the export resolution.
- Keep texture subordinate to the quantitative mark and test labels placed over fills for contrast.
- Do not alternate pattern or shade unless the change carries a declared meaning.

## Three-dimensional effects

- Do not use decorative 3D perspective, extrusion, shadows, or camera angles for two-dimensional data. They distort length, area, alignment, and occlusion.
- Use a genuinely three-dimensional display only when three quantitative spatial dimensions are necessary and no clearer set of two-dimensional views serves the task.
- If 3D is unavoidable, prevent occlusion, use views that reveal all critical content, label the axes unambiguously, and export the underlying coordinates. A static 3D view cannot support precise hidden-value comparison.

## Gridlines, backgrounds, captions, and keys

- Use thin, light gridlines when precise lookup or vertical/horizontal comparison needs them. Increase grid density only when the required precision justifies it.
- Avoid decorative backgrounds. A background element is acceptable only when it reinforces the subject or an evidential relationship without competing with or grouping falsely with the marks.
- Put necessary captions or notes close to the display and make them typographically distinct but legible. Use them for unfamiliar terms, methods, sources, and qualifications.
- Prefer direct labels. Use a key only when it reduces collisions or repeated labeling.
- Order legend patches exactly like the corresponding content elements and keep each patch closest to its label. Use one shared legend for repeated mappings across panels.
- Conventional legend placement is secondary to clarity; place it in available whitespace without covering data or interrupting the reading path.

## Multiple panels

- Put data that answer different questions in different panels. Put observations that must be directly compared together when doing so remains legible.
- Group lines or marks that form a meaningful pattern in the same panel; otherwise group similar series so each panel forms a manageable perceptual unit.
- Keep panels close enough to read as one composition but far enough apart that labels and marks cannot group with the wrong panel.
- Put the primary panel first in the audience's reading direction, normally upper left for left-to-right readers.
- Keep corresponding categories, positions, colors, mark types, and orders consistent. Vary panel size or appearance only when that variation carries an explicit meaning.
- Use identical scales and units when cross-panel magnitude comparison matters. If a scale must differ, label it unmistakably and do not invite direct visual comparison of incompatible heights.
- Remove redundant labels only when readers can still recover the intended values and panel identity without memory-dependent lookup.
- Make overview/detail and part/whole relationships explicit through titles, alignment, or restrained connectors.

## Final accessibility check

Inspect the actual PNG and SVG at intended size. Verify contrast, grayscale legibility, color-vision robustness, legend-to-mark mapping, panel alignment, grid hierarchy, texture rendering, label clarity, and the absence of decorative depth or background interference.

