function scrolltobottom() {
    // scroll document to bottom
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}

function preparemessage_sender(message, date, id) {

    var div = document.createElement("div");
    div.className = "d-flex align-items-baseline mb-4";

    var div2 = document.createElement("div");
    div2.className = "pe-2";

    var div3 = document.createElement("div");
    
    var div4 = document.createElement("div");
    div4.className = "card-b card card-text d-inline-block p-2 px-3 m-1";
    div4.innerHTML = message;

    div3.appendChild(div4);

    var div5 = document.createElement("div");

    var div6 = document.createElement("div");
    div6.className = "small";
    div6.innerHTML = date;
    
    div5.appendChild(div6);

    div2.appendChild(div3);
    
    div2.appendChild(div5);

    div.appendChild(div2);

    return div;

}

function preparemessage_reciver(message, date, id) {
        
        var div = document.createElement("div");
        div.className = "d-flex align-items-baseline text-end justify-content-end mb-4";

        var div2 = document.createElement("div");
        div2.className = "pe-2";

        var div3 = document.createElement("div");
        
        var div4 = document.createElement("div");
        div4.className = "card-s card card-text d-inline-block p-2 px-3 m-1";
        div4.innerHTML = message;

        div3.appendChild(div4);

        var div5 = document.createElement("div");

        var div6 = document.createElement("div");
        div6.className = "small";
        div6.innerHTML = date;
        
        div5.appendChild(div6);

        div2.appendChild(div3);
        
        div2.appendChild(div5);

        div.appendChild(div2);

        return div;

}