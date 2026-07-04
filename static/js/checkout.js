document.addEventListener("DOMContentLoaded", function () {

    const zone = document.getElementById("id_delivery_zone");

    if (!zone) return;

const checkoutPage = document.querySelector(".checkout-page");

const subtotal = Number(
    checkoutPage.dataset.subtotal
);

    zone.addEventListener("change", function () {

        fetch(`/orders/delivery-fee/${this.value}/`)

            .then(response => response.json())

            .then(data => {

                document.getElementById("delivery-fee").innerHTML =
                    "KSh " + data.fee;

                document.getElementById("grand-total").innerHTML =
                    "KSh " + (subtotal + data.fee);

            });

    });

});