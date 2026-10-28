# connects FastAPI backend to AWS lambda
# later config Lambda to use app.lambda_handler.handler

# mangum translates Lambda events from API Gateway (event, context) into FastAPI understandable format and vice versa.
from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off") 