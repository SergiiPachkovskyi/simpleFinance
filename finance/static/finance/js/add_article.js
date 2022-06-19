var user_select = document.getElementById('id_user');
var user_pk = document.getElementById("user_pk").value;
for (var i = user_select.options.length-1; i != -1; i--) {
    if (user_select.options[i].value != user_pk ) {
        user_select.remove(i)
    }
}
