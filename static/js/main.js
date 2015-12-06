function getCookie(name){
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}

function regist_check()
{
    //alert("begin regist check");
    var name = $("#name").val();
    var passwd = $("#passwd").val();
    var confirmpasswd = $("#confirmpasswd").val();
    if( passwd == "")
    {
        $("#passwd_not_match").html("<font color=\"red\">passwd is empty</font>");
        $("#passwd_not_match").css({'display':'inline'});
    }
    if (passwd != confirmpasswd)
    {
        //alert("passwd not match");
        $("#passwd_not_match").html("<font color=\"red\">confirm passwd not match</font>");
        $("#passwd_not_match").css({'display':'inline'});
        return false;
    }
    if(name == "" )
    {
        //alert("name or passwd is empty");
        $("#user_exist").html("<font color=\"red\">username is empty</font>");
        $("#user_exist").css({'display':'inline'});
        return false;
    }
    passwd =$.md5(passwd);
    $.post("/regist", {"username":name,"passwd":passwd, "_xsrf":getCookie("_xsrf")}, function(data, status){
        if(data=='success') {  
            location.href="/"};
    });
    //alert("verify success");
    return true;
}
function login_check()
{
    //alert("begin");
    var name = $("#username").val();
    var passwd = $("#passwd").val();
    if(name == "") 
    {
        //alert("name or passwd is empty");
        $("#login_error").html("<font color=\"red\">username is empty</font>");
        return false;
    }
    if( passwd == "")
    {
        $("#login_error").html("<font color=\"red\">passwd is empty</font>");
        return false;
    }
    //alert("verify success");
    return true;
}

function checkConfirm(){ 
    $("#user_exist").css({'display':'none'});
    $("#passwd_not_match").css({'display':'none'});
    $("#name").blur(function(){ 
        var gradename = $(this).val(); 
        var url = "regist?act=userexist&name="+gradename; 
        $.get(url,function(data, status){ 
            if(data == 'exists'){ 
                $("#user_exist").html("<font color=\"red\">*username exists</font>"); 
                $("#user_exist").css({'display':'inline'});
            }
            else {
                $("#user_exist").html("<font color=\"green\">congratunation</font>");
                $("#user_exist").css({'display':'inline'});
            }
        }); 
    });
    $("#confirmpasswd").blur(function(){
        var passwd = $("#passwd").val();
        var confirmpasswd = $("#confirmpasswd").val();
        if(passwd != confirmpasswd)
        {
            $("#passwd_not_match").html("<font color=\"red\">*confirm passwd not match</font>");
            $("#passwd_not_match").css({'display':'inline'});
        }
        else
        {
            $("#passwd_not_match").html("<font color=\"green\">confirm passwd match</font>");
            $("#passwd_not_match").css({'display':'inline'});
        }
    });
    
} 
$(document).ready(function(){
    checkConfirm();
    $("#regist_submit").click(regist_check);
    $("body").css({"background-color":"#aaa"});
    $("#login_error").css({"display":"none"});
    $("#login_button").click(function() {
        //alert("click");
        if(login_check() == false) return;
        var name = $("#username").val();
        var passwd = $("#passwd").val();
        passwd = $.md5(passwd);
        var post_data ={"username":name, "passwd":passwd, "_xsrf":getCookie("_xsrf")};
        $.post("/login",post_data, function(ret_data, status){
            //alert("post return data: "+ret_data);
            if(ret_data.indexOf("success") >= 0)
            {
                //alert("success");
                //$("#login_error").html("<font color=\"green\">login ok</font>");
                //$("#login_error").css({"display":"inline"});
                location.href="/";
            }
            else 
            {
                //alert("failed");
                $("#login_error").html("<font color=\"red\">passwd invalid</font>");
                $("#login_error").css({"display":"inline"});
            }
        }); 
    });
    //$('#editor').wysiwyg();
    $("#create_blog_submit").click(function(){
        var context = $("#editor").html();
        $("textarea").val(context);
    });
});

