function show_car_info(api_data) {
    document.getElementById("result_photo").src = "/imgs/results/" + api_data.result_photo;

    document.getElementById("span_msg").innerHTML = api_data.message;

    if (api_data.status == "0") {
        document.getElementById("result_photo").src = "/imgs/results/" + api_data.result_photo;
        document.getElementById("span_msg").className = "success";
    } else if(api_data.status == "2") {
        document.getElementById("result_photo").src = api_data.result_photo;
        document.getElementById("span_msg").className = "failed";
    } else {
        document.getElementById("result_photo").src = "/imgs/uploads/" + api_data.result_photo;
        document.getElementById("span_msg").className = "failed";
    }

    document.getElementById("span_plate").innerHTML = api_data.plate;
    document.getElementById("span_top_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + api_data.location[0] + "<i class=\"fa fa-chevron-right\"></i>,";
    document.getElementById("span_top_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + api_data.location[1] + "<i class=\"fa fa-chevron-right\"></i>";
    document.getElementById("span_bottom_left").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + api_data.location[3] + "<i class=\"fa fa-chevron-right\"></i>,";
    document.getElementById("span_bottom_right").innerHTML = "<i class=\"fa fa-chevron-left\"></i>" + api_data.location[2] + "<i class=\"fa fa-chevron-right\"></i>";
    document.getElementById("span_confidence").innerHTML = api_data.confidence;

    document.getElementById("span_time").innerHTML = api_data.used_time;
    document.getElementById("span_size").innerHTML = api_data.img_size;
    document.getElementById("span_dpi").innerHTML = api_data.img_dpi;
    document.getElementById("span_format").innerHTML = api_data.img_format;
}

function load_listener() {
    api_data = {
        "status": 1,
        "message": "",
        "plate": "未识别",
        "result_photo": "/imgs/online_lnr/default_car.jpg",
        "confidence": 0.0,
        "location": [0, 0, 0, 0],
        "img_dpi": "未识别",
        "img_format": "未识别",
        "img_size": "未识别",
        "used_time": "未识别"
    }

    if (this.status == 413) {
        api_data.status = 1
        api_data.message = "图片大于2M无法识别"
        show_car_info(api_data);
        return;
    }

    if (this.status != 200) {
        api_data.status = 2
        api_data.message = "接口请求失败"
        show_car_info(api_data);
        return;
    }

    if (this.responseText == null) {
        api_data.status = 2
        api_data.message = "接口请求失败，返回值为空"
        show_car_info(api_data);
        return;
    }

    try {
        var api_data = JSON.parse(this.responseText);
        show_car_info(api_data);
    } catch (e) {
        api_data.message = "接口返回值错误"
        show_car_info(api_data);
    }
}

function ajax_post(url, photo) {
    var form_data = new FormData();
    form_data.append("photo", photo);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = load_listener;
    xhr.send(form_data);
}


var drag_overlay_div = document.getElementById('drag_overlay');

$(drag_overlay_div).click(function () {
    $(this).removeClass('drag_overlay');
});


function check_photo_size(photo) {
    MAX_SIZE = 2 * 1024 * 1024;

    if (photo.size > MAX_SIZE) {
        show_car_info("图片不能大于2M，请重新选择图片", "/imgs/online_lnr/default_car.jpg", "未识别", [0, 0, 0, 0], "未识别", "failed");
        alert("图片不能大于2M，请重新选择图片");
        return 1;
    }

    return 0;
}

//拖拽上传文件
document.getElementsByTagName("html")[0].addEventListener('dragover', function (event) {
    event.preventDefault(); // 必须阻止默认事件
    $(drag_overlay_div).addClass('drag_overlay');
}, false);
document.getElementsByTagName("html")[0].addEventListener('drop', function (event) {
    event.preventDefault(); // 阻止默认事件

    photo = event.dataTransfer.files[0];

    if (check_photo_size(photo) == 0) {
        ajax_post('/api/recognize', photo)
        $(drag_overlay_div).removeClass('drag_overlay');
    }
}, false);

// 点击上传
var drag_target_box = document.getElementById("drag_target_box");
var upload_input = document.getElementById("upload_input");
var upload_form = document.getElementById("upload_form");

drag_target_box.onclick = function () {
    upload_input.click();
}
upload_input.onchange = function (event) {
    photo = document.getElementById("upload_input").files[0]

    if (check_photo_size(photo) == 0)
        ajax_post('/api/recognize', photo)
}

function toggle_mobile_menu() {
    var e;
    return e = document.querySelector("#menu-container-mobile"),
        "block" === e.style.display ? e.style.display = "none" : e.style.display = "block",
        null
}

function init_mobile_form() {
    var mobile_choose_btn = document.getElementById("mobile_choose_btn");
    var mobile_choose_input = document.getElementById("mobile_choose_input");
    var mobile_form_submit = document.getElementById("mobile_form_submit");

    mobile_form_submit.setAttribute("disabled", "disabled")

    mobile_choose_btn.onclick = function () {
        mobile_choose_input.click()
    }

    mobile_choose_btn.onkeydown = function () {
        mobile_choose_input.click()
    }

    mobile_choose_input.onchange = function () {
        mobile_form_submit.removeAttribute("disabled")

        photo = mobile_choose_input.files[0]
        mobile_choose_btn.innerText = "文件：" + photo.name
    }

    mobile_form_submit.onclick = function () {
        photo = mobile_choose_input.files[0]

        if (check_photo_size(photo) == 0) {
            ajax_post('/api/recognize', photo)
            mobile_form_submit.setAttribute("disabled", "disabled")
        }
    }
}

window.onload = function () {
    if (window.innerWidth <= 1080)
        init_mobile_form()
}

window.onresize = function () {
    if (window.innerWidth <= 1080)
        init_mobile_form()
}