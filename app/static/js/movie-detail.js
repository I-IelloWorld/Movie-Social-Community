$(document).ready(function () {

    function isLogin() {
        let isLogined
        $.ajax({
            async: false,
            type: 'GET',
            url: "/isLogin",
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function(res){
                console.log(res['isLogined'])
                isLogined = res['isLogined']
            },
            error: function(){
                console.log('error')
            }
        })
        return isLogined
    }


    // get movie id
    let movieDetail = $("#movieDetailID").text()
    let movieDetailID = parseInt(movieDetail)


    // rate the movie
    let rateModal = $("#Rate")
    $("#RateButton").click(function () {
        if (isLogin()) {
            console.log(1)
            rateModal.modal("show")
        } else {
            window.location.href = '/login'
        }

    })


    // submit rating
    $("#submitRateInDetailPage").click(function () {
        // let commentContent = $("#commentList")
        // console.log(movieDetailID)
        // console.log(typeof movieDetailID)
        let rate =  $("#rateInput").val() * 1

        // let comment = $("#commentInput").val()
        // let commentTitle = $("#commentTitleInput").val()
        // console.log(commentTitle.length)
        console.log(rate)
        console.log(rate * 2)
        // console.log(comment)
        // console.log(commentTitle)
        let data = JSON.stringify({'movie_id': movieDetailID,
                    'rate': rate})

            if (rate === 0) {
                console.log(rate)
                alert("Please rate again and make sure rate is not empty")
            }
            else {
                $.ajax({
                type: "POST",
                url: "/movie/sent_rate",
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
                window.setTimeout(function () {
                    window.location.reload();
                 },150)
            }



    })


    // comment start
    let commentModal = $("#Comment")
    $("#CommentButton").click(function () {
        if (isLogin()) {
            console.log(1)
            commentModal.modal("show")
        } else {
            window.location.href = '/login'
        }

    })


    // submit comment
    $("#submitCommentInDetailPage").click(function () {
        let commentContent = $("#commentList")
        let comment = $("#commentInput").val()
        let commentTitle = $("#commentTitleInput").val()
        let data = JSON.stringify({'movie_id': movieDetailID,
                        'comment': comment,
                        'commentTitle': commentTitle})
            if (comment === '' || commentTitle === '') {
                alert("Please comment again and make sure comment is not empty")
            }
            else {
                $.ajax({
                type: "POST",
                url: "/movie/sent_comment",
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
                window.setTimeout(function () {
                    window.location.reload();
                 },150)
            }
    })


    // like a movie
    $("#movieEmptyHeartButton, #movieEmptyHeartButton1").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            $("#movieEmptyHeartButton").hide()
            $("#movieEmptyHeartButton1").hide()
            $("#movieHeartButton").show()
            $("#movieHeartButton1").show()
            let liked = JSON.stringify({"like": 1,
                                        'movie_id': movieDetailID})
            $.ajax({
                async: false,
                type: 'POST',
                url: "/isliked",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: liked,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }

    })

    // cancel like a movie
    $("#movieHeartButton, #movieHeartButton1").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            $("#movieHeartButton").hide()
            $("#movieHeartButton1").hide()
            $("#movieEmptyHeartButton").show()
            $("#movieEmptyHeartButton1").show()
            let liked = JSON.stringify({"like": 0,
                                       'movie_id': movieDetailID})
            $.ajax({
                async: false,
                type: 'POST',
                url: "/isliked",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: liked,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }
    })


    // collect a movie
    $("#CollectEmptyMovieButton, #CollectEmptyMovieButton1").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            $("#CollectEmptyMovieButton").hide()
            $("#CollectEmptyMovieButton1").hide()
            $("#CollectMovieButton").show()
            $("#CollectMovieButton1").show()
            let collected = JSON.stringify({"collected": 1,
                                                'movie_id': movieDetailID})
            $.ajax({
                async: false,
                type: 'POST',
                url: "/isCollected",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: collected,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }

    })


    // cancel collect a movie
    $("#CollectMovieButton, #CollectMovieButton1").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            $("#CollectMovieButton").hide()
            $("#CollectMovieButton1").hide()
            $("#CollectEmptyMovieButton").show()
            $("#CollectEmptyMovieButton1").show()
            let collected = JSON.stringify({"collected": 0,
                                                 'movie_id': movieDetailID})
            $.ajax({
                async: false,
                type: 'POST',
                url: "/isCollected",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: collected,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }

    })


    // dislike a comment
    $(".commentLike").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            let commentID = $(this).attr('id')
            console.log(commentID)
            console.log(typeof (commentID))
            $("#"+commentID).hide()
            $("#"+commentID).siblings().show()
            let pureCommentId = commentID.split("S")
            console.log(pureCommentId)
            let commentliked = JSON.stringify({"like": 0,
                                                "comment_id": pureCommentId[1]})
            let newCommentLikeNum = parseInt($("#commentNum" + pureCommentId[1]).text())
            $("#commentNum" + pureCommentId[1]).text((newCommentLikeNum - 1).toString())
            $.ajax({
                async: false,
                type: 'POST',
                url: "/like_comment",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: commentliked,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }
    })
    //
    // like a comment
    $(".commentDislike").click(function () {
        if (!isLogin()) {
            window.location.href = '/login'
        } else {
            let commentID = $(this).attr('id')
            console.log(commentID)
            let pureCommentId = commentID.split("S")
            console.log(pureCommentId)
            $("#"+commentID).hide()
            $("#"+commentID).siblings().show()
            let newCommentLikeNum = parseInt($("#commentNum" + pureCommentId[1]).text())
            $("#commentNum" + pureCommentId[1]).text((newCommentLikeNum + 1).toString())
            let commentliked = JSON.stringify({"like": 1, "comment_id": pureCommentId[1]})
            $.ajax({
                async: false,
                type: 'POST',
                url: "/like_comment",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: commentliked,
                success: function(res){
                    console.log(res)
                },
                error: function(){
                    console.log('error')
                }
            })
        }
    })

})