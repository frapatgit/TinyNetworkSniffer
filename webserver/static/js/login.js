function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/authenticate", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          window.location.href = "/home";
      } else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status !== 200) {
          alert("Invalid username or password.");
      }
  };
  var data = JSON.stringify({"username": username, "password": password});
  xhr.send(data);
}
