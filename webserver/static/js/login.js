function validate() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  
  if (username == "user" && password == "pw") {
    //alert("success")
    //alert("Login erfolgreich!");
    // Navigiere zu einer anderen Seite
    window.location.replace("../templates/home.html");
  } 
  else {
    alert("Benutzername oder Passwort falsch.");
  }
}