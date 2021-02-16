async function get_plot(type, method){
    let extent = {
        type: type,
        method: method
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
    console.log(GeoLayer)
    for (i in GeoLayer._layers){
        GeoLayer._layers[i].options.color = GeoLayer._layers[i].feature.properties.stroke
    }
    GeoJSONLayers.addLayer(GeoLayer);
}

async function get_markers(){
    let response = await fetch('marker');
    if (response.ok) {
        let json = await response.json();
        set_markers(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_markers(Data){
    if (MarkerLayers.getLayers().length != 0){
        MarkerLayers.clearLayers();
    } else {
        Data.forEach(element => {
            marker = L.marker([element[0], element[1]]).bindPopup(element[2].toString());
            MarkerLayers.addLayer(marker);
        })
    } 
}