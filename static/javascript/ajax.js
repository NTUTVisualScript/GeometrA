const hostUrl = "http://127.0.0.1:5000";

function Get(apiUrl, callback) {
    $(document).ready(function() {
        $.ajax({
            type: "GET",
            url: hostUrl + apiUrl,
            success: function(msg) {
                callback(msg);
            },
            error: function(xhr, textStatus, error) {
                console.log(xhr.statusText);
            }
        });
    });
}

function Post(apiUrl, postData, callback) {
    $(document).ready(function() {
        $.ajax({
            type: "POST",
            url: hostUrl + apiUrl,
            data: postData,
            success: function(msg) {
                callback(msg);
            },
        });
    });
}
