
function update_port(port) {
    if (port === 0) {
        port = $("#port").val();
    }
    let div_list = $("iframe");
    for (let i in div_list) {
        let div = $(div_list[i]);
        let pid = div.attr('id');
        div.attr('src', "http://localhost:" + port + "/#scalars&regexInput=" + pid);
    }
}

function kill(obj, pid) {
    $.ajax({
        method: "get",
        url: "/kill/" + pid,
        contentType: 'application/json',
        dataType: "json",
        success : function (data){
            if (data.err_no) {
                alert(data.err_msg);
                return;
            }
            $(obj).parent().html('success');
        }
    });
}