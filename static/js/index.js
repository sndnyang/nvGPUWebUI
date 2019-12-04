
function update_port(obj) {
    let port = $(obj).val();

    let div_list = $("iframe");
    for (let i in div_list) {
        let div = $(div_list[i]);
        let pid = div.id;
        div.attr('src', "http://localhost:" + port + "/#scalars&regexInput=" + pid);
    }
}