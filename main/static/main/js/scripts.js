async function get_markers() {
    let response = await fetch('measurements');
    if (response.ok) {
        let json = await response.json();
        set_markers(json);
        set_markers_heatmap(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_markers(Data) {
    Data.forEach(element => {
        marker = L.circleMarker([element[0], element[1]], { radius: 5 }).bindPopup(element[2].toString() + " mkT");
        MarkerLayers.addLayer(marker);
    })
}

function set_markers_heatmap(Data) {
    for (i in Data) {
        Data[i] = [Data[i][0], Data[i][1], Math.abs(Data[i][2] - 50) / 55]
    }
    heat_markers = L.heatLayer(Data, { radius: 25 });
}

function show_markers() {
    if (map.hasLayer(MarkerLayers)) {
        map.removeLayer(MarkerLayers);
    }
    else {
        map.addLayer(MarkerLayers);
    }
}

function show_markers_heatmap() {
    if (map.hasLayer(heat_markers)) {
        map.removeLayer(heat_markers);
    }
    else {
        map.addLayer(heat_markers);
    }
}

function show_legend_heatmap() {
    legend.onAdd = function (map) {
        var div = L.DomUtil.create("div", "legend");
        div.innerHTML += "<h4>Levels</h4>";
        div.innerHTML += '<i style="background: #8300e9"></i><span>1-3 nT</span><br>';
        div.innerHTML += '<i style="background: #b300d0"></i><span>3-6 nT</span><br>';
        div.innerHTML += '<i style="background: #d400b5"></i><span>6-10 nT</span><br>';
        div.innerHTML += '<i style="background: #eb009b"></i><span>10-15 nT</span><br>';
        div.innerHTML += '<i style="background: #fa0080"></i><span>15-21 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0067"></i><span>21-28 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0050"></i><span>28-36 nT</span><br>';
        div.innerHTML += '<i style="background: #ff003a"></i><span>36-45 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0023"></i><span>45-55 nT</span><br>';
        return div;
    };
}

function show_legend_isolines() {
    legend.onAdd = function (map) {
        var div = L.DomUtil.create("div", "legend");
        div.innerHTML += "<h4>Levels</h4>";
        div.innerHTML += '<i style="background: #0000ff"></i><span>1 nT</span><br>';
        div.innerHTML += '<i style="background: #8300e9"></i><span>3 nT</span><br>';
        div.innerHTML += '<i style="background: #b300d0"></i><span>6 nT</span><br>';
        div.innerHTML += '<i style="background: #d400b5"></i><span>10 nT</span><br>';
        div.innerHTML += '<i style="background: #eb009b"></i><span>15 nT</span><br>';
        div.innerHTML += '<i style="background: #fa0080"></i><span>21 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0067"></i><span>28 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0050"></i><span>36 nT</span><br>';
        div.innerHTML += '<i style="background: #ff003a"></i><span>45 nT</span><br>';
        div.innerHTML += '<i style="background: #ff0023"></i><span>55 nT</span><br>';
        return div;
    };
}

async function get_plots() {
    let response = await fetch('plots');
    if (response.ok) {
        let plots = await response.json();
        for (i in plots) {
            set_plot(plots[i], i);

        }
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_plot(GeoData, k) {
    if (typeof GeoJSONLayers[k] !== 'undefined') {
        if (GeoJSONLayers[k].length != 0) {
            GeoJSONLayers[k].clearLayers();
        }
    }
    GeoJSONLayers.set(k, new L.layerGroup());
    var GeoLayer = L.geoJSON(JSON.parse(GeoData))
    for (i in GeoLayer._layers) {
        GeoLayer._layers[i].options.color = GeoLayer._layers[i].feature.properties.stroke
        if (GeoLayer._layers[i].feature.geometry.type != "MultiPolygon") {
            GeoLayer._layers[i].bindPopup(GeoLayer._layers[i].feature.properties["level-value"].toString() + " mkT")
        }
    }
    GeoJSONLayers.get(k).addLayer(GeoLayer);
}

function show_plot(type_method) {
    layer = GeoJSONLayers.get(type_method)
    legend.remove()
    if (map.hasLayer(layer)) {
        map.removeLayer(layer);
        return
    }
    else {
        for (key of GeoJSONLayers.keys()) {
            if (key != type_method) {
                map.removeLayer(GeoJSONLayers.get(key))
            } else {
                map.addLayer(layer);
            }
        }
    }
    if (type_method.startsWith('heatmap')) {
        show_legend_heatmap()
    } else {
        show_legend_isolines()
    }
    legend.addTo(map);
}

function show_only_danger_lines() {
    cur_lev = 36
    levels = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
    cur_levels = levels.slice(levels.indexOf(cur_lev))
    if (!danger_lines) {
        map.eachLayer(function (layer) {
            if (layer.hasOwnProperty("feature")) {
                to_delete = true
                for (level of cur_levels) {
                    if (layer.feature.properties.title.startsWith(level.toString())) {
                        to_delete = false
                        break;
                    }
                }
                if (to_delete) {
                    deleted_layers.push(layer);
                    map.removeLayer(layer);
                }
            }
        });
    } else {
        for (layer of deleted_layers) {
            map.addLayer(layer)
        }
    }
    danger_lines = !danger_lines
}