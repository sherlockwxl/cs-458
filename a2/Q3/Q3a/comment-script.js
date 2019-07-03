function fn(){
    var path = window.location.pathname.substring(window.location.pathname.lastIndexOf("/")+1);
    if(path == "view.php") {
        var str = window.location.search;
        var re = new RegExp(/\\?id=[0-9]+/);
        if(re.test(str)){// contains id
            console.log("matched");
            document.getElementById("author").innerHTML = "posted by AGoldmund";
            var idstr = String(str.match(re));
            var id = idstr.substring(idstr.lastIndexOf("=")+1);
            return id;
        }
    }else{
        return;
    }
}