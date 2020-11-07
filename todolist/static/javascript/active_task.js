function show_tools(id_el) {
    let div_id = "task-tools-" + id_el;
    document.getElementById(div_id).style.visibility="visible";
}

function hide_tools(id_el) {
    let div_id = "task-tools-" + id_el;
    document.getElementById(div_id).style.visibility="hidden";
}
