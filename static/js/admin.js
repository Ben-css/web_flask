// 在錯誤訊息顯示後，啟動計時器以在10秒後隱藏錯誤訊息
document.addEventListener("DOMContentLoaded", function() {
    var errorMessage = document.getElementById("error-message");
    if (errorMessage) {
        setTimeout(function() {
            errorMessage.style.display = 'none';
        }, 5000); // 5秒後隱藏錯誤訊息
    }
});