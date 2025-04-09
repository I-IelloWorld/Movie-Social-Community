$(document).ready(function(){
        setTimeout(test, 500);

             let friendModal = $("#friendReason")
      let warning = $("#reasonEmptyWarning")
          // add friend
    $(".addfriend").click(function () {
        warning.hide()
        let userAdd = $("#userID").val()
        console.log(userAdd)
        console.log(userAdd)

        friendModal.modal("show")
        $("#selectedUserId").val(userAdd)
    })

//    make limitations to word length

    $("button[type=submit]").click(function (event) {
        let text = $("#friendReasonBodyText").val()
        console.log(text)
        if (text.length < 3) {
            event.preventDefault();
            warning.show()
        }
        else {
            $("#friendReasonForm").submit()
        }
    })

    $(".close").click(function () {
        friendModal.modal("hide")
    })
});