
function update_port(obj) {
    let port = $(obj).val();

    let div_list = $(".iframe_container");
    for (let i in div_list) {
        let div = $(div_list[i]);
        let pid = div.id;
        div.html('<iframe src="http://localhost:' + port + '/#scalars&regexInput=' + pid + '" frameborder="0"></iframe>');
    }
}