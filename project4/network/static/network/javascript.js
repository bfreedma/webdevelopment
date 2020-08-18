document.addEventListener('DOMContentLoaded', function () {
    //editing
    document.querySelectorAll('.edit').forEach(button =>
        button.onclick = function () {
            if (this.innerHTML === "edit") {
                this.innerHTML = "save";
                card = this.closest(".card");
                card_text = card.getElementsByClassName("card-text")[0]
                text = card_text.innerHTML;
                box = document.createElement('textarea');
                box.className += "form-control";
                box.innerHTML = text;
                card_text.replaceWith(box);
            } else {
                this.innerHTML = "edit";
                //to get inner html data you need .dataset before data name
                id = this.dataset.id
                card = this.closest(".card");
                card_form = card.getElementsByClassName("form-control")[0];
                //need to use .value instead of .innerhtml for text areas
                plain_text = card_form.value;
                text = document.createElement('p')
                text.className += "card-text"
                text.innerHTML = plain_text
                card_form.replaceWith(text)
                var data = new FormData();
                data.append('text', plain_text);
                data.append('id', id);
                data.append('csrfmiddlewaretoken', csrftoken)

                fetch('/edit', {
                    credentials: 'same-origin',
                    method: 'POST',
                    body: data
                })
            }
        });

    //liking
    document.querySelectorAll('.like').forEach(button =>
        button.onclick = function () {
            if (this.innerHTML === "like") {
                this.innerHTML = "unlike";
                this.classList.remove("btn-primary")
                this.classList.add("btn-warning")
                id = this.dataset.id
                card = this.closest(".card");
                liketotal = card.getElementsByClassName("likecount")[0];
                liketotal.innerHTML = parseInt(liketotal.innerHTML) + 1;
                var data = new FormData();
                var like = true
                data.append('like', like);
                data.append('id', id);
                data.append('csrfmiddlewaretoken', csrftoken)

                fetch('/like', {
                    credentials: 'same-origin',
                    method: 'POST',
                    body: data
                })

            } else {
                this.innerHTML = "like";
                this.classList.remove("btn-warning")
                this.classList.add("btn-primary")
                id = this.dataset.id
                card = this.closest(".card");
                liketotal = card.getElementsByClassName("likecount")[0];
                liketotal.innerHTML = parseInt(liketotal.innerHTML) - 1;
                var data = new FormData();
                var like = false
                data.append('like', like);
                data.append('id', id);
                data.append('csrfmiddlewaretoken', csrftoken)

                fetch('/like', {
                    credentials: 'same-origin',
                    method: 'POST',
                    body: data
                })
            }
        });
});