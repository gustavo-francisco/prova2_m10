import json
import pathlib
import logging
from typing import Union
from fastapi import FastAPI, Request, Response
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import uvicorn
from pydantic import BaseModel
import encodings

app = FastAPI()

formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler('logfile.log', backupCount=0)
logging.getLogger("fastapi")
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)

fastapi_logger.info('****************** Starting Server *****************')

blog_posts = []

class BlogPost(BaseModel):
    id: str
    title: str
    content: str
    
@app.post('/blog')
def create_blog_post(post: BlogPost):
    try:
        blog_post = post
        blog_posts.append(blog_post)
        success = 'success'
        return Response(content=success, media_type='application/json'), 201
    except KeyError:
        bad_request = 'invalid request'
        return Response(content=bad_request, media_type='application/json'), 400
    except Exception as e:
        server_error = str(e)
        return Response(content=server_error, media_type='application/json'), 500
    
@app.get('/blog')
def get_blog_posts() -> list[BlogPost]:
    get_blogs = []
    for blog in blog_posts:
        
        get_blogs.append(str(blog))
    return Response(content=json.dumps(get_blogs, ensure_ascii=False), media_type='application/json')

@app.get('/blog/<int:id>')
def get_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            success = {'post': post.__dict__}
            return Response(content=success, media_type='application/json'), 200
    error = {'error': 'Post not found'}
    return Response(content=error, media_type='application/json'), 404

@app.delete('/blog/<int:id>')
def delete_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            success = {'status':'sucess'}
            blog_posts.remove(post)
            return Response(content=success, media_type='application/json'), 200
        error = {'error': 'Post not found'}
    return Response(content=error, media_type='application/json'), 404
    
@app.put('/blog/<int:id>')
def update_blog_post(id: int, request: Request):
    try:
        data = request.get_json()
        for post in blog_posts:
            if post.id == id:
                post.title = data['title']
                post.content = data['content']
                success = {'status':'sucess'}
                return Response(content=success, media_type='application/json'), 200
            not_found = {'error': 'Post not found'}
            bad_request = {'error': 'Invalid request'}
        return Response(content=not_found, media_type='application/json'), 404
    except KeyError:
        return Response(content=bad_request, media_type='application/json'), 400
    except Exception as e:
        server_error = {'error': str(e)}
        return Response(content=server_error, media_type='application/json'), 500
    
if __name__ == "__main__":
    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run(app, host="0.0.0.0", port=5000, log_config=f"{cwd}/log.ini")