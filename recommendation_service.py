from urllib.parse import quote_plus
import uuid

def search_url(platform,q):
    q=quote_plus(q)
    return {"Amazon":f"https://www.amazon.in/s?k={q}","Flipkart":f"https://www.flipkart.com/search?q={q}","IKEA":f"https://www.ikea.com/in/en/search/?q={q}","Swiggy":f"https://www.swiggy.com/search?query={q}","Zomato":f"https://www.zomato.com/search?query={q}","OYO":f"https://www.oyorooms.com/search?location={q}","BigBasket":f"https://www.bigbasket.com/ps/?q={q}"}.get(platform,f"https://www.google.com/search?q={q}")

def fallback_recommendation(planner,data):
    b=float(data["budget"])
    if planner=="home":
        alloc={"Furniture":b*.40,"Lighting":b*.15,"Decor":b*.20,"Utility":b*.15,"Reserve":b*.10}
        base=[("Furniture","Compact modular furniture",b*.22,"IKEA"),("Furniture","Storage cabinet",b*.18,"Amazon"),("Lighting","LED ceiling lights",b*.08,"Amazon"),("Decor","Wall decor set",b*.10,"Flipkart"),("Utility","Decorative wall clock",b*.07,"Amazon")]
    elif planner=="party":
        alloc={"Food":b*.45,"Venue":b*.20,"Decoration":b*.15,"Entertainment":b*.10,"Reserve":b*.10}
        base=[("Food","Catering / meal package",b*.45,"Swiggy"),("Venue","Event venue search",b*.20,"OYO"),("Decoration","Party decoration package",b*.15,"Amazon"),("Entertainment","Entertainment supplies",b*.10,"Zomato")]
    elif planner=="travel":
        destination=data.get("destination","your destination")
        alloc={"Transport":b*.35,"Stay":b*.35,"Food":b*.20,"Activities":b*.10}
        base=[("Transport",f"Travel to {destination}",b*.35,"Google"),("Stay",f"Stay in {destination}",b*.35,"OYO"),("Food",f"Local food in {destination}",b*.20,"Google"),("Activities",f"Things to do in {destination}",b*.10,"Google")]
    elif planner=="meal":
        alloc={"Grains and staples":b*.30,"Produce":b*.25,"Protein":b*.25,"Dairy and extras":b*.20}
        base=[("Grains and staples","Weekly grains and pantry staples",b*.30,"BigBasket"),("Produce","Seasonal fruits and vegetables",b*.25,"BigBasket"),("Protein","Protein and lentils",b*.25,"BigBasket"),("Dairy and extras","Dairy and meal essentials",b*.20,"BigBasket")]
    elif planner=="shopping":
        alloc={"Essentials":b*.50,"Priority items":b*.30,"Reserve":b*.20}
        requested=data.get("items",[])
        base=[("Essentials",requested[0] if requested else "Everyday essentials",b*.50,"Amazon"),("Priority items",requested[1] if len(requested)>1 else f"{data.get('category','General')} priority item",b*.30,"Flipkart")]
    else:
        alloc={"Necklace":b*.35,"Earrings":b*.20,"Bracelet":b*.15,"Accessories":b*.10,"Reserve":b*.20}
        base=[("Necklace",f"{data.get('style','Elegant')} necklace",b*.35,"Amazon"),("Earrings","Matching earrings",b*.20,"Flipkart"),("Bracelet","Minimal matching bracelet",b*.15,"Amazon"),("Accessories","Fashion accessory",b*.10,"Flipkart")]
    items=[{"category":c,"name":n,"description":"Budget-aware sample recommendation; verify current price and availability.","estimated_price":round(p,2),"platform":pl,"search_url":search_url(pl,n)} for c,n,p,pl in base]
    return {"planner":planner,"budget":b,"total_estimated":round(sum(x["estimated_price"] for x in items),2),"summary":f"Sample {planner} plan generated within the stated budget.","allocation":{k:round(v,2) for k,v in alloc.items()},"recommendations":items,"source":"Mock recommendation engine","recommendation_id":str(uuid.uuid4())}
