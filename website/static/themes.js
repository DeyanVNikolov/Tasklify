function darktheme() {
    document.cookie = "theme=dark; path=/";
    window.location.reload();
}

function lighttheme() {
    // get cookie from the / path
    document.cookie = "theme=light; path=/";
    window.location.reload();
}


function printWarningRed(message) {
  const bigMessage = message.toUpperCase();
  console.log(`%c\n%s\n`, `font-size: 30px; color: red; font-weight: bold;`, bigMessage);
}

function printWarningRedSmall(message) {
  const bigMessage = message.toUpperCase();
  console.log(`%c\n%s\n`, `font-size: 20px; color: red; font-weight: bold;`, bigMessage);
}

function printWarningYellow(message) {
    const bigMessage = message.toUpperCase();
    console.log(`%c\n%s\n`, `font-size: 20px; color: yellow; font-weight: bold;`, bigMessage);
}

function printWarningYellowSmall(message) {
    const bigMessage = message.toUpperCase();
    console.log(`%c\n%s\n`, `font-size: 15px; color: yellow; font-weight: bold;`, bigMessage);
}

console.error("SECURITY NOTICE");
printWarningRed("!!! WARNING !!!");
printWarningYellow("This is a security notice!");
printWarningYellow("Unless you know what you are doing, do not proceed!");
printWarningYellow("Pasting anything into the console can compromise your account and data!");
printWarningYellowSmall("Tasklify is not responsible for any damage caused by pasting anything into the console!");
printWarningRedSmall("Continue at your own risk!");
printWarningRed("!!! WARNING !!!");
console.error("SECURITY NOTICE");
console.error("Your data is at risk! Do not paste anything into the console unless you know what you are doing!")