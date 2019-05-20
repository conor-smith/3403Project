var number = 1

$(document).ready(function()
{
    var entries = $(".movieCover").length
    console.log(entries)
    $(".movieCover").click(function()
    {
        $(this).parent().hide()
        $(this).siblings("input").val(number)
        if(number == entries)
        {
            $("#poll").submit()
        }
        number++
    })
})