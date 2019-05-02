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