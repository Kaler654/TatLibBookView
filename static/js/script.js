$(function () {
    $(document).scroll(function () {
        var $nav = $(".header");
        $nav.toggleClass('header_show', $(this).scrollTop() > $nav.height());
    });
});

$('.input-file input[type=file]').on('change', function(){
	let file = this.files[0];
	$(this).next().html(file.name);
});