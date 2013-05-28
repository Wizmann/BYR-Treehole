$(document).ready(function() {
    $(".preview-btn").click(function() {
        var ptype=$(this).attr("ptype");
        var idx = $(this).parents(".preview").attr("sid");
        $.post("/secret/preview/",{"idx":idx, "ptype": ptype}, function(result)
        {
            location.reload();
        });
    });
});
        
