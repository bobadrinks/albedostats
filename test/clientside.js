$('#ledon-button').click(function() {
    $.ajax({
        type: 'POST',
        url: 'http://localhost:1337/LEDon'
    });
});
