/*
  This javascript file is for javascript code that applies
  to every page on the website e.g. date modified
*/

// Shows date the document was last modified
function lastModified()
{
  var x = document.lastModified;
  document.getElementById("lastmod").innerHTML = "This page was last modified: " + x;
}

// Shows current time
function currentTime()
{
  var d = new Date();
  var n = d.toLocaleTimeString();
  document.getElementById("currenttime").innerHTML = "The current time is: " + n;
}

//Handles login popup
$("document").ready(function()
{
  //Displays login popup and dims rest of page
  $("#userlogin").click(function()
  {
    document.getElementById("cover").style.zIndex = "50"
    document.getElementById("cover").style.opacity = "0.5"
    document.getElementById("ulogin").style.display = "block"
  })

  //hides login popup
  $("#cover").click(function()
  {
    document.getElementById("cover").style.zIndex = "-1"
    document.getElementById("cover").style.opacity = "0"
    document.getElementById("ulogin").style.display = "none"
  })
})