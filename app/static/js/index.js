$(document).ready(function () {
    var swiper = new Swiper(".mySwiper", {
        spaceBetween: 10,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesProgress: true,
      });
      var swiper2 = new Swiper(".mySwiper2", {
        spaceBetween: 10,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        thumbs: {
          swiper: swiper,
        },
      });

    // $("#indexSearchMovie").click(function () {
    //     let movieName = $("#searchMovie").val()
    //     console.log(movieName)
    //     let searchContent = JSON.stringify({searchMovie: movieName})
    //     $.ajax({
    //             async: false,
    //             type: 'POST',
    //             url: "/search_movie",
    //             contentType: 'application/json; charset=UTF-8',
    //             dataType: 'json',
    //             data: searchContent,
    //             success: function(res){
    //                 window.location.href = "/search_movie"
    //                 console.log(res)
    //             },
    //             error: function(){
    //                 console.log('error')
    //             }
    //         })
    // })

    let popularUncheck = $("#popularUncheck")
    let popularCheck = $("#popularCheck")
    let latestUncheck = $("#latestUncheck")
    let latestCheck = $("#latestCheck")
    let topUncheck = $("#topUncheck")
    let topCheck = $("#topCheck")
    let viewUncheck = $("#viewUncheck")
    let viewCheck = $("#viewCheck")


    $("#indexPopularSelector").click(function () {
        $("#indexPopular").show()
        $("#indexLatest").hide()
        $("#indexTopRated").hide()
        $("#indexMostViewed").hide()
        if (!($("#indexPopularSelector").hasClass('fourBarTitleActive'))) {
            $("#indexPopularSelector").addClass('fourBarTitleActive')
            $("#indexPopularSelector").siblings().removeClass('fourBarTitleActive')
            popularCheck.show()
            popularUncheck.hide()
            topCheck.hide()
            topUncheck.show()
            viewCheck.hide()
            viewUncheck.show()
            latestCheck.hide()
            latestUncheck.show()
        }


    })


    $("#indexLatestSelector").click(function () {
        $("#indexPopular").hide()
        $("#indexLatest").show()
        $("#indexTopRated").hide()
        $("#indexMostViewed").hide()
        if (!($("#indexLatestSelector").hasClass('fourBarTitleActive'))) {
            $("#indexLatestSelector").addClass('fourBarTitleActive')
            $("#indexLatestSelector").siblings().removeClass('fourBarTitleActive')
            popularCheck.hide()
            popularUncheck.show()
            topCheck.hide()
            topUncheck.show()
            viewCheck.hide()
            viewUncheck.show()
            latestCheck.show()
            latestUncheck.hide()
        }
    })

    $("#indexTopRatedSelector").click(function () {
        $("#indexPopular").hide()
        $("#indexLatest").hide()
        $("#indexTopRated").show()
        $("#indexMostViewed").hide()
        if (!($("#indexTopRatedSelector").hasClass('fourBarTitleActive'))) {
            $("#indexTopRatedSelector").addClass('fourBarTitleActive')
            $("#indexTopRatedSelector").siblings().removeClass('fourBarTitleActive')
            popularCheck.hide()
            popularUncheck.show()
            topCheck.show()
            topUncheck.hide()
            viewCheck.hide()
            viewUncheck.show()
            latestCheck.hide()
            latestUncheck.show()
        }
    })

    $("#indexMostViewedSelector").click(function () {
        $("#indexPopular").hide()
        $("#indexLatest").hide()
        $("#indexTopRated").hide()
        $("#indexMostViewed").show()
        if (!($("#indexMostViewedSelector").hasClass('fourBarTitleActive'))) {
            $("#indexMostViewedSelector").addClass('fourBarTitleActive')
            $("#indexMostViewedSelector").siblings().removeClass('fourBarTitleActive')
            popularCheck.hide()
            popularUncheck.show()
            topCheck.hide()
            topUncheck.show()
            viewCheck.show()
            viewUncheck.hide()
            latestCheck.hide()
            latestUncheck.show()
        }
    })

    //feedback
    $("#feedbackButton").click(function () {
        $("#feedbackModal").modal("show")
        console.log(1)
    })

        // submit feedback
    $("#submitFeedbackInDetailPage").click(function () {
        console.log(111)
        let feedback = $("#feedbackInput").val()
        let feedbackTitle = $("#feedbackTitleInput").val()
        let userID = $("#userIDforFeedback").val()
        let data = JSON.stringify({'user_id': userID,
                        'feedback': feedback,
                        'feedbackTitle': feedbackTitle})
            if (feedback === '' || feedbackTitle === '') {
                alert("Please feedback again and make sure feedback is not empty")
            }
            else {
                $.ajax({
                type: "POST",
                url: "/feedback",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: data,
                success: function(res){
                    console.log(res)
                    if (res["returnValue"] === 1) {
                        }
                    },
                error: function(){
                    console.log('error')
                    }
                })
            }
    })


})


