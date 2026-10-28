import requests
from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from .models import Laptop
from django.conf import settings

# ---------------------------------------------------------------------------
# npoint.io settings
# Replace the placeholder below with your actual npoint.io link!
# (It should look something like: https://api.npoint.io/8a3b4c5d...)
# ---------------------------------------------------------------------------
NPOINT_API = settings.NPOINT_URL

def _to_int(value):
    """Turns messy API values like '16 GB' or '16' into the number 16."""
    try:
        return int(str(value).split()[0])
    except (ValueError, IndexError, TypeError):
        return 0

def _to_decimal(value):
    """Turns messy price values into Decimal('1299.99')."""
    try:
        # Clean up currency symbols just in case
        clean_str = str(value).replace("$", "").replace("€", "").replace(",", "").strip()
        return Decimal(clean_str)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0")

def explorer_search(request):
    laptops = []
    error_message = None

    if request.method == "POST":
        # ----- STEP 1: GATHER THE FORM INPUT -----
        ram = request.POST.get("ram")            
        storage = request.POST.get("storage")    
        vram = request.POST.get("vram")          
        use_case = request.POST.get("use_case")  

        try:
            # ----- STEP 2: FETCH THE "BOX" (All Laptops) -----
            response = requests.get(NPOINT_API, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            # Safety check: Ensure we have a list, even if the API wraps it in a dictionary
            all_laptops = data if isinstance(data, list) else data.get("results", data.get("laptops", []))
            
            # ----- STEP 3: DJANGO DOES THE FILTERING (The Librarian) -----
            filtered_laptops = []
            for item in all_laptops:
                # Extract specs safely
                item_ram = _to_int(item.get("ram_gb"))
                item_storage = _to_int(item.get("storage_gb"))
                item_vram = _to_int(item.get("vram_gb"))
                item_use = str(item.get("recommended_for", "")).lower()
                
                # If user selected a filter, skip laptops that DON'T meet the minimum requirement
                if ram and item_ram < int(ram):
                    continue
                if storage and item_storage < int(storage):
                    continue
                if vram and item_vram < int(vram):
                    continue
                
                # Check if the use case matches (e.g., "gaming" inside "Gaming, Programming")
                if use_case and use_case.lower() not in item_use:
                    continue
                
                # If it survived all the 'continue' skips, it's a match!
                filtered_laptops.append(item)

            # ----- STEP 4: SAVE MATCHES TO DATABASE & DISPLAY -----
            for item in filtered_laptops:
                laptop, _created = Laptop.objects.update_or_create(
                    name=item.get("name") or "Unknown Laptop",
                    defaults={
                        "ram_gb": _to_int(item.get("ram_gb")),
                        "storage_gb": _to_int(item.get("storage_gb")),
                        "vram_gb": _to_int(item.get("vram_gb")),
                        "cpu": item.get("cpu") or "Unknown CPU",
                        "price": _to_decimal(item.get("price")),
                        "recommended_for": item.get("recommended_for") or "",
                    },
                )
                laptops.append(laptop)
                
            # Limit to 50 results so your HTML page doesn't freeze if there are 1000 matches
            laptops = laptops[:50]

        except requests.RequestException as e:
            error_message = f"Could not fetch laptops from npoint.io. Check your URL. ({e})"
        except Exception as e:
            error_message = f"An error occurred while filtering: {e}"

    else:
        # GET REQUEST: Show previously saved laptops
        laptops = Laptop.objects.all()[:12]

    # ----- STEP 5: RENDER THE PAGE -----
    context = {
        "laptops": laptops,
        "error_message": error_message,
    }
    return render(request, "explorer.html", context)
