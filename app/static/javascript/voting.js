var number = 1

$(document).ready(function()
{
    $(".movieCover").click(function()
    {
        $(this).parent().hide()
        $(this).siblings("input").val(number)
        number++
    })
})