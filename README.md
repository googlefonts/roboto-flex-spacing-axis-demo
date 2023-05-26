Roboto Flex SPAC
================

Adding a spacing axis to [Roboto Flex] using the [VariableSpacing] tools and data format.


Contents of this repository
---------------------------

```
Roboto Flex SPAC
├── scripts
│   └── *.py
├── spacing states
│   └── *.json
├── index.html
└── Roboto-Flex_SPAC.ttf
```

<dl>
<dt>scripts
<dd>various scripts to transform the UFO sources and build the variable font
<dt>spacing states
<dd>spacing state data in JSON format for all sources
<dt><a href='http://gferreira.github.io/roboto-flex-spac/'>index.html</a>
<dd>comparison between spacing axis and tracking
<dt>Roboto-Flex_SPAC.ttf
<dd>custom Roboto Flex variable font with a spacing axis
</dl>


About the project
-----------------

Roboto Flex SPAC is an experimental version of [Roboto Flex] which includes an additional *spacing* axis (`SPAC`).

The spacing axis offers a new way to modify the default spacing of a font. While the automatic tracking function provided by applications adds a fixed value to all glyph widths, the spacing axis allows the designer to define **proportional** changes to the glyph margins, and use a different set of kerning values as well.


Notes on the workflow
---------------------

Roboto Flex SPAC is built on top of the sources and designspace of Roboto Flex.

1. For each source in the `Mains`, `Duovars` and `Trivars` folders, with the exception of `GRAD` sources, two new “tight” and “loose” spacing sources are created. This process is assisted by a new set of tools and a custom data format.

2. The original designspace is extended with the addition of a new *spacing* axis (`SPAC`), and the insertion of all new “tight” and “loose” spacing sources produced in step (1) in their appropriate min/max locations on that axis.

3. A variable font is then generated from this new designspace using the standard `fontmake` pipeline.

4. The new Roboto Flex SPAC can be compared to Roboto Flex using a [custom testing page](http://gferreira.github.io/roboto-flex-spac/) which synchronizes the spacing axis value in the first with the tracking value in the second, and vice-versa.

### Creation of “tight” and “loose” spacing states

Variations of the default spacing are created by the designer with help of [VariableSpacing] tools. During the design stage, all the different versions of a font’s spacing can be stored inside the same UFO source. When it’s time to generate a variable font, these different *spacing states* are exported as separate UFOs.

It is essential that the width of the `space` glyph remains unaltered accross spacing states, as the reference point for all spacing variation. If a change to the width of the space is needed, it must be implemented through a separate mechanism (for example as a separate axis, or provided automatically by an application).  

Is is important that values in the spacing axis are more or less equivalent to tracking values. That is, setting the spacing axis value to `-50` should produce the same overall tightness than setting tracking to `-50`. The sweetspot can be found with help of the testing page after a few iterations.

### The “tight” spacing state

In the *tight* spacing state, glyphs can almost touch. The font’s default spacing was modified by the designer using the tool [smart set margins](#), which reduces all glyph margins to 10 units while making sure that all components stay in place. Some glyphs like `i`, `j`, `f` need a second, manual pass using a beam at specific y-positions.

The bottleneck of the whole workflow is defining the tight kerning values. A script (which employs the collision-detection code of the [Touché](http://github.com/ninastoessinger/Touche) extension) can be used to approximate the results, which still need to be checked visually and fine-tuned by hand, for all sources. The designer must make aesthetic decisions about which glyph pairs are allowed to touch and produce ligatures (for example `TV`, `KY`, `LX` etc), and which don’t – there is no additional parameter to control this aspect (as there is in [HEX Franklin Tyght](http://hex.xyz/HEX_Franklin/Tyght/)).

For this demonstation, only basic tight kerning was created for combinations of UC/UC, UC/lc and lc/lc. This work was done manually and was very time-consuming. The full implementation of tight kerning in all sources would require some form of automation, as provided by tools like [iKern](http://www.ikern.space), [KernOn](https://kern-on.com) or other.

### The “loose” spacing state

In the *loose* spacing state, the space between glyphs is almost as large as the word space. The font’s default spacing is modified automatically with a script, using an approach similar to positive tracking: a fixed number of units is added to the margins of all glyphs. The kerning values were not changed (maybe they should be).

### Remaining issues

There is currently no special handling for ligatures and digraph glyphs, which look odd when the spacing axis is close to the minimum (tight) or maximum (loose) ends of the axis. In comparison, automatic tracking usually disables ligatures when tracking exceeds a certain value. Similar behavior could be implemented in the spacing axis by adding glyph shape variations to spacing states – for more info see [add support for glyph shape variation along the spacing axis ](https://github.com/gferreira/VariableSpacing/issues/5).


[Roboto Flex]: http://github.com/googlefonts/roboto-flex
[VariableSpacing]: http://github.com/gferreira/VariableSpacing

