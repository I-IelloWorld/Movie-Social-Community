$(document).ready(function (){


    let selfName
    let selfIcon
    let contactUserName
    let contactUserIcon
    let socket = io();
    let data
    // 连接
    socket.connect(location.protocol + '//' + document.domain + ':' + location.port);
    //click user to chat interface
    let sortList = $(".sort_list")

    sortList.click(function () {
        $(this).find("#unread").hide()
        data = $(this).find("#friendRoom").text()
        $("#roomID").val(data)
        console.log(data)
        let roomData = JSON.stringify({"room_id": data})

        $.ajax({
            type: "POST",
            url: "/api/contact",
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            data: roomData,
            success: function(res){
                let selfId = res['self']
                selfIcon = res['self_icon']
                let contactUser = res['contact_user']
                contactUserName = res['contact_username']
                contactUserIcon = res['contact_user_icon']
                let message = res['message']
                selfName = res['self_name']
                 // 加入房间
                socket.emit('join', {
                    username: selfName,
                    room: data
                })
                $("#chat-interface").empty()
                let content = ""
                content += "<div class=\"col-md-12\"><div id=\"chatUsername\" class=\"chat-username\">" + contactUserName
                    + "<button id=\"leaveRoom\" class=\"leave-room\"><a href=\"/chat_list\">Exit</a></button></div></div><div class=\"col-md-12\"><hr></div><div class=\"container-fluid chat-box\" id=\"chatBox\">"
                for (let i = 0; i < message.length; i++) {
                    if (message[i]["author"] === contactUser) {
                        content += "<div class=\"row\"><div class=\"col-md-5 \"><div class=\"chat-title\"><img src=\"\" alt=\"\" class=\"chat-img contactor-img\" id=\"contactor-img\"><h3>"
                            + "&nbsp" + contactUserName + "</h3></div>"
                        content += "<p class=\"other-user-chat-box\">" + message[i]["content"] + "</p></div></div>"
                        // $("#contact-img").attr("src", contactUserIcon)
                        // console.log($("#contact-img").attr("src"))
                    }
                    if (message[i]["author"] === selfId) {
                        content += "<div class=\"row\"><div class=\"col-md-5 col-md-offset-7\"><div class=\"chat-title\"><img src=\"\" alt=\"\" class=\"chat-img pull-right user-img\" id=\"user-img\"><h3 class=\"text-right\">"
                            + "&nbsp" + selfName + "</h3></div>"
                        content += "<p class=\"user-chat-box pull-right\">" + message[i]["content"] + "</p></div></div>"
                        // $("#user-img").attr("src", selfIcon)
                    }
                }
                content += "</div><div class=\"container-fluid send-chat-box\"><div class=\"col-md-11\"><textarea name=\"chat\" id=\"chat-textarea\" cols=\"85\" rows=\"6\" class=\"chat-text\" placeholder=\"\"></textarea></div><div class=\"col-md-1\"><button class=\"chat-submit\" id=\"chatSubmit\">Submit</button></div></div>"
                $("#chat-interface").append(content)
                $(".contactor-img").attr("src", contactUserIcon)
                $(".user-img").attr("src", selfIcon)
                $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight)
                },
            error: function(){
                console.log('error')
                }
            })
            // window.setTimeout(function () {
            //     window.location.reload();
            //  },150)
    })



    // 退出房间
    $(document).on('click','#leaveRoom',function(){
        let room = $(".sort_list").find("#friendRoom").text()
        socket.emit('leave', {
            username: selfName,
            room: room
        })
    })


    // 发送消息
    $(document).on('click','#chatSubmit',function(){
        let inp = $('#chat-textarea')
        let msg = inp.val()
        let data = $("#roomID").val()
        console.log(data)
        if (msg !== "" && msg.length <= 600) {
            socket.emit('send msg', {
                user: selfName,
                message: msg,
                room: data,
            })
            let chatHTML = ""
            chatHTML += "<div class=\"row\"><div class=\"col-md-5 col-md-offset-7\"><div class=\"chat-title\"><img src=\"\" alt=\"\" class=\"chat-img pull-right user-img\" id=\"user-img\"><h3 class=\"text-right\">&nbsp" +  selfName + "</h3></div><p class=\"user-chat-box pull-right\">"
            chatHTML += msg
            chatHTML += "</p></div></div>"
            $("#chatBox").append(chatHTML)
            $(".user-img").attr("src", selfIcon)
            $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight)
            inp.val("")
        } else {
            $("#chatErrorModal").modal("show")
        }
    })
    // let chatSubmit = $("#submitChat")
    // chatSubmit.click(function () {
    //     let inp = $('#chat-textarea')
    //     let msg = inp.value
    //     let user = '{{ username }}'
    //     inp.value = ''
    //     if (msg) {
    //         socket.emit('send msg', {
    //             user: user,
    //             message: msg,
    //         })
    //         messageBox.scrollTop = messageBox.scrollHeight
    //     } else {
    //         alert('消息不能为空')
    //     }
    // })
    // sendMsgBtn.onclick = function () {
    //     let inp = document.querySelector('#send-msg-inp')
    //     let msg = inp.value
    //     let user = '{{ username }}'
    //     inp.value = ''
    //     if (msg) {
    //         socket.emit('send msg', {
    //             user: user,
    //             message: msg,
    //         })
    //         messageBox.scrollTop = messageBox.scrollHeight
    //     } else {
    //         alert('消息不能为空')
    //     }
    // }

    // 回车发送消息
    // $('#chat-textarea').addEventListener("keyup", function (event) {
    //     event.preventDefault();
    //     if (event.keyCode === 13) {
    //         $('#chatSubmit').click();
    //     }
    // });
    //
    // 连接的信息
    socket.on('connect info', function (data) {
        // console.log(data)
        // let connectInfo = document.createElement('div')
        // connectInfo.style = 'text-align: center'
        // let msg = '<li >${data}</li>'
        // connectInfo.innerHTML = msg
        // $("chatBox").appendChild(connectInfo)
        $("#online").modal("show")
        $("#chatMessage").empty()
        $("#chatMessage").text(data)
    })
    //
    // 接受消息
    socket.on('send msg', function (data) {
        console.log(data)
        console.log(socket.id)

        // let msg = null
        if (data.user !== selfName) {
            let chatHTML = `<div class=\"row\"><div class=\"col-md-5\"><div class=\"chat-title\"><img src=\"\" alt=\"\" class=\"chat-img contactor-img\" id=\"contactor-img\"><h3 class=\"\">&nbsp${data.user}</h3></div><p class=\"other-user-chat-box\">${data.message}</p></div></div>`
            $("#chatBox").append(chatHTML)
            $(".contactor-img").attr("src", contactUserIcon)
        } else {
            // msg = `<li class="left" ><b>${data.user}</b>:  ${data.message}</li>`
        }
        $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight)
    })
})