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
    if (map.hasLayer(layer)) {
        map.removeLayer(layer);
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
}

async function get_grids() {
    let response = await fetch('grid');
    if (response.ok) {
        let points = await response.json();
        set_heat_grid(points)
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_heat_grid(Data) {
    for (i in Data) {
        for (j in Data[i]) {
            Data[i][j] = [Data[i][j][0], Data[i][j][1], Math.abs(Data[i][j][2]) / 55]
        }
    }
    heat_grid_griddata = L.heatLayer(Data[0], { radius: 25 });
    heat_grid_rbf = L.heatLayer(Data[1], { radius: 25 });
    alert("Данные прогружены, вы можете приступить к работе!")
}

function show_heat_grid(method) {
    layer = method == 'griddata' ? heat_grid_griddata : heat_grid_rbf
    other_layer = layer == heat_grid_griddata ? heat_grid_rbf : heat_grid_griddata
    if (map.hasLayer(layer)) {
        map.removeLayer(layer);
    }
    else {
        if (map.hasLayer(other_layer)) {
            map.removeLayer(other_layer);
        }
        map.addLayer(layer);
    }
}
