# data/

`maui-county.geojson` — outlines of the four Maui County islands (Maui,
Molokai, Lānaʻi, Kahoʻolawe), used by `generate_maps.py` to draw the island
for context behind the trail tracks.

Extracted from [us-atlas](https://github.com/topojson/us-atlas)'s
`counties-10m.json` (US Census TIGER/Line, simplified to 10m resolution),
filtered to Maui County (FIPS 15009) and converted from TopoJSON to GeoJSON
with `topojson-client`. us-atlas is ISC licensed (Copyright Michael Bostock).
Coordinates rounded to 5 decimal places (~1m) to keep the file small — this
is a basemap outline, not a survey reference.

To regenerate or extend to other counties/states:

```
npm install us-atlas topojson-client
node -e '
import("topojson-client").then(({feature}) => {
  const topo = require("us-atlas/counties-10m.json");
  const geo = feature(topo, topo.objects.counties);
  const maui = geo.features.filter(f => f.id === "15009");
  console.log(JSON.stringify({type: "FeatureCollection", features: maui}));
});
'
```
