"""
Fake Store Product Browser
===========================
A simple Streamlit app that fetches products from the Fake Store API
(https://fakestoreapi.com/products) and lets the user browse and filter
them by category, maximum price, and a text search on the product title.

Streamlit apps work by re-running this entire script from top to bottom
every time the user interacts with a widget (e.g. moves a slider, types
in a text box). Keep that in mind as you read through - each "run" is a
fresh pass through the code below.
"""

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# SECTION 0: PAGE CONFIG
# ---------------------------------------------------------------------------
# st.set_page_config() must be the first Streamlit command that runs. It
# controls high-level page settings like the browser tab title and layout.
# "wide" layout gives us more horizontal space, which is nice for showing
# product images and details side by side.
st.set_page_config(page_title="Fake Store Product Browser", layout="wide")

st.title("🛍️ Fake Store Product Browser")
st.caption("Browse and filter products fetched live from the Fake Store API.")


# ---------------------------------------------------------------------------
# SECTION 1: DATA FETCHING
# ---------------------------------------------------------------------------
# We wrap the API call in a function decorated with @st.cache_data.
# Why cache? Without it, every single widget interaction (moving the slider,
# typing a letter in search, etc.) would re-run this script AND re-fetch
# the data from the internet again, which is slow and unnecessary since the
# product data doesn't change every second. @st.cache_data tells Streamlit
# to remember the result and reuse it on future re-runs, only calling the
# real function again if the code changes or the cache expires.
@st.cache_data(ttl=600)  # cache the result for 10 minutes (600 seconds)
def fetch_products():
    """
    Fetch the list of products from the Fake Store API.

    Returns:
        A list of product dictionaries on success, or None if the
        request failed for any reason (network error, bad status code, etc.).
    """
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=10)
        # raise_for_status() raises an exception if the server responded
        # with an error status code (like 404 or 500), which we catch below.
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        # This catches connection errors, timeouts, bad status codes, etc.
        # We return None so the calling code can handle the failure cleanly
        # instead of letting the app crash with a traceback.
        return None


# st.spinner() shows a small "loading" animation with the given message
# for as long as the code inside the `with` block is running. Since
# fetch_products() might take a moment (it's a network call), this gives
# the user visual feedback that something is happening.
with st.spinner("Loading products..."):
    products = fetch_products()

# If the fetch failed, show an error message and stop the app here.
# st.stop() halts execution of the script at this point, so none of the
# code below (which assumes `products` is a valid list) will run.
if products is None:
    st.error("Failed to load products")
    st.stop()


# ---------------------------------------------------------------------------
# SECTION 2: SIDEBAR FILTERS
# ---------------------------------------------------------------------------
# st.sidebar puts widgets in a collapsible panel on the left side of the
# app, which is a common pattern for keeping filter controls out of the
# way of the main content area.
st.sidebar.header("Filters")

# --- Category filter -------------------------------------------------------
# Build the list of available categories dynamically from the fetched data,
# rather than hardcoding them, so the filter always matches what the API
# actually returned. set(...) removes duplicates, and sorted(...) puts them
# in a predictable alphabetical order.
categories = sorted({product["category"] for product in products})

# We add an "All" option at the front so the user can choose to see every
# category at once. st.selectbox() shows a dropdown; the value the user
# picks is returned and stored in `selected_category`.
selected_category = st.sidebar.selectbox("Category", options=["All"] + categories)

# --- Maximum price filter ---------------------------------------------------
# Determine sensible slider bounds from the actual product prices, rounding
# the max up so every product is reachable by the slider.
min_price = 0.0
max_price = float(max(product["price"] for product in products))

# st.slider() lets the user pick a single numeric value by dragging a
# handle between min_price and max_price. We default it to the highest
# price so that, initially, no products are filtered out by price.
max_price_filter = st.sidebar.slider(
    "Maximum Price",
    min_value=min_price,
    max_value=max_price,
    value=max_price,
    step=1.0,
)

# --- Search filter -----------------------------------------------------------
# st.text_input() gives the user a free-text box. We'll use whatever they
# type to filter product titles below. An empty string (the default) means
# "no search filter applied".
search_term = st.sidebar.text_input("Search", placeholder="Search by product title...")


# ---------------------------------------------------------------------------
# SECTION 3: FILTERING LOGIC
# ---------------------------------------------------------------------------
# Now we combine all three filters together. A product is only kept if it
# passes ALL three checks (category AND max price AND search term) - this
# is what makes the filters work together rather than independently.
def matches_filters(product):
    # Category check: pass automatically if "All" is selected, otherwise
    # the product's category must match exactly.
    category_ok = (selected_category == "All") or (product["category"] == selected_category)

    # Price check: the product's price must not exceed the slider's value.
    price_ok = product["price"] <= max_price_filter

    # Search check: case-insensitive substring match against the title.
    # We lowercase both sides so "Phone", "phone", and "PHONE" all match.
    # An empty search term matches everything (search_term.lower() in title
    # is True for an empty string).
    search_ok = search_term.lower() in product["title"].lower()

    return category_ok and price_ok and search_ok


# Build the final filtered list using our combined check above.
filtered_products = [product for product in products if matches_filters(product)]


# ---------------------------------------------------------------------------
# SECTION 4: DISPLAYING PRODUCTS
# ---------------------------------------------------------------------------
# Let the user know how many products matched their filters, and bail out
# early with a friendly message if nothing matched.
st.subheader(f"Showing {len(filtered_products)} of {len(products)} products")

if not filtered_products:
    st.info("No products match your current filters. Try adjusting them.")
else:
    # Loop through each filtered product and render it as its own "card".
    for product in filtered_products:
        # st.container() with a border groups all the widgets for one
        # product together visually, separating it from the next product.
        with st.container(border=True):
            # Split the card into two columns: a narrow one for the image,
            # a wide one for the text details.
            image_col, details_col = st.columns([1, 3])

            with image_col:
                # st.image() renders the product photo directly from its URL.
                st.image(product["image"], width=150)

            with details_col:
                # Title as a small heading.
                st.markdown(f"### {product['title']}")

                # Price, formatted to 2 decimal places like currency.
                st.write(f"**Price:** ${product['price']:.2f}")

                # Category, shown as-is from the API.
                st.write(f"**Category:** {product['category']}")

                # Rating information lives in a nested dictionary in the
                # API response: {"rate": ..., "count": ...}.
                rating = product["rating"]
                st.write(f"**Rating:** ⭐ {rating['rate']} ({rating['count']} reviews)")

                # st.expander() creates a collapsible section that starts
                # closed by default (that's why we don't pass expanded=True).
                # This keeps long descriptions from cluttering the page
                # until the user actually wants to read them.
                with st.expander("View details"):
                    st.write(product["description"])
