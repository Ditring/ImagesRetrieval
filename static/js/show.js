$("#file0").change(function () {
    var objUrl = getObjectURL(this.files[0]);//获取文件信息
    console.log("objUrl = " + objUrl);
    if (objUrl) {
        $("#img0").attr("src", objUrl);
    }
    var file = this.files[0];
    var formData = new FormData();
    formData.append('image', file);
    // 发送POST请求到后端，将formData作为数据发送
    $('#result').css('display', 'block')
    $.ajax({
        url: '/action/upload',  // 后端接收图片的URL
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (result) {
            console.log(result)
            if (parseInt(result['code']) == 1) {
                //替换照片
                $('#result .col-md-3').each(function (i, e) {
                    $(e).find('img').attr('src', '/static/dataset/' + result['img_names'][i])
                    $(e).find('img').attr('alt', result['img_names'][i])
                    $(e).find('a').attr('data-mfp-src', '/static/dataset/' + result['img_names'][i])
                    $(e).find('img').css('width', '287px')
                    $(e).find('.caption').html(result['img_names'][i])
                })
            } else {
                console.log(result['message'])
                alert(result['message'])
            }
        },
        error: function (xhr, status, error) {
            // 处理上传失败的情况
            console.error('上传失败: ' + error);
        }
    });
});

function getObjectURL(file) {
    var url = null;
    if (window.createObjectURL != undefined) {
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}


$(document).ready(function () {
    $('.thumbnail').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });
});
