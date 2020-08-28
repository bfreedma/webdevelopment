document.addEventListener('DOMContentLoaded', function () {

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

                fetch('/cookbook/like', {
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

                fetch('/cookbook/like', {
                    credentials: 'same-origin',
                    method: 'POST',
                    body: data
                })
            }
        });


    //edit review
    document.querySelectorAll('.edit').forEach(button =>
        button.onclick = function () {
            if (this.innerHTML === "edit") {
                this.innerHTML = "save";
                card = this.closest(".card");
                card_text = card.getElementsByClassName("card-text")[0]
                finished_rating = card.getElementsByClassName("finished-rating")[0]
                text = card_text.innerHTML;
                div_stars = document.createElement("div")
                div_stars.className += "rate button_example finished-rating"
                div_inner = div_stars.innerHTML
                div_inner = document.getElementById('blockOfreview').innerHTML;
                div_stars.innerHTML = div_inner
                finished_rating.replaceWith(div_stars)
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


                rating_form = card.getElementsByClassName("finished-rating")[0];
                rate_element = document.getElementsByName('rate')

                new_stars = document.createElement('div')
                new_stars.className += "finished-rating"
                for (i = 0; i < rate_element.length; i++) {
                    if (rate_element[i].checked)
                        rate_value = rate_element[i].value;
                }
                if (rate_value == 1) {
                    div_inner = document.getElementById('blockofrating1').innerHTML;
                } else if (rate_value == 2) {
                    div_inner = document.getElementById('blockofrating2').innerHTML;
                } else if (rate_value == 3) {
                    div_inner = document.getElementById('blockofrating3').innerHTML;
                } else if (rate_value == 4) {
                    div_inner = document.getElementById('blockofrating4').innerHTML;
                } else if (rate_value == 5) {
                    div_inner = document.getElementById('blockofrating5').innerHTML;
                }


                new_stars.innerHTML = div_inner
                rating_form.replaceWith(new_stars);
                var data = new FormData();
                data.append('text', plain_text);
                data.append('id', id);
                data.append("rate", rate_value);
                data.append('csrfmiddlewaretoken', csrftoken)

                fetch('/cookbook/editreview', {
                    credentials: 'same-origin',
                    method: 'POST',
                    body: data
                })
            }
        });










});