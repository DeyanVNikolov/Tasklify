function getdata(id, otherid) {
    // Get the data from the server api /messageget/{id}/{otherid}
    // Return the data

    request = new XMLHttpRequest();
    request.open('GET', '/messageget/' + id + '/' + otherid, false);
    request.send(null);
    if (request.status === 200) {
        return JSON.parse(request.responseText);
    }

    return null;
    
}