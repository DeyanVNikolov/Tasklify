function darktheme() {
    document.cookie = "theme=dark; path=/";
    window.location.reload();
}

function lighttheme() {
    // get cookie from the / path
    document.cookie = "theme=light; path=/";
    window.location.reload();
}

