$(document).ready(function(){
    $.post("/secret/get_preview_num/",{},function(result){
        $("#unpreview").html(result);
    });
});
