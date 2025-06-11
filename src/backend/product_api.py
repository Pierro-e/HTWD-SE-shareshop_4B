from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

OPENFOODFACTS_API = "https://world.openfoodfacts.org/cgi/search.pl"

def extract_unit(quantity: str) -> str | None:
    if not quantity:
        return None
    quantity = quantity.lower()
    if "kg" in quantity or "g" in quantity or "mg" in quantity:
        return "Kilogramm"
    if "l" in quantity or "ml" in quantity or "cl" in quantity:
        return "Liter"
    if "stück" in quantity or "st" in quantity or "x" in quantity:
        return "Stück"
    return None

@app.get("/product")
async def search_one_product(query: str):
    params = {
        "search_terms": query,
        # Herkunftsfilter testweise deaktiviert:
        # "tagtype_0": "origins",
        # "tag_contains_0": "contains",
        # "tag_0": "germany",
        "action": "process",
        "json": 1,
        "page_size": 20
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPENFOODFACTS_API, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Fehler bei der Anfrage an OpenFoodFacts")

    data = response.json()
    products = data.get("products", [])

    for p in products:
        name = p.get("product_name")
        if not name:
            continue

        if query.lower().strip() in name.lower():
            quantity = p.get("quantity", "")
            unit = extract_unit(quantity)
            if not unit:
                continue
            return {
                "product_name": query,
                "unit": unit
            }

    raise HTTPException(status_code=404, detail=f"Kein Produkt mit '{query}' gefunden")
