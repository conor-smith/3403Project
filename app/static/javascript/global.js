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

function renderLogin()
{
  $('#renderLogin').load( "/login form");
}