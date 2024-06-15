from enum import Enum
from random import randint
from typing import Optional, List
from pydantic import BaseModel
from fastapi.params import Body
from fastapi import FastAPI, Response, HTTPException, status, Depends

app = FastAPI() ## FastAPI Instance names as app

## Path Operations/Route:
@app.get("/")  # Known as Decorator for Magical Operation like works as APIS.... [GET is Mehotd & '/' is Path Here is HomePage]
def read_root():  
    return {"Message": "Welcome to the Home Page."}   # Return the What we got from the server.

@app.post("/createposts") 
def create_posts(payload: dict = Body(...)): # Here it extract all the input in body and create dict and store it on the payload variable.
    title = payload.get('title')
    content = payload.get('content')
    print(f"Extracted via another method: Title: {title} and Content: {content}")
    return {"message": f"successfully post created.... which Title: {title} and Content: {content}"}

## So Here New Concern is User Provide Valid Type of Data or Not So Therefor we need Schema So for that we have ti use external library schema validation...

# Define a Pydantic model for the post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field with a default value of True
    rating: Optional[int] = None  # Optional field, can be None if not provided by the user

# Create a new endpoint to handle post creation
@app.post("/createpost_val", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post):  
    """
    This endpoint creates a new post.
    The status code is set to 201 to indicate resource creation.
    The request payload is validated against the Post Pydantic model.
    """
    # Convert the Pydantic model instance to a dictionary
    post_data = payload.dict()
    print(post_data)
    return {"new post": f"title: {payload.title} and content is {payload.content}"}

# Define an Enum for predefined place names
class Place(str, Enum):
    amd = "Ahmedabad"
    brd = "Baroda"
    srt = "Surat"
    
# Define a GET endpoint that accepts a place_name parameter
@app.get("/place/{place_name}")
def get_place(place_name: Place):
    """
    Endpoint to get information about a specific place.
    Args:
    - place_name (Place): A path parameter specifying the place name from the Place Enum.
    Returns:
    - dict: A dictionary with the place name as a response.
    Raises:
    - HTTPException 422: If an invalid place_name that is not part of the Place Enum is provided.
    """
    if place_name == Place.amd:
        return {"Place": Place.amd}
    elif place_name == Place.brd:
        return {"Place": Place.brd}   
    else:
        return {"Place": Place.srt}
    
## Other Methods --------------------------------
all_data = [{'id': 1,"title": "First Post", "content": "This is the content of the first post.", "published": True, "rating": 4},
       {'id': 2, "title": "Second Post", "content": "This is the content of the second post.", "published": False, "rating": None}]

@app.get("/all_data", response_model=List[dict])  # Uses response_model=List[dict] to specify that the response is a list of dictionaries.
def get_all_data():
    return all_data

# POST endpoint to add a new post
@app.post("/add_post", response_model=dict)
def create_post(post: Post):
    new_id = randint(1, 1000)
    post_dict = post.dict()
    post_dict['id'] = new_id
    all_data.append(post_dict)
    return post_dict

# Helper function to find post by id
def find_post_by_id(post_id: int):
    for post in all_data:
        if post["id"] == post_id:
            return post
    return None

# GET endpoint to retrieve post by id
@app.get("/all_data/{id}", response_model=dict)
def get_post_by_id(id: int):
    post_info = find_post_by_id(id)
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"Data": post_info}


# Handling Path as Parameters:
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return {"file_content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Reading file: {str(e)}")

def find_index_post(id):
    for  i, post in enumerate(all_data):
        if post['id'] == id:
            return i

# Delete Method:
@app.delete("/all_data/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    all_data.pop(index)
    return {"Message": "post Successfully Deleted..."}  # We Set the Status Code 204 So This Status is Not Return after Post Delete...

# Update Method:  # Update a post by ID
@app.put("/all_data/{id}", response_model=Post)
def update_post(id: int, updated_post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.") 
    current_post = all_data[index]
    updated_data = updated_post.dict(exclude_unset=True)
    for key, value in updated_data.items():
        current_post[key] = value

    # Alternate:
    # current_post.update(updated_data)
    # return {"Message": "Resource Sucessfully Updated....", "Updated Data": updated_post}
    # Return the updated post using the Post model
    return Post(**current_post)

# # PATCH Method: Partially update a post by ID
@app.patch("/all_data/{id}", response_model=Post)
def patch_post(id: int, updated_post: dict = Body(...)):  # Removed Post Pydantic Validation because it Gives Erro if we onlye send small portion.
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    current_post = all_data[index]
    # Update only the fields that are provided in the request body
    # update_data = updated_post.dict(exclude_unset=True)
    for key, value in updated_post.items():
        current_post[key] = value
    return Post(**current_post)