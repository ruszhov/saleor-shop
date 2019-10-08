// import {onAddToCartError, onAddToCartSuccess} from './cart';
// import {variantImages} from '../../dashboard-next/products/fixtures';
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

window.onload=function() {
  let selector = document.getElementById('id_variant');
  if(selector){
    selector.addEventListener('change', function (event) {
    let value = selector[selector.selectedIndex].value;
    let data = {};
    data['value'] = value;
    data['csrftoken'] = getCookie('csrftoken');
    $.ajax({
      url: '/en/products/ajax-selected-variant/',
      method: 'post',
      passDXHeaders: false,
      dataType: 'json',
      async: true,
      data: data,
      success: function (response) {
        if (response != false) {
          let full_url = (window.location.origin).toString() + '/' + (getCookie('django_language')).toString() + '/products/' + (response).toString();
          location.replace(full_url);
        }}
      });
    }, false);
    // Making selected options like current product variant
    let dataString = JSON.parse(selector.dataset.images);
    let first_key = Object.keys(dataString)[0];
    selector.value = first_key;
  };
}
