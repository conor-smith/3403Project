/*
  This javascript file is for javascript code that applies
  to every page on the website e.g. date modified
*/

// Shows date the document was last modified
function lastModified()
{
  var lm = new Date(document.lastModified);
  document.getElementById("lastmod").innerHTML = 
    "This page was last modified: " + lm.getDate() + 
    "/" + (lm.getMonth() + 1) + "/" + lm.getFullYear() + 
    " " + lm.getHours() + ":" + lm.getMinutes() +
    ":" + lm.getSeconds();
}


// Handles login popup
$("document").ready(function()
{
  // Displays login popup and dims rest of page
  $("#userlogin").click(function()
  {
    document.getElementById("cover").style.zIndex = "50"
    document.getElementById("cover").style.opacity = "0.5"
    document.getElementById("ulogin").style.display = "block"
  })

  // Hides login popup
  $("#cover").click(function()
  {
    document.getElementById("cover").style.zIndex = "-1"
    document.getElementById("cover").style.opacity = "0"
    document.getElementById("ulogin").style.display = "none"
  })
})