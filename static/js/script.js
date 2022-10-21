$(function () {
  $(document).scroll(function () {
    var $nav = $(".header");
    $nav.toggleClass('header_show', $(this).scrollTop() > $nav.height());
  });
});