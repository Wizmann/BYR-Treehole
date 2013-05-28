$(document).ready(function() {

    $(".star").each(function() {
        var status = $(this).attr("status");
        if(status=="on") {
            $(this).addClass("star-highlighted");
        }
    });

    $(".star").click(function() {
        var sid=$(this).attr("sid");
        var starnum = $(this).siblings(".command").children("p");
        var star = $(this);
        if($(this).attr("status")=="on") {
            $.post("/secret/shell/starlight/",{"sid": sid, "cmd": "off"}, 
                function(request){
                    console.log(request);
                    if(request=="true") {
                        star.attr("status", "off");
                        starnum.text(parseInt(starnum.text())-1);
                        star.toggleClass("star-highlighted");
                    }
                    else {
                        var res = jQuery.parseJSON(request).info;
                        var pp = star.parent().parent(".secret");
                        if(pp.siblings(".alert").html()) {}
                        else {
                            pp.append("<div class=\"alert alert-info\"><a class=\"close\" data-dismiss=\"alert\">×</a>" + res + "</div>");
                        }
                    }
                }
            );
        }
        else {
            $.post("/secret/shell/starlight/",{"sid": sid, "cmd": "on"},
                function(request) {
                    if(request=="true") {
                        star.attr("status", "on");
                        starnum.text(parseInt(starnum.text())+1);
                        star.toggleClass("star-highlighted");
                    }
                    else {
                        var res = jQuery.parseJSON(request).info;
                        var pp = star.parent().parent(".secret");
                        if(pp.siblings('.alert').html()) {}
                        else {
                            pp.after("<div class=\"alert alert-info\"><a class=\"close\" data-dismiss=\"alert\">×</a>" + res + "</div>");
                        }
                    }
                }
            );
        }
    });


    $(".fui-cross-24").click( function() {
        //TODO: 增加验证对话框
        var sid=$(this).attr("sid");
        $.post("/secret/shell/ban/",{"sid": sid},function(){
            window.location.reload(true)
        });
    });
});
