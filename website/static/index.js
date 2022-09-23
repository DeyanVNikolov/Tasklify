function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
}

    var myCookie = getCookie("locale");

    if (myCookie == null) {
        document.cookie = "locale=en;path=/"
        window.location.reload();
    }

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

    
function setlang(lang) {
    document.cookie = "locale=" + lang + ";path=/"
    console.log(document.cookie)
    window.location.reload();
  
}

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}