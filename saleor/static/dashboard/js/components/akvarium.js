// var createCookie = function(name, value, days) {
//     var expires;
//     if (days) {
//         var date = new Date();
//         date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
//         expires = "; expires=" + date.toGMTString();
//     }
//     else {
//         expires = "";
//     }
//     document.cookie = name + "=" + value + expires + "; path=/";
// }
//
// function getCookie(c_name) {
//     if (document.cookie.length > 0) {
//         c_start = document.cookie.indexOf(c_name + "=");
//         if (c_start != -1) {
//             c_start = c_start + c_name.length + 1;
//             c_end = document.cookie.indexOf(";", c_start);
//             if (c_end == -1) {
//                 c_end = document.cookie.length;
//             }
//             return unescape(document.cookie.substring(c_start, c_end));
//         }
//     }
//     return "";
// }
//
// //Returning to pginated page list
// let rows = document.getElementsByClassName('avatar');
// for (let item of rows) {
//   item.onclick = function () {
//     createCookie('paged_url', window.location.href);
//   };
// };
//
// let goToPaginated = document.getElementById('paginated_url');
// if (goToPaginated != null) {
//   goToPaginated.onclick = function () {
//     let paged_url = getCookie('paged_url');
//     window.location.replace(paged_url);
//   };
// };

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let rows = document.getElementsByClassName('avatar');
for (let item of rows) {
  item.onclick = function (e) {
    data = {}
    data["paged_url"] = window.location.href;
    data["csrfmiddlewaretoken"]= getCookie('csrftoken');
      $.ajax({
      url : '/dashboard/products/ajax-paged-url/',
      type : "POST",
      data : data,
      cache: false,
      success: function(data){
        // alert(data);
      }
    });
  };
};
