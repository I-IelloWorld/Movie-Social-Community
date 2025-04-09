$(document).ready(function () {
    $(".banUserSearched, .banUser").click(function () {
        let user_id = $(this).prev().text()
        console.log(user_id)
        let data = JSON.stringify({'id': user_id})
        $.ajax({
                type: "POST",
                url: "/ban",
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                data: data,
                success: function(res){
                    console.log(res)
                    },
                error: function(){
                    console.log('error')
                    }
                })
                window.setTimeout(function () {
                    window.location.reload();
                 },150)
    })
})