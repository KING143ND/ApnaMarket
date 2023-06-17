$('#slider1, #slider2, #slider3, #slider4, #slider5').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: true,
            autoplay: true,
        },
        
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

function prev() {
    document.getElementById('slider-container').scrollLeft -= 270;
}

function next() {
    document.getElementById('slider-container').scrollLeft += 270;
}

function loginpassword() {
    var password = document.getElementById("loginpassword");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

function pass1() {
    var password = document.getElementById("pass1");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

function pass2() {
    var password = document.getElementById("pass2");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
    alertTrigger.addEventListener('click', () => {
        appendAlert('Nice, you triggered this alert message!', 'success')
    })
}