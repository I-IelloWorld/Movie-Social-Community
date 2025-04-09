$(document).ready(function () {

    //select category
    $(".movie-category-select").click(function () {
        let thisType = $(this).attr("id")
        console.log(thisType)
        let thisTypeDiv = $("#" + thisType)
        thisTypeDiv.on("change", function () {
            let change = thisTypeDiv.is(":checked")
            if (change) {
                thisTypeDiv.val(1)
                console.log(thisTypeDiv.val())
            } else {
                thisTypeDiv.val("")
                console.log(thisTypeDiv.val())
            }
        })
    })

    function checkTagFull() {
        let tagS = $("#categorySelect").find(".movie-category-select")
        console.log(tagS)
        let nonempty = false
        tagS.each(function () {
            console.log($(this).val())
            if ($(this).val() === "1") {
                nonempty = true
            }
        })
        console.log(nonempty)
        return nonempty
    }

    $("button[type=submit]").click(function (event) {
        if (checkTagFull()) {
            event.preventDefault();
        }
        else {
            $("#categorySelect").submit()
        }
    })
})

