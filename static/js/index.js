function success_listener() {
    var data = JSON.parse(this.responseText);

    document.getElementById("result_photo").src = data.result_photo;
    document.getElementById("span_msg").innerHTML = data.message;

    if(data.status == "0") {
        document.getElementById("span_plate").innerHTML = data.plate;
        document.getElementById("span_top_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + data.location[0] + "<i class=\"fa fa-chevron-right\"></i>,";
        document.getElementById("span_top_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + data.location[1] + "<i class=\"fa fa-chevron-right\"></i>";
        document.getElementById("span_bottom_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + data.location[3] + "<i class=\"fa fa-chevron-right\"></i>,";
        document.getElementById("span_bottom_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + data.location[2] + "<i class=\"fa fa-chevron-right\"></i>";
        document.getElementById("span_confidence").innerHTML = data.confidence;
        
        document.getElementById("span_msg").className = "success";
    } else {
        document.getElementById("span_plate").innerHTML = "未识别";
        document.getElementById("span_top_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>0<i class=\"fa fa-chevron-right\"></i>,";
        document.getElementById("span_top_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>0<i class=\"fa fa-chevron-right\"></i>";
        document.getElementById("span_bottom_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>0<i class=\"fa fa-chevron-right\"></i>,";
        document.getElementById("span_bottom_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>0<i class=\"fa fa-chevron-right\"></i>";
        document.getElementById("span_confidence").innerHTML = "未识别";
        
        document.getElementById("span_msg").className = "failed";
    }
}

function ajax_post(url, photo) {
    var form_data = new FormData();
    form_data.append("photo", photo);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = success_listener;
    xhr.send(form_data);
}


var drag_overlay_div = document.getElementById('drag-overlay');

$(drag_overlay_div).click(function () {
    $(this).removeClass('drag-overlay');
});

//拖拽上传文件
document.getElementsByTagName("html")[0].addEventListener('dragover', function (event) {
    event.preventDefault(); // 必须阻止默认事件
    $(drag_overlay_div).addClass('drag-overlay');
}, false);
document.getElementsByTagName("html")[0].addEventListener('drop', function (event) {
    event.preventDefault(); // 阻止默认事件

    document.getElementById('upload_input').files = event.dataTransfer.files;
    document.getElementById('upload_form').submit();
}, false);

// 点击上传
var drag_target_box = document.getElementById("drag-target-box");
var upload_input = document.getElementById("upload_input");
var upload_form = document.getElementById("upload_form");

drag_target_box.onclick = function () {
    upload_input.click();
}
upload_input.onchange = function (event) {
    photo = document.getElementById("upload_input").files[0]
    ajax_post('/api/recognize', photo)
}