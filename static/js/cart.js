var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateCartBadge(count) {
  var badge = document.getElementById("cart-total");
  if (badge) {
    badge.textContent = count;
  }
}

function getProductStockFromPage(productId) {
  // Try to find the product's stock from the page data
  // Look for a hidden element with stock info, or use the cart data
  var stockEl = document.querySelector(
    '[data-product-stock="' + productId + '"]',
  );
  if (stockEl) {
    return parseInt(stockEl.dataset.stock);
  }
  return null;
}

function addCookieItem(productId, action) {
  if (action == "add") {
    var currentQty = cart[productId] ? cart[productId]["quantity"] : 0;
    var newQty = currentQty + 1;

    // Try to get stock info from the page
    var productEl = document.querySelector(
      '[data-product="' + productId + '"][data-stock]',
    );
    if (productEl) {
      var stock = parseInt(productEl.dataset.stock);
      if (stock !== null && !isNaN(stock) && newQty > stock) {
        alert(
          "Only " +
            stock +
            " available in stock (you already have " +
            currentQty +
            " in cart).",
        );
        return;
      }
    }

    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;
    if (cart[productId]["quantity"] <= 0) {
      delete cart[productId];
    }
  }

  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

  // Update badge from cookie data
  var totalItems = 0;
  for (var key in cart) {
    totalItems += cart[key]["quantity"];
  }
  updateCartBadge(totalItems);

  // Reload if on cart page to reflect item changes
  if (window.location.pathname.includes("/cart")) {
    location.reload();
  }
}

function updateUserOrder(productId, action) {
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }
      updateCartBadge(data.cartItems);
      // Reload if on cart page to reflect item/price changes
      if (window.location.pathname.includes("/cart")) {
        location.reload();
      }
    })
    .catch((error) => {
      alert("An error occurred. Please try again.");
    });
}
