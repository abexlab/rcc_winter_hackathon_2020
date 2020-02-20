window.onload = () => {
  const initialSecId = "top";
  showSec(initialSecId);
}
const allSecIds = ["top", "charSelector", "recording", "result", "ranking"];

function hideAllSec() {
  for (let id of allSecIds) {
    document.getElementById(id).style.display = "none";
  }
}

function showSec(id) {
  hideAllSec();
  document.getElementById(id).style.display = "block";
}

