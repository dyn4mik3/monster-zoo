/**
 * Created by michael on 1/26/15.
 */

$(function () {

    // Important variables to hold data for the game
    var player_id;
    var player_position;
    var turn;
    var gameroom_id;

    // Connect to SocketIO
    socket = io.connect('/game');

    // Console logging through 'alert' message
    socket.on('alert', function (msg) {
        console.log(msg);
    });

    // Sends user a redirect to their browser
    socket.on('redirect', function (data) {
        window.location = data.url;
    });

    // Received Server Connection
    // Join game room
    socket.on('connected', function (data) {
        var url_parts = window.location.pathname.split('/');
        gameroom_id = url_parts[2]
        console.log('Game ID: ' + gameroom_id);
        player_id = data['player_id']
        console.log('Player ID:' + player_id + ' has connected.');
        socket.emit('game_connect', {'player_id': player_id, 'gameroom_id': gameroom_id});
    });

    socket.on('host', function(data) {
        $('#waiting-modal').modal('show');
        console.log('Open waiting-modal');
    });

    socket.on('game_start', function (data) {
        console.log('Received game_start signal from server.');
        socket.emit('get_game_state', {'player_id': player_id, 'gameroom_id': gameroom_id});
        $('#waiting-modal').modal('hide');
    });

    socket.on('render_state', function (data) {
        console.log('Received render_state signal from server.');
        clear_render(function () {
            render_game(data);
        });
    });

    socket.on('player_position', function (data) {
        // Set the player position variable
        player_position = data.position;
        console.log('My player position is: ' + player_position);
    })

    function clear_render(callback) {
        // Wipe the render clean. Note this could be optimized to only wipe out portions of the board
        // that need updating. Add a callback so this is done before rendering starts.
        $('#wild').empty();
        $('#player1').empty();
        $('#player2').empty();
        if (callback && typeof(callback) == "function") {
            callback();
        }
    }

    function render_game(data) {
        // Data is passed as JSON, so we need to convert it to a Javascript object before using it.
        var game_data = JSON.parse(data);

        // Render all the wild cards
        render_wild(game_data.wild.hand);

        // Render all the player cards
        var players = game_data.players;
        var players_length = game_data.players.length;
        for (var i = 0; i < players_length; i++) {
            // iterate through all the players
            var player = players[i];
            render_player_cards(player, player.hand.cards);
        }

        // Render all the player stats
        render_players_stats(game_data.players);

        // Render all the current player buttons
        render_play_buttons(game_data.current_player);

    }

    function render_player_cards(player, cards) {
        var card_count = cards.length;
        if (player.player_id == player_id) {
            // Render face up if player_id match
            for (var c = 0; c < card_count; c++) {
                console.log('Face up card');
                render_card_face_up(player.player_id, cards[c], c)
            }
        }
        else {
            // Render face down if player_id match
            for (var c = 0; c < card_count; c++) {
                console.log('Face down card');
                render_card_face_down(player.player_id, cards[c], c)
            }
        }
    }

    function render_card_face_up(player, card, index_location) {
        var card_family = card.family;
        var card_name = card.name;
        var card_cost = card.cost;
        var card_image = card.image;
        var card_text = card.description;

        if (card_family == 'Boogly') {
            var card_class = '<div class="card booglyback" ';
        }
        else if (card_family == 'Oogly') {
            var card_class = '<div class="card ooglyback" ';
        }
        else if (card_family == 'Zoogly') {
            var card_class = '<div class="card zooglyback" ';
        }
        else if (card_family == 'Food') {
            var card_class = '<div class="card foodback" ';
        }
        else {
            var card_class = '<div class="card" ';
        }
        var card_back = '<div class="card cardback" style="background-color:#f79a2f;"><div class="corner top_left"><span class="number">' +
        '</span></div><div class="corner top_right"><span class="number">' +
        '</span></div><div class="card_image"><p><img src="/static/images/Logo.png" height="80px"></p>' +
        '</div>' +
        '</div>';

        var card_layout = card_class + 'id="player1card' + index_location +
        '"><div class="corner top_right"><span class="number">' + card_cost +
        '</span></div><div class="corner top_left"><span class="number">' + card_name +
        '</span></div><div class="card_image"><p><img src="' + card_image +
        '" height="80px"></p>' + card_text +
        '</div>' +
        '<div class="playbutton">' +
        '<button type="button" ' +
        'name="' + index_location +
        '" class="btn btn-primary btn-xs play-this">Play This Card</button>' +
        '</div></div>';

            console.log('Rendering card face up.');
            $('#player1').append(card_layout);
    }

    function render_card_face_down(player, card, index_location) {
        var card_family = card.family;
        var card_name = card.name;
        var card_cost = card.cost;
        var card_image = card.image;
        var card_text = card.description;

        if (card_family == 'Boogly') {
            var card_class = '<div class="card booglyback" ';
        }
        else if (card_family == 'Oogly') {
            var card_class = '<div class="card ooglyback" ';
        }
        else if (card_family == 'Zoogly') {
            var card_class = '<div class="card zooglyback" ';
        }
        else if (card_family == 'Food') {
            var card_class = '<div class="card foodback" ';
        }
        else {
            var card_class = '<div class="card" ';
        }
        var card_back = '<div class="card cardback" style="background-color:#f79a2f;"><div class="corner top_left"><span class="number">' +
        '</span></div><div class="corner top_right"><span class="number">' +
        '</span></div><div class="card_image"><p><img src="/static/images/Logo.png" height="80px"></p>' +
        '</div>' +
        '</div>';

        var card_layout = card_class + 'id="player1card' + index_location +
        '"><div class="corner top_right"><span class="number">' + card_cost +
        '</span></div><div class="corner top_left"><span class="number">' + card_name +
        '</span></div><div class="card_image"><p><img src="' + card_image +
        '" height="80px"></p>' + card_text +
        '</div>' +
        '<div class="playbutton">' +
        '<button type="button" ' +
        'name="' + index_location +
        '" class="btn btn-primary btn-xs play-this">Play This Card</button>' +
        '</div></div>';

            console.log('Rendering card face down.');
            $('#player2').append(card_back);
    }

    function render_play_buttons(current_player) {
        if (current_player.player_id == player_id) {
            console.log('This is my turn');
            turn = true;
            $('.btn').hide(); // hide all buttons
            $('#turn-player1').show(); // show the "end turn" button
            $('#discard-player1').show();
            $('#player1 .play-this').show(); // show the "play this card" buttons
        }
        else {
            console.log('not my turn');
            turn = false;
            $('#turn-player1').hide();
            $('#discard-player1').hide();
            $('.btn').hide();
        }
        ;
    }

    function render_players_stats(data) {
        var players_length = data.length;
        for (var i = 0; i < players_length; i++) {
            if (data[i].player_id == player_id) {
                console.log('Player Match');
                $('#player1-food').html(data[i].food);
            }
        }
    }

    function render_wild(data) {
        // Assign wild_deck cards to cards array
        console.log(data);
        var cards = data.cards;
        var cards_length = cards.length;
        // Loop through cards array and get data
        for (var i = 0; i < cards_length; i++) {
            console.log(cards[i].name);
            // render card on client
            render_wild_card(cards[i], i);
        }
    }

    function render_wild_card(data, index_location) {
        // Index location comes from cards array in the render function
        var card_name = data.name;
        var card_cost = data.cost;
        var card_image = data.image;
        var card_text = data.description;

        var button = '<button type="button" ' + 'id="wild' + index_location + '" ' +
            'name="' + index_location + '" class="btn btn-primary btn-xs buy-this">Buy This Card</button>';
        var card_layout = '<div class="card"><div class="corner top_right"><span class="number">' + card_cost +
            '</span></div><div class="corner top_left"><span class="number">' + card_name +
            '</span></div><div class="card_image"><p><img src="' + card_image +
            '" height="80px"></p>' + card_text +
            '</div><div class="playbutton">';

        var close_div = '</div></div>';

        var food = $('#player1-food').html();

        if (food >= card_cost && turn == true) {
            card_layout = card_layout + button + close_div;
        }
        else {
            card_layout = card_layout + close_div;
        }
        $('#wild').append(card_layout);
    }

    // Bind to deal button
    $('#deal-player1').click(function () {
        socket.emit('deal', socket.socket.sessionid);
    });

    // Bind to end turn button
    $('#turn-player1').click(function () {
        console.log('Clicked #turn-player1');
        console.log(gameroom_id);
        socket.emit('end_turn', {'gameroom_id': gameroom_id});
    });

    // Bind to discard end turn button
    $('#discard-player1').click(function () {
        $('#player1-zoo .playbutton .btn').hide();
        $('#player1 .playbutton .btn').show();
        $('#player1 .play-this').html('Discard');
        $('#player1 .playbutton .btn').toggleClass('play-this discard-this');
        $('#player1 .playbutton .btn').toggleClass('btn-default btn-info');
        $('#discard-player1').hide();
    });

    // Bind to discard this buttons
    $('.row').on('click', '#player1 .discard-this', function (event) {
        socket.emit('discard', this.name);
    });

    // Bind the card play this buttons
    $('.row').on('click', '#player1 .play-this', function (event) {
        console.log(this.name);
        console.log("Clicked on a play this button.");
        socket.emit('play', this.name);
    });

    // Bind the select card buttons
    $('.row').on('click', '#player1 .pick-this', function (event) {
        console.log("Clicked on a pick this button.");
        socket.emit('selected_card', this.name);
    });

    // Bind the select card zoo buttons
    $('.row').on('click', '#player1-zoo .pick-this', function (event) {
        console.log("Clicked on a pick this button in the Zoo.");
        socket.emit('selected_card_from_zoo', this.name);
    });

    // Bind the select card other zoo buttons
    $('.row').on('click', '#player2-zoo .pick-this', function (event) {
        console.log("Clicked on a pick this button in the Zoo.");
        socket.emit('selected_card_from_other_zoo', this.name);
    });

    // Bind the select card zoo buttons
    $('.row').on('click', '#wild .select-this', function (event) {
        console.log("Clicked on a pick this button in the Wild.");
        socket.emit('selected_card_from_wild', this.name);
    });

    // Bind the card buy this buttons
    $('.row').on('click', '.buy-this', function (event) {
        socket.emit('buy', this.name);
    });

    // Bind the card buy this buttons
    $('.row').on('click', '.remodel-this', function (event) {
        socket.emit('remodel', this.name);
    });

    /* OLD CODE

     // Load up the login modal
     $('#login-modal').modal('show');

     // Bind to login form
     $('#login').submit(function() {
     socket.emit('login', $('#username').val(), function(set) {
     if (set) {
     clear();
     return $('#chat').addClass('nickname-set');
     }
     });
     $('#login').css('visibility','hidden');
     $('#login-modal').modal('hide');
     return false;
     });

     // Bind to send message form
     $('#send-message').submit(function() {
     socket.emit('user message', $('#message').val());
     $('#message').val('').focus();
     // $('#lines').get(0).scrollTop =100000000000;
     setTimeout(function() {
     $("#lines").scrollTop($("#lines")[0].scrollHeight);
     }, 10);
     return false;
     });

     function clear () {
     $('message').val('').focus();
     };

     // Bind to deal button
     $('#deal-player1').click(function() {
     socket.emit('deal', socket.socket.sessionid );
     });

     // Bind to end turn button
     $('#turn-player1').click(function() {
     socket.emit('turn');
     });

     // Bind to discard end turn button
     $('#discard-player1').click(function() {
     $('#player1-zoo .playbutton .btn').hide();
     $('#player1 .playbutton .btn').show();
     $('#player1 .play-this').html('Discard');
     $('#player1 .playbutton .btn').toggleClass('play-this discard-this');
     $('#player1 .playbutton .btn').toggleClass('btn-default btn-info');
     $('#discard-player1').hide();
     });

     // Bind to discard this buttons
     $('.row').on('click', '#player1 .discard-this', function(event) {
     socket.emit('discard', this.name);
     });

     // Bind the card play this buttons
     $('.row').on('click', '#player1 .play-this', function(event) {
     console.log(this.name);
     console.log("Clicked on a play this button.");
     socket.emit('play', this.name);
     });

     // Bind the select card buttons
     $('.row').on('click', '#player1 .pick-this', function(event) {
     console.log("Clicked on a pick this button.");
     socket.emit('selected_card', this.name);
     });

     // Bind the select card zoo buttons
     $('.row').on('click', '#player1-zoo .pick-this', function(event) {
     console.log("Clicked on a pick this button in the Zoo.");
     socket.emit('selected_card_from_zoo', this.name);
     });

     // Bind the select card other zoo buttons
     $('.row').on('click', '#player2-zoo .pick-this', function(event) {
     console.log("Clicked on a pick this button in the Zoo.");
     socket.emit('selected_card_from_other_zoo', this.name);
     });

     // Bind the select card zoo buttons
     $('.row').on('click', '#wild .select-this', function(event) {
     console.log("Clicked on a pick this button in the Wild.");
     socket.emit('selected_card_from_wild', this.name);
     });

     // Bind the card buy this buttons
     $('.row').on('click', '.buy-this', function(event) {
     socket.emit('buy', this.name);
     });

     // Bind the card buy this buttons
     $('.row').on('click', '.remodel-this', function(event) {
     socket.emit('remodel', this.name);
     });
     */
});
