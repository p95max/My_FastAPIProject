from fastapi import FastAPI, Depends, HTTPException
from routers.lost_items import router as lost_item_router
from routers.found_items import router as found_items_router
from routers.category import router as category_router
from routers.tags import router as tags_router

app = FastAPI()
app.include_router(lost_item_router, prefix="/lost_items", tags=["lostItems"])
app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(tags_router, prefix="/tags", tags=["tags"])


@app.get("/")
def read_root():
    return {"message": "Welcome LostAndFound API"}

