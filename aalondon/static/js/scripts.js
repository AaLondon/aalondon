window.onscroll = function() {
    growShrinkLogo();
};

function growShrinkLogo() {
    var Logo = document.getElementById("Logo");
    if (document.body.scrollTop > 5 || document.documentElement.scrollTop > 5) {
        Logo.style.width = '50px';
    } else {
        Logo.style.width = '80px';
    }
}