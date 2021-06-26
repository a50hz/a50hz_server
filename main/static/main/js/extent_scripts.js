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
            marker = L.circleMarker([element[0], element[1]], { radius: 5 }).bindPopup(element[2].toString() + " nT");
            MarkerLayers.addLayer(marker);
        })
    }
}

async function get_extents() {
    let response = await fetch('extents');
    if (response.ok) {
        let json = await response.json();
        set_extents(json);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

function set_extents(Data) {
    if (ExtentLayers.getLayers().length != 0) {
        ExtentLayers.clearLayers();
        Extents = []
    } else {
        Extents.push(...Data)
        Data.forEach(el => {
            bounds = [[el['lat1'], el['lng1']], [el['lat2'], el['lng2']]];
            extent = L.rectangle(bounds, { color: "#ff0000", weight: 2 }).bindPopup(`name: ${el['place']}`);
            ExtentLayers.addLayer(extent)
            extent.database_id = el['id']
            extent.type = 'extent'
        })
    }
}

async function upload() {
    for (index in Extents) {
        if (Extents[index]['status'] == 'from database') {
            Extents.splice(index, 1)
        }
    }
    Extents.push(window.prompt("Enter password to confirm changes", ""));
    let response = await fetch('extents', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(Extents)
    });
    if (response.ok) {
        let answer = await response.text();
        alert(answer);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
    document.location.reload();
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
    } else {
        Data.forEach(el => {
            bounds = [[el['lat1'], el['lng1']], [el['lat2'], el['lng2']]];
            zone = L.rectangle(bounds, { color: "#ff0000", weight: 2 }).bindPopup(`name: ${el['name']}` + ` <a href="https://gms.myxomopx.ru/apply-zone?id=${el['id']}">https://gms.myxomopx.ru/apply-zone?id=${el['id']}</a>`);
            ZoneLayers.addLayer(zone)
            zone.database_id = el['id']
            zone.type = 'zone'
        })
    }
}