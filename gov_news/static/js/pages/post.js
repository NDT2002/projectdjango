$(document).ready(function () {
    // Đối tượng trường dữ liệu và số lượng từ tối ưu cho từng trường
    var fields = [
        { name: "post_name", minWords: 75, maxWords: 100 },
        { name: "post_title", minWords: 50, maxWords: 70 },
        { name: "post_excerpt", minWords: 150, maxWords: 160 },
    ];
    $("input, textarea").each(function () {
      var name = $(this).attr("name");
      var valLength = $(this).val().length;
      updateProgressBar(name, valLength);
    });

  // Xử lý khi trường dữ liệu thay đổi
  $("input, textarea").on("input", function () {
    var name = $(this).attr("name");
    var valLength = $(this).val().length;
    updateProgressBar(name, valLength);
  });

  // Cập nhật progress bar dựa trên số lượng từ và đổi màu sắc
  function updateProgressBar(name, valLength) {
    fields.forEach(function (field) {
      console.log(name);
      if (field.name == name) {
        var progressBarElement = $("#" + field.name + "_progress");
        progressBarElement.css("width", "100%");
        if (valLength < field.minWords) {
          progressBarElement.css("background-color", "#349beb");
        } else if (valLength <= field.maxWords) {
          progressBarElement.css("background-color", "#34eb3a");
        } else {
          progressBarElement.css("background-color", "#ebab34");
        }
      }
    });
  }
});
