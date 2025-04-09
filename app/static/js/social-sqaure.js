$(document).ready(function () {
    var swiperCard = new Swiper(".myCardSwiper", {
        effect: "cards",
        grabCursor: true,
        freeMode: false,

    });


    let initName = $('.swiper-slide-active').find(".cardUser0").text()
    $('#cardUser').text(initName)
    let initGender = $('.swiper-slide-active').find(".cardGender0").text()
    $('#cardGender').text(initGender)
    let initIntro = $('.swiper-slide-active').find(".cardIntro0").text()
    $('#cardIntro').text(initIntro)
    let initTag = $('.swiper-slide-active').find(".cardTag0").text()
    $('#cardTag').text(initTag)

    swiperCard.on("transitionEnd", function () {
        let name = $('.swiper-slide-active').find(".cardUser0").text()
        $('#cardUser').text(name)
        let gender = $('.swiper-slide-active').find(".cardGender0").text()
        $('#cardGender').text(gender)
        let intro = $('.swiper-slide-active').find(".cardIntro0").text()
        $('#cardIntro').text(intro)
        let tag = $('.swiper-slide-active').find(".cardTag0").text()
        $('#cardTag').text(tag)
    })

    let friendModal = $("#friendReason")
    let warning = $("#reasonEmptyWarning")
    //add recommended friends
    $(".add-recommended-friends").click(function () {
        warning.hide()
        let userRecAdd = $(this).attr("id")
        let userRecAddId = $("#" + userRecAdd)
        let userRecAddSib = userRecAddId.prev().text()

        friendModal.modal("show")
        $("#selectedUserId").val(userRecAddSib)
    })

    // add friend
    $(".friendListItemAdd").click(function () {
        warning.hide()
        let userAdd = $(this).attr("id")
        console.log(userAdd)
        let userAddId = $("#" + userAdd)
        let userAddSib = userAddId.prev().text()
        console.log(userAddSib)

        friendModal.modal("show")
        $("#selectedUserId").val(userAddSib)
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