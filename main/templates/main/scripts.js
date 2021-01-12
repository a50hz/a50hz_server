function getTypeUrl() {
    if (isolines.checked){
        return "isolines"
    }
    return "heatmap"
}

async function get_data(url){
    if (url == undefined){
        url = getTypeUrl();
    }   
    b = map.getBounds()
    let borders = {
        x1: b._northEast.lng,
        x2: b._southWest.lng,
        y1: b._northEast.lat,
        y2: b._southWest.lat
    };
    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(borders)
    });
    if (response.ok) {
        let json = await response.json();
        get_layer(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function get_layer(GeoData){
    if (GeoJSONLayers.length != 0){
        GeoJSONLayers.clearLayers();
    }
    var GeoLayer = L.geoJSON()
    GeoLayer.addData(GeoData)
    GeoJSONLayers.addLayer(GeoLayer);
}