from fastapi import FastAPI, Depends, HTTPException
from routers.lost_items import router as lost_item_router
from routers.found_items import router as found_items_router
from routers.category import router as category_router
from routers.tags import router as tags_router
from routers.users import router as users_router
from depense import get_current_user

app = FastAPI()
app.include_router(lost_item_router, prefix="/lost_items", tags=["lostItems"], dependencies=[Depends(get_current_user)])
app.include_router(found_items_router, prefix="/found_items", tags=["foundItems"], dependencies=[Depends(get_current_user)])
app.include_router(category_router, prefix="/category", tags=["category"], dependencies=[Depends(get_current_user)])
app.include_router(tags_router, prefix="/tags", tags=["tags"],dependencies=[Depends(get_current_user)])
app.include_router(users_router, prefix="/users", tags=["users"])




@app.get("/")
def read_root():
    return {"message": "Welcome LostAndFound API"}

