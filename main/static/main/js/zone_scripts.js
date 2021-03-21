async function get_markers() {
    let response = await fetch('measurements');
    if (response.ok) {
        let json = await response.json();
        set_markers(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_markers(Data) {
    if (MarkerLayers.getLayers().length != 0) {
        MarkerLayers.clearLayers();
    } else {
        Data.forEach(element => {
            marker = L.circleMarker([element[0], element[1]], { radius: 5 }).bindPopup(element[2].toString());
            MarkerLayers.addLayer(marker);
        })
    }
}

async function get_zones() {
    let response = await fetch('zones');
    if (response.ok) {
        let json = await response.json();
        set_zones(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_zones(Data) {
    if (ZoneLayers.getLayers().length != 0) {
        ZoneLayers.clearLayers();
        Zones = []
    } else {
        Zones.push(...Data)
        Data.forEach(el => {
            bounds = [[el['lat1'], el['lng1']], [el['lat2'], el['lng2']]];
            zone = L.rectangle(bounds, { color: "#ff0000", weight: 2 }).bindPopup(`name: ${el['name']}`);
            ZoneLayers.addLayer(zone)
            zone.database_id = el['id']
        })
    }
}

async function upload() {
    for (index in Zones) {
        if (Zones[index]['status'] == 'from database'){
            Zones.splice(index, 1)
        }
    }
    Zones.push(window.prompt("Enter password to confirm changes", ""));
    let response = await fetch('zones', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(Zones)
    });
    if (response.ok) {
        let answer = await response.text();
        alert(answer);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
    document.location.reload();
}