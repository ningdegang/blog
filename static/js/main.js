function getCookie(name){
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}
$(document).ready(function(){
    $("body").css({"background-color":"#aaa"});
    $("#login_error").css({"display":"none"});
    $("#login_button").click(function() {
        alert("click");
        var name = $("#inputEmail").val();
        var passwd = $("#inputPassword").val();
        var post_data ={"username":name, "passwd":passwd, "_xsrf":getCookie("_xsrf")};
        $.post("/login",post_data, function(ret_data, status){
            alert("post return data: "+ret_data);
            if(ret_data.indexOf("success") >= 0)
            {
                alert("success");
                location.href="/";
            }
            else 
            {
                alert("failed");
                $("#login_error").css({"display":"inline"});
            }
        }); 
    });
    $('#editor').wysiwyg();
    $("#create_blog_submit").click(function(){
        var context = $("#editor").html();
        $("textarea").val(context);
    });
});

function regist_check()
{
    var name = $("#name").val()
    var passwd = $("#passwd").val();
    var confirmpasswd = $("#confirmpasswd").val();
    if (passwd != confirmpasswd)
    {
        //alert("passwd not match");
        return false;
    }
    if(name == "" || passwd == "")
    {
        //alert("name or passwd is empty");
        return false;
    }
    $("#passwd").val(hex_md5(passwd));
    //alert("verify success");
    return true;
}
function login_check()
{
    alert("begin");
    var name = $("#username").val()
    var passwd = $("#passwd").val();
    if(name == "" || passwd == "")
    {
        alert("name or passwd is empty");
        return false;
    }
    $("#passwd").val(hex_md5(passwd));
    alert("verify success");
    return true;
}
