document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var curr_user = "";

    // When connected, configure message button
    socket.on('connect', () => {


        //get current user from html

        curr_user = window.localStorage.getItem("curr_user")

        if (!curr_user) {

            window.localStorage.setItem("curr_channel", "home");
            curr_user = prompt("Please enter a username");

            socket.emit('new user', { 'curr_user': curr_user, 'texts': "no" });
        } else {
            socket.emit('new user', { 'curr_user': curr_user, 'texts': "yes" });
        }




        //allow submit with enter key
        document.getElementById("message")
            .addEventListener("keyup", function (event) {
                event.preventDefault();
                if (event.keyCode === 13) {
                    document.getElementById("button-send").click();
                }
            });

        // Button should emit a "submit message" event
        function submitclick() {
            const message = document.getElementById("message").value;
            document.getElementById('message').value = '';
            curr_user = document.getElementById("the-name").textContent;
            curr_channel = document.getElementById("channel-id").innerHTML;
            socket.emit('submit message', { 'message': message, 'curr_user': curr_user, 'curr_channel': curr_channel });
        }
        document.getElementById("button-send").addEventListener("click", submitclick);

        //create channel action button
        function channelcreate() {
            chan_name = prompt("Type in a channel name");
            socket.emit('create channel', { 'chan_name': chan_name });
        }
        document.getElementById("channel-button").addEventListener("click", channelcreate);


        // If hide button is clicked, delete the post.
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.className === 'hide') {
                var parent = element.parentElement.innerHTML
                element.parentElement.style.animationPlayState = 'running';
                element.parentElement.addEventListener('animationend', () => {
                    element.parentElement.remove();
                    var chan_id = document.getElementById("channel-id").innerHTML
                    user = window.localStorage.getItem("curr_user")
                    //prompt(parent)
                    socket.emit("delete", { "text": parent, "curr_channel": chan_id, "curr_user": user })
                });
            }
        });
        //when a channel button is clicked
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.className === 'chan_name') {
                const text = element.innerHTML;

                socket.emit('change channel', { "chan": text })
            }
        });

        //when clear button is clicked
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.className === 'clear') {
                localStorage.clear();
                window.location.reload();
            }
        });

        //when create button is clicked
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.className === 'create') {
                curr_user = prompt("Please enter a username");
                socket.emit('new user', { 'curr_user': curr_user, 'texts': "no" });
            }
        });

    });

    //initial start up or on page reload.
    window.onload = function () {
        var curr_user = window.localStorage.getItem("curr_user")
        if (curr_user == null || curr_user == undefined) {
            curr_user = "default"
        }
        var curr_channel = window.localStorage.getItem("curr_channel")
        if (curr_channel == null || curr_channel == undefined) {
            curr_channel = "home"
        }
        socket.emit('start up', { "curr_channel": curr_channel, "curr_user": curr_user });
    };




    //don't allow two people to have the same username.
    socket.on('create user', data => {
        var mess = data.mess;
        var curr_user = data.curr_user;
        if (mess == "false") {
            user = prompt("Username already taken please enter a different name.");
            socket.emit('new user', { 'curr_user': user })
        } else if (mess == "true") {
            if (curr_user != "") { //display the username
                window.localStorage.setItem("curr_user", curr_user)
                document.getElementById("the-name").innerHTML = data.curr_user;

                //call change channel here so that messages are updated when user is switched
                chan = window.localStorage.getItem("curr_channel")
                socket.emit("change channel", { "chan": chan })

            }

        }
    });

    //update the channel list
    socket.on('update channels', data => {
        var chans = data.channel_names;
        document.getElementById('channels-list').innerHTML = '';

        for (chan = 0; chan < chans.length; chan++) {
            const li = document.createElement('li');
            li.innerHTML = `<button class="chan_name">${chans[chan]}</button>`;
            document.querySelector('#channels-list').append(li);
        }

    });

    socket.on("fix delete", data => {
        var current_channel = data.curr_channel;
        var current_user = data.curr_user;
        var channels = data.channels;
        var this_chan = channels[current_channel];
        document.getElementById("channel-id").innerHTML = `${current_channel}`;
        document.getElementById('messages').innerHTML = '';
        for (chan = 0; chan < this_chan.length; chan++) {
            const li = document.createElement('li');
            li.classList.add("post");
            var message = ""
            if (this_chan[chan][0] == current_user) {
                message = "<button class='hide'>Delete</button>"
            }
            li.innerHTML = `${this_chan[chan][1]}${message}`;
            document.querySelector('#messages').append(li);
        }

    });


    //update the messages generic
    socket.on('update messages', data => {
        var current_channel = data.curr_channel;

        var current_user = window.localStorage.getItem("curr_user")
        var channels = data.channels;
        var this_chan = channels[current_channel];
        document.getElementById("channel-id").innerHTML = `${current_channel}`;
        document.getElementById('messages').innerHTML = '';
        for (chan = 0; chan < this_chan.length; chan++) {
            const li = document.createElement('li');
            li.classList.add("post");
            var message = ""
            if (this_chan[chan][0] == current_user) {
                message = "<button class='hide'>Delete</button>"
            }
            li.innerHTML = `${this_chan[chan][1]}${message}`;
            document.querySelector('#messages').append(li);
        }

    });

    //update the messages when changing channels
    socket.on('update messages channel', data => {
        var current_channel = data.curr_channel;
        window.localStorage.setItem("curr_channel", current_channel);
        var current_user = window.localStorage.getItem("curr_user")
        var channels = data.channels;
        var this_chan = channels[current_channel];
        document.getElementById("channel-id").innerHTML = `${current_channel}`;
        document.getElementById('messages').innerHTML = '';
        for (chan = 0; chan < this_chan.length; chan++) {
            const li = document.createElement('li');
            li.classList.add("post");
            var message = ""
            if (this_chan[chan][0] == current_user) {
                message = "<button class='hide'>Delete</button>"
            }
            li.innerHTML = `${this_chan[chan][1]}${message}`;
            document.querySelector('#messages').append(li);
        }

    });



    function updateScroll() {
        var element = document.getElementById("message-cont");
        element.scrollTop = element.scrollHeight;
    }
    // When a new message is announced, add to the unordered list
    socket.on('announce message', data => {
        var current_channel = window.localStorage.getItem("curr_channel")
        var sent_channel = data.curr_channel
        if (current_channel == sent_channel) {
            var current_user = data.curr_user
            const li = document.createElement('li');
            li.classList.add("post");
            var this_user = document.getElementById("the-name").innerHTML
            var message = ""
            if (this_user == current_user) {
                message = "<button class='hide'>Delete</button>"
            }
            li.innerHTML = `${data.message}${message}`;
            document.querySelector('#messages').append(li);
            updateScroll()
        }

    });



});