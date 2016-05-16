$(document).ready(function(){

    $( "#query" ).submit(function( event ) {
        event.preventDefault();
        $.get('api/query?' + $('#query').serialize(), function( data ) {

            // build table object
            var table = $('<table></table>').addClass('table');

            //console.log('word: ' + data['result']['word']);
            var row = $('<tr><td colspan="3" align="center"><b>' + data['result']['word'] + '</b></td></tr>');
            table.append(row);

            var row = $('<tr><td>&nbsp</td><td>&nbsp</td><td>&nbsp</td></tr>');
            table.append(row);

            // for each entry
            $.each(data['result']['definitions'], function(defKey) {
                
                //console.log('functional label: ' + data['result']['definitions'][defKey]['functional label']);
                var row = $('<tr><td colspan="3">' + data['result']['definitions'][defKey]['functional label'] + '(s)</td></tr>');
                table.append(row);

                // for each functional sense
                $.each(data['result']['definitions'][defKey]['senses'], function(senseKey) {

                    //console.log('functional label: ' + data['result']['definitions'][defKey]['senses'][senseKey]['definition']);
                    //console.log('functional label: ' + data['result']['definitions'][defKey]['senses'][senseKey]['example']);
                    var row = $('<tr><td colspan="1"></td><td>Definition</td>' + 
                                '<td colspan="1">' + data['result']['definitions'][defKey]['senses'][senseKey]['definition'] + '</td></tr>');
                    table.append(row);
                    var row = $('<tr><td colspan="1"></td><td>Example</td>' + 
                                '<td colspan="1">' + data['result']['definitions'][defKey]['senses'][senseKey]['example'] + '</td></tr>');
                    table.append(row);

                    $.each(data['result']['definitions'][defKey]['senses'][senseKey]['synonyms'], function(synKey, value) {
                        //console.log('syn: ' + value);
                        var row = $('<tr><td colspan="2"></td><td colspan="1">' + 
                                    data['result']['definitions'][defKey]['senses'][senseKey]['translated synonyms'][synKey] +
                                    '(' + data['result']['definitions'][defKey]['senses'][senseKey]['synonyms'][synKey] + ') </td></tr>');
                        table.append(row);
                    });
                    //$.each(data['result']['definitions'][defKey]['senses'][senseKey]['translated synonyms'], function(synKey, value) {
                    //    //console.log('transSyn: ' + value);
                    //    var row = $('<tr><td>' + value + '</td></tr>');
                    //    table.append(row);
                    //});
                    //console.log('key: ' + key2);
                    //console.log('value: ' + value2);

                    // for each sense
                    //$.each(data['result']['definitions'][defKey]['senses'][key2], function(key3, value3) {
                    //    console.log('key: ' + key3);
                    //    console.log('value: ' + value3);
                    //})
                    var row = '<tr><td colspan="3"></td></tr>';
                    table.append(row);
                })
            });
            $( "#results" ).html(table);
        });
    });
});
