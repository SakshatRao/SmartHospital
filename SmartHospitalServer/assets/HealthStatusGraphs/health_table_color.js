$(function() {
    $('tr > td.temp').each(function(index) {
        var scale = [['low', 35], ['medium', 38], ['high', 45]];
        var score = $(this).text();
        for (var i = 0; i < scale.length; i++) {
            if (score <= scale[i][1]) {
                $(this).addClass(scale[i][0]);
                break;
            }
        }
    });
});