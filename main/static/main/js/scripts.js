function getTypeUrl() {
    if (isolines.checked){
        return "isolines"
    }
    return "heatmap"
}

function getTypeMethod() {
    if (griddata.checked){
        return "griddata"
    }
    else if (spline.checked){
        return "spline"
    }
    return "pandas"
}

async function get_data(url, method){
    if (url == undefined){
        url = getTypeUrl();
    }   
    if (method == undefined){
        method = getTypeMethod();
    } 
    b = map.getBounds()
    let borders = {
        x1: b._northEast.lng,
        x2: b._southWest.lng,
        y1: b._northEast.lat,
        y2: b._southWest.lat,
        method: method
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