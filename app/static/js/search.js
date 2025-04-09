$(document).ready(function () {
        let friendModal = $("#friendReason")
    let warning = $("#reasonEmptyWarning")
    // add friend
    $(".friendListItemAddSearch").click(function () {
        warning.hide()
        let userAdd = $("#friendIdSearch").val()
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

})