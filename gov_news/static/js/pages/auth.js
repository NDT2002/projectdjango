$(document).ready(function() {
    $('#show_password').on('click', function() {
        var passwordInput = $('#password');
        var eyeIcon = $('#eye_icon');

        if (passwordInput.attr('type') === 'password') {
            passwordInput.attr('type', 'text');
            eyeIcon.removeClass('bi bi-eye');
            eyeIcon.addClass('bi bi-eye-slash');
        } else {
            passwordInput.attr('type', 'password');
            eyeIcon.removeClass('bi bi-eye-slash');
            eyeIcon.addClass('bi bi-eye');
        }
    });
    $('#password').on('input', function() {
        validatePassword();
    });

    function validatePassword() {
        var passwordInput = $('#password');
        var passwordError = $('#passHelp');
        var password = passwordInput.val();

        // Kiểm tra 3 tiêu chí
        var hasMinLength = password.length >= 8;
        var hasDigit = /\d/.test(password);
        var hasSpecialChar = /[!@#$%^&*]/.test(password);

        // Kiểm tra và hiển thị thông báo tương ứng
        if (hasMinLength && hasDigit && hasSpecialChar) {
            passwordError.html('Mật khẩu Hợp lệ').removeClass('text-danger').addClass('text-success');
        } else {
            var message = 'Mật khẩu không hợp lệ. ';
            if (!hasMinLength) {
                message += 'Phải có ít nhất 8 ký tự. ';
            }
            if (!hasDigit) {
                message += 'Phải chứa ít nhất 1 chữ số. ';
            }
            if (!hasSpecialChar) {
                message += 'Phải chứa ít nhất 1 ký tự đặc biệt.';
            }
            passwordError.html(message).removeClass('text-success').addClass('text-danger');
        }
    }
    $('form').on('submit', function(event) {
        // Kiểm tra trường tên đăng nhập
        if ($('#username').val() === '') {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng nhập tên đăng nhập',
            });
            event.preventDefault(); // Ngăn chặn việc gửi biểu mẫu nếu trường trống
            return;
        }
        
        // Kiểm tra trường mật khẩu
        if ($('#password').val() === '') {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng nhập mật khẩu',
            });
            event.preventDefault();
            return;
        }
        
        // Kiểm tra trường xác nhận mật khẩu
        if ($('#confirm_password').val() === '') {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng xác nhận mật khẩu',
            });
            event.preventDefault();
            return;
        }
        
        if ($('#confirm_password').val() != $('#password').val() ) {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Mật khẩu xác nhận không đúng',
            });
            event.preventDefault();
            return;
        }
        
        // Kiểm tra trường email
        if ($('#email').val() === '') {
            Swal.fire({
                icon: 'error',
                title: 'Lỗi',
                text: 'Vui lòng nhập email',
            });
            event.preventDefault();
            return;
        }
        
        // Các kiểm tra cho các trường khác ở đây
        
        // Nếu tất cả các kiểm tra thành công, biểu mẫu sẽ được gửi đi
        
    });
});
  // Function to check if any field in col-4 is empty
  function checkForm() {
    var col4Inputs = document.querySelectorAll(".col-md-4 input, .col-md-4 textarea");
    var btnSave = document.getElementById("btn-save");

    var disableFields = false;

    for (var i = 0; i < col4Inputs.length; i++) {
      if (col4Inputs[i].value.trim() === "") {
        disableFields = true;
        break;
      }
    }

    var col8Inputs = document.querySelectorAll(".col-md-8 input, .col-md-8 textarea");
    for (var j = 0; j < col8Inputs.length; j++) {
      col8Inputs[j].disabled = disableFields;
    }

    btnSave.disabled = disableFields;
  }

  // Attach the checkForm function to the input fields' input event
  var col4Inputs = document.querySelectorAll(".col-md-4 input, .col-md-4 textarea");
  for (var k = 0; k < col4Inputs.length; k++) {
    col4Inputs[k].addEventListener("input", checkForm);
  }

// Function to format phone number as 4-3-3-3-2
function formatPhoneNumber(input) {
  // Xóa tất cả các ký tự không phải số và dấu gạch nối
  var cleaned = input.value.replace(/[^\d-]/g, '');

  // Giới hạn số lượng ký tự số và dấu gạch nối thành 15
  cleaned = cleaned.slice(0, 19);

  // Xóa tất cả các dấu gạch nối hiện tại
  cleaned = cleaned.replace(/-/g, '');

  // Định dạng theo dạng 4-3-3-3-2
  var formatted = '';
  for (var i = 0; i < cleaned.length; i++) {
    if (i === 4 || i === 7 || i === 10 || i === 13 || i === 15) {
      formatted += '-';
    }
    formatted += cleaned.charAt(i);
  }

  // Gán lại giá trị đã định dạng vào trường "Số điện thoại"
  input.value = formatted;
}

// Lấy trường "Số điện thoại" bằng id
var phoneInput = document.getElementById("phone");

// Gán sự kiện input vào trường "Số điện thoại"
phoneInput.addEventListener("input", function () {
  formatPhoneNumber(this);
});





  // Check the form initially when the page loads
  checkForm();