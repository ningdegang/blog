$(document).ready(function(){$("body").css({"background-color":"444"});});

function regist_check()
{
    var name = $("#name").val()
    var passwd = $("#passwd").val();
    var confirmpasswd = $("#confirmpasswd").val();
    if (passwd != confirmpasswd)
    {
        alert("passwd not match");
        return false;
    }
    if(name == "" || passwd == "")
    {
        alert("name or passwd is empty");
        return false;
    }
    $("#passwd").val(hex_md5(passwd));
    alert("verify success");
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
