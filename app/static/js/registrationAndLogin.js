

$(document).ready(function () {
    let usernameReg = new RegExp('[\u4e00-\u9fa5_a-zA-Z0-9]{4,10}')
    let emailReg = new RegExp('^[A-Za-z0-9-_.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    let passwordReg = new RegExp('[0-9a-zA-Z_]{6,18}')

    let usernameW = $(".username-warning-same").text()
    console.log(usernameW)

    function warningSame() {
        if (usernameW !== "") {
            $('#reg-modal-body').append('<li>The same registered user name exists, please replace it.</li>')
            $('#regModal').modal("show");
        }
    }

    let logW = $(".reminder").text()
    console.log(logW)

    function logWarning() {
        console.log(logW !== undefined)
        console.log(logW.type)
        if (logW === "Incorrect user name or password") {
            $('#log-modal-body').append('<li>Incorrect username or password</li>')
            $('#logModal').modal("show");
        }
    }

    logWarning()

    warningSame()

    // select tag
    $("#selectTag").click(function () {
        $('#tagModal').modal("show");
    })

    $(".movie-type-check").click(function () {
        let thisType = $(this).attr("id")
        console.log(thisType)
        let thisTypeDiv = $("#" + thisType)
        thisTypeDiv.on("change", function () {
            let change = thisTypeDiv.is(":checked")
            if (change) {
                thisTypeDiv.val(1)
                $("#" + thisType + "Show").val(1)
                console.log($("#" + thisType + "Show").val())
            } else {
                thisTypeDiv.val("")
                $("#" + thisType + "Show").val("")
            }
        })
    })

    $("#username").blur(function(){   //失去焦点
        if (!($(this).val().match(usernameReg))){
            $(".username-warning").show()
        } else {
            $(".username-warning").hide()
        }
    })


    $("#Email").blur(function(){   //失去焦点
        if (!($(this).val().match(emailReg))){
            $(".email-warning").show()
        } else {
            $(".email-warning").hide()
        }
    })

    $("#password").blur(function(){   //失去焦点
        if (!($(this).val().match(passwordReg))){
            $(".password-warning").show()
        } else {
            $(".password-warning").hide()
        }
    })

    $("#passwordConfirm").blur(function(){   //失去焦点
        let password = ($("#password").val())
        if ($(this).val() !== password){
            $(".password-confirm-warning").show()
        } else {
            $(".password-confirm-warning").hide()
        }
    })

    $("button[type=submit]").click(function (event) {
        let password = ($("#password").val())
        if ((!$("#password").val().match(passwordReg)) || (!$("#username").val().match(usernameReg)) || (!$("#Email").val().match(emailReg)) || ($('#passwordConfirm').val()) !== password || !checkTagFull()) {
            event.preventDefault();
        }
        else {
            $("#sign-up-form").submit()
        }
    })
    
    
    function checkTagFull() {
        let tagS = $("#tagSelect").children("input")
        console.log(tagS)
        let nonempty = false
        tagS.each(function () {
            if ($(this).val() === "1") {
                nonempty = true
            }
        })
        return nonempty


    }



        $("#sign-up-button").click(function(){
        let password = ($("#password").val())
        if ((!$("#password").val().match(passwordReg)) || (!$("#username").val().match(usernameReg)) || (!$("#Email").val().match(emailReg)) || ($('#passwordConfirm').val()) !== password || !checkTagFull()) {
            $('#regModal').modal("show");
        } else {
            // $('#sign-up-form').submit()
        }
        if ((!$("#username").val().match(usernameReg))) {
            $('#reg-modal-body').append('<li>Username should be alphabets, Chinese characters, numbers or "_" between 4-12 length</li>')
            $('#reg-modal-body').append('<ul></ul>')
        }
        if ((!$("#Email").val().match(emailReg))) {
            $('#reg-modal-body').append('<li>Please enter correct email</li>')
            $('#reg-modal-body').append('<ul></ul>')
        }
        if ((!$("#password").val().match(passwordReg))) {
            $('#reg-modal-body').append('<li>Password should be alphabets, numbers or "_" between 6-18 length</li>')
            $('#reg-modal-body').append('<ul></ul>')
        }
        if (($("#passwordConfirm").val() !== password)) {
            $('#reg-modal-body').append('<li>Password Confirmation should be same as the password</li>')
            $('#reg-modal-body').append('<ul></ul>')
        }
        if (!checkTagFull()) {
            $('#reg-modal-body').append('<li>Please select at least 1 tag</li>')
            $('#reg-modal-body').append('<ul></ul>')
        }

    });

    $('#closeModal').click(function () {
        $('#reg-modal-body').children().remove()
    })

    $('#closeModal1').click(function () {
        $('#log-modal-body').children().remove()
    })




    // $("#logButton").click(function () {
    //     let logW = $(".reminder").text()
    //     console.log("0")
    //     console.log(logW)
    //     if (logW !== "") {
    //         $('.modal-body').append('<li>Incorrect username or password</li>')
    //         $('#logModal').modal("show");
    //     }
    //
    // })



})