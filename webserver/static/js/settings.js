function toggleStatus() {
    const button = document.getElementById("toggleBtn");
    if (button.innerText === "Enabled") {
      button.innerText = "Disabled";
      button.style.backgroundColor = "#dd0000";
    } else {
      button.innerText = "Enabled";
      button.style.backgroundColor = "#4169E1";
    }
  }