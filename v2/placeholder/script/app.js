var html_nav;
var html_nav_list;

document.addEventListener('DOMContentLoaded', function () {
    html_nav_list = document.querySelector(".js-nav-list");
    html_nav_btn = document.querySelector(".js-nav-btn");
    var flf = 0

    html_nav_btn.addEventListener("click", function() {
        if (flf == 0) {
            html_nav_list.style.height = "255px";
            flf = 1;
        }
        else {
            html_nav_list.style.height = "0";
            flf = 0;
        }
        
    });

});