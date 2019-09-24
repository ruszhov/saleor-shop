//Returning to pginated page list
let rows = document.getElementsByClassName('avatar');
for (let item of rows) {
  item.onclick = function () {
    sessionStorage.setItem("current_url", window.location.href);
  };
}

let goToPaginated = document.getElementById('paginated_url');
if (goToPaginated != null) {
  goToPaginated.onclick = function () {
    window.location.replace(sessionStorage.getItem("current_url"));
  };
};
