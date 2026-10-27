# views.py — The brain of the Explorer feature. It shows the search form, and
# when the user clicks "Search Laptops" it asks the RapidAPI "LaptopDB"
# service for matching laptops, saves them into our local database, and hands
# the results to the HTML page to display.

import requests
from decimal import Decimal, InvalidOperation

from django.shortcuts import render

from .models import Laptop

# ---------------------------------------------------------------------------
# RapidAPI settings for the "LaptopDB" API.
# Replace the placeholder below with your own key from https://rapidapi.com
# (subscribe to the LaptopDB API, then copy your key into RAPIDAPI_KEY).
# ---------------------------------------------------------------------------
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_HERE"           # <-- PASTE YOUR KEY HERE
RAPIDAPI_HOST = "laptopdb.p.rapidapi.com"         # the API's host on RapidAPI
RAPIDAPI_URL = f"https://{RAPIDAPI_HOST}/search"  # the /search endpoint


def _to_int(value):
    """Turns messy API values like '16 GB' or '16' into the number 16.
    If the value cannot be read as a number, we safely return 0 instead
    of crashing (IntegerField needs a real number)."""
    try:
        # str(value) -> "16 GB", .split()[0] -> "16", int("16") -> 16
        return int(str(value).split()[0])
    except (ValueError, IndexError):
        return 0


def _to_decimal(value):
    """Turns messy price values like '$1,299.99' or 1299 into Decimal('1299.99').
    DecimalField needs a Decimal (or int), so we clean the string first.
    If it still fails, we return 0 so the row can still be saved."""
    try:
        return Decimal(str(value).replace("$", "").replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return Decimal("0")


def explorer_search(request):
    """One view for the whole Explorer page.
    GET  -> the user just opened /explorer: show the empty form (plus any
            laptops saved by previous searches, so the page is never empty).
    POST -> the user clicked "Search Laptops": run ONE API call and show the
            matching laptops."""

    # This list holds the Laptop objects shown in the results section.
    # It starts empty and gets filled either from a new search or from
    # laptops already saved in our database.
    laptops = []

    # Will hold a friendly error message if the API call fails
    # (for example because the API key placeholder was never replaced).
    error_message = None

    if request.method == "POST":
        # ----- STEP 1: GATHER THE FORM INPUT -----
        # Every <select> in the form arrives inside request.POST.
        # .get() returns an empty string if the field is missing, which is
        # much safer than crashing with a KeyError.
        ram = request.POST.get("ram")            # e.g. "16"
        storage = request.POST.get("storage")    # e.g. "512"
        vram = request.POST.get("vram")          # e.g. "4"
        use_case = request.POST.get("use_case")  # e.g. "Gaming"

        # ----- STEP 2: BUILD ONE SINGLE API REQUEST -----
        # We only add the filters the user actually picked (empty = "Any").
        # All filters go into ONE request as URL parameters, so a search is
        # always exactly ONE API call. This matters because RapidAPI free
        # plans have strict rate limits (a maximum number of calls per month),
        # and calling on every keystroke would burn the quota instantly.
        params = {}
        if ram:
            params["ram"] = ram
        if storage:
            params["storage"] = storage
        if vram:
            params["vram"] = vram
        if use_case:
            params["use_case"] = use_case

        # RapidAPI identifies WHO is calling using these two headers.
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }

        try:
            # ----- STEP 3: CALL THE API (exactly once per search) -----
            # requests.get() builds the final URL from RAPIDAPI_URL + params,
            # e.g. .../search?ram=16&storage=512&vram=4&use_case=Gaming
            # timeout=15 stops waiting after 15 seconds if the API is down.
            response = requests.get(
                RAPIDAPI_URL, params=params, headers=headers, timeout=15
            )
            # If the API answered with an error code (401 wrong key,
            # 429 quota exceeded, 500 server error), raise an exception so
            # we jump straight to the except block below.
            response.raise_for_status()
            # Convert the JSON text in the response into Python data
            # (a list of laptop dictionaries).
            data = response.json()

            # Depending on the API version, the laptop list lives under a key
            # like "results" or "laptops". Try the common ones, otherwise
            # assume the whole response IS the list.
            results = data.get("results") or data.get("laptops") or data

            # ----- STEP 4: SAVE EVERY LAPTOP INTO OUR LOCAL DATABASE -----
            for item in results:
                # update_or_create() means: "look for a Laptop row with this
                # name; if it already exists UPDATE its fields, otherwise
                # CREATE a new row".
                # WHY we do this:
                #   1. It prevents duplicate rows when the user searches the
                #      same laptop twice (name is unique in the model).
                #   2. It lets the demo reuse data we already fetched —
                #      later searches for the same laptop can be served from
                #      our local database without another paid API call.
                laptop, _created = Laptop.objects.update_or_create(
                    # The field used to find an existing row (its "identity").
                    name=item.get("name") or "Unknown Laptop",
                    # The fields to write into that row.
                    defaults={
                        "ram_gb": _to_int(item.get("ram_gb")),
                        "storage_gb": _to_int(item.get("storage_gb")),
                        "vram_gb": _to_int(item.get("vram_gb")),
                        "cpu": item.get("cpu") or "Unknown CPU",
                        "price": _to_decimal(item.get("price")),
                        "recommended_for": item.get("recommended_for") or use_case,
                    },
                )
                # Collect the saved objects so we can show them on the page.
                laptops.append(laptop)

        except (requests.RequestException, ValueError) as e:
            # Network problems, an invalid API key, or a response that is not
            # valid JSON all land here. We show a friendly message on the
            # page instead of letting Django crash with an error screen.
            error_message = (
                "Could not fetch laptops from LaptopDB. Please check your "
                f"RAPIDAPI_KEY and your internet connection. ({e})"
            )

    else:
        # ----- GET REQUEST: the page was just opened, no search yet -----
        # Show laptops saved by PREVIOUS searches so the results area is not
        # completely empty on the first visit.
        laptops = Laptop.objects.all()[:12]

    # ----- STEP 5: RENDER THE PAGE -----
    # 'laptops' is looped over in explorer.html; 'error_message' is shown in
    # a red box only when something went wrong (None hides that block).
    context = {
        "laptops": laptops,
        "error_message": error_message,
    }
    return render(request, "explorer.html", context)
