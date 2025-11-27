document.addEventListener("DOMContentLoaded", function () {
  const products = [];
  const wrappers = document.querySelectorAll(".product-card-wrapper");
  const choosenProducts = document.getElementById("choosen-products");

  // Function to render chosen products
  function renderChoosenProducts() {
    choosenProducts.innerHTML = "";

    if (products.length === 0) {
      choosenProducts.innerHTML =
        '<p class="text-center text-base-content/50 py-4">لم يتم اختيار منتجات بعد</p>';
      return;
    }

    products.forEach((product, index) => {
      const productCard = document.createElement("div");
      productCard.className =
        "flex justify-between items-center p-3 bg-base-100 rounded-lg mb-2 hover:bg-base-200 transition-all";
      productCard.innerHTML = `
                <div class="flex-1">
                    <h4 class="font-semibold text-sm">${product.name}</h4>
                    <p class="text-xs text-base-content/70">${product.price.toFixed(
                      2
                    )} ج.س</p>
                </div>
                <div class="flex items-center gap-2">
                    <input type="number" value="${product.quantity}" min="1" 
                           class="input input-bordered input-xs w-16 text-center chosen-quantity" 
                           data-index="${index}">
                    <button class="btn btn-xs btn-error btn-circle remove-product" data-index="${index}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            `;
      choosenProducts.appendChild(productCard);
    });

    // Add event listeners for quantity changes
    document.querySelectorAll(".chosen-quantity").forEach((input) => {
      input.addEventListener("change", function () {
        const index = parseInt(this.getAttribute("data-index"));
        const newQuantity = parseInt(this.value);
        if (newQuantity > 0) {
          products[index].quantity = newQuantity;
        }
      });
    });

    // Add event listeners for remove buttons
    document.querySelectorAll(".remove-product").forEach((btn) => {
      btn.addEventListener("click", function () {
        const index = parseInt(this.getAttribute("data-index"));
        products.splice(index, 1);
        renderChoosenProducts();
      });
    });
  }

  wrappers.forEach((wrapper) => {
    const frontCard = wrapper.querySelector(".front-card");

    if (frontCard) {
      // Toggle product selection on click
      frontCard.addEventListener("click", function () {
        const productInput = frontCard.querySelector(".product-id");
        const productId = productInput.value;
        const productName = productInput.name;
        const productPrice = parseFloat(productInput.getAttribute("price"));
        console.log(productPrice);

        if (products.some((p) => p.id === productId)) {
          // Product already exists, increment quantity
          const index = products.findIndex((p) => p.id === productId);
          products[index].quantity++;
        } else {
          // Add new product
          products.push({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: 1,
          });
        }

        // Update the chosen products display
        renderChoosenProducts();
      });
    }
  });

  // Checkout Button Logic
  const checkoutBtn = document.getElementById("checkout-button");
  const checkoutForm = document.getElementById("checkout-form");
  const closeBtn = document.getElementById("close-checkout");
  const productsBody = document.getElementById("products-body");
  const grandTotalEl = document.getElementById("grand-total");

  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent form submission if button is inside form

      // Clear existing rows
      productsBody.innerHTML = "";
      let grandTotal = 0;

      products.forEach((product, index) => {
        const row = document.createElement("tr");
        const total = product.price * product.quantity;
        grandTotal += total;

        row.innerHTML = `
                    <input type="hidden" name="product_id" value="${
                      product.id
                    }">
                    <td style="text-align: right;">${product.name}</td>
                    <td style="text-align: center;">${product.price.toFixed(
                      2
                    )} ج.س</td>
                    <td style="text-align: center;">${product.quantity}</td>
                    <td style="text-align: center;" class="row-total">${total.toFixed(
                      2
                    )} ج.س</td>
                `;
        productsBody.appendChild(row);
      });

      grandTotalEl.textContent = `${grandTotal.toFixed(2)} ج.س`;

      checkoutForm.classList.remove("hidden");
    });
  }

  // Close Modal Logic
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      checkoutForm.classList.add("hidden");
    });
  }

  // Close on click outside
  if (checkoutForm) {
    checkoutForm.addEventListener("click", function (e) {
      if (e.target === checkoutForm) {
        checkoutForm.classList.add("hidden");
      }
    });
  }

  // Handle Quantity Changes in Modal
  if (productsBody) {
    productsBody.addEventListener("change", function (e) {
      if (e.target.classList.contains("quantity-input")) {
        const index = e.target.getAttribute("data-index");
        const newQuantity = parseInt(e.target.value);

        if (newQuantity > 0) {
          products[index].quantity = newQuantity;

          // Update row total
          const row = e.target.closest("tr");
          const rowTotalEl = row.querySelector(".row-total");
          const newRowTotal = products[index].price * newQuantity;
          rowTotalEl.textContent = `${newRowTotal.toFixed(2)} ج.س`;

          // Update Grand Total
          let newGrandTotal = 0;
          products.forEach((p) => {
            newGrandTotal += p.price * p.quantity;
          });
          grandTotalEl.textContent = `${newGrandTotal.toFixed(2)} ج.س`;
        }
      }
    });
  }

  // Print Receipt Logic
  const printBtn = document.getElementById("print-receipt-btn");
  if (printBtn) {
    printBtn.addEventListener("click", function (e) {
      e.preventDefault();

      // Get form data
      const formData = new FormData(checkoutForm);
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      // Submit transaction to backend
      fetch(window.location.href, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {
          if (response.ok) {
            // Transaction saved successfully, now print
            printJS({
              printable: "printable-checkout",
              type: "html",
              scanStyles: true,
              targetStyles: ["*"],

              style: `
        /* ========================================================= */
        /* 1. FONT & PAGE CONFIGURATION */
        /* ========================================================= */
        *{
            direction: rtl; 
            /* Ensure the font is defined first */
            font-family: 'Cairo', sans-serif; 
        }

        /* 80mm Receipt Size Configuration */
        @page { 
            size: 80mm auto;
            margin: 0;
        }
        
        /* Main Content Wrapper - ADDING BORDER AROUND RECEIPT */
        #printable-checkout {
            width: 80mm;
            padding: 0 4mm;
            box-sizing: border-box;
            font-size: 10pt;
            border: 1px solid #000; /* BORDER ADDED: Full border around the receipt content */
        }

        /* ========================================================= */
        /* 2. TABLE AND BORDER STYLES */
        /* ========================================================= */
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 5px 0;
            border-top: 1px solid #000; /* Top Border for the table */
            border-bottom: 1px solid #000; /* Bottom Border for the table */
        }
        
        table th, table td { 
            /* Use dashed lines for internal separation, and remove the bottom border defined previously */
            border-bottom: none; 
            padding: 4px 0; 
            text-align: right; 
            color: #000; 
        }
        
        /* Separate the header from the body with a line */
        table thead tr {
            border-bottom: 1px solid #000; 
        }
        
        table tfoot td { 
            font-weight: bold; 
            font-size: 11pt;
            padding-top: 8px;
            border-top: 2px solid #000; /* BORDER ADDED: Thick line to separate totals */
        }

        /* ========================================================= */
        /* 3. CLEANUP & HIDING WEB ELEMENTS */
        /* ========================================================= */
        #close-checkout, .modal-action { display: none !important; } 
        .modal-box { 
            box-shadow: none !important; 
            border: none !important; 
            width: 100% !important; 
            max-width: 100% !important; 
            padding: 0 !important; 
        }
        input { display: none !important; }
        .text-primary { color: #000 !important; }
        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        input[type="number"] {
            -moz-appearance: textfield;
        }`,
              onPrintDialogClose: function () {
                // Close modal and reset after printing
                checkoutForm.classList.add("hidden");
                productsBody.innerHTML = "";
                products.length = 0;
                // Remove active state from all cards
                document
                  .querySelectorAll(".front-card.active")
                  .forEach((card) => {
                    card.classList.remove("active");
                  });
              },
            });
          } else {
            alert("Error saving transaction. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Error saving transaction. Please try again.");
        });
    });
  }
});
