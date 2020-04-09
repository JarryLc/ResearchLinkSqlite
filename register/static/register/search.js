function tree(data) {
    if (typeof (data) == 'object') {
        let ul = $('<ul>');
        for (let i in data) {
            ul.append($('<li>').text(i).append(tree(data[i])));
        }
        return ul;
    } else {
        let textNode = document.createTextNode(' => ' + data);
        return textNode;
    }
}

$(document).ready(function () {
    $('#ajax_search-form').on('submit', function (event) {
        event.preventDefault();
        console.log("form submitted!"); // sanity check
        let formData = $('#ajax_search-form').serialize();
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/search/?"+String(formData),
            success: function (data) {
                console.log(data);
                let ul = $('#display-result');
                ul.empty();
                ul.append(tree(data));
            }
        });
    });
});
