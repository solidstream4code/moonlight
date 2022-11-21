$(document).ready(function() {
        $('.select-genre').hide()

        $(document).on('click', '.toggle-drop-down', function () {
            if ($(this).hasClass('opened')) {
                $('.select-genre').slideUp()
                $(this).removeClass('opened')
            } else {
                $('.select-genre').slideDown()
                $(this).addClass('opened')
            }
        })
    }
)