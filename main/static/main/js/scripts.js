async function get_plot(type, method){
    b = map.getBounds()
    let extent = {
        lat1: b._northEast.lat,
        lat2: b._southWest.lat,
        lng1: b._northEast.lng,
        lng2: b._southWest.lng,
        method: method,
        type: type
    };
    let response = await fetch('plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(extent)
    });
    if (response.ok) {
        let json = await response.json();
        set_layer(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_layer(GeoData){
    if (GeoJSONLayers.length != 0){
        GeoJSONLayers.clearLayers();
    }
    var GeoLayer = L.geoJSON()
    GeoLayer.addData(GeoData)
    GeoJSONLayers.addLayer(GeoLayer);
}