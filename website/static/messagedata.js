function getdata(id, otherid) {
    // Get the data from the server api /messageget/{id}/{otherid}
    // Return the data

    request = new XMLHttpRequest();
    try {
    request.open('GET', '/messageget/' + id + '/' + otherid, false);
    request.send(null);
    if (request.status === 200) {
        return JSON.parse(request.responseText);
    }
} catch (e) {
    console.log("ERROR! ERROR! ERROR!");
    return "No data could be retrieved! Web server is down or not responding.";
    
}
}