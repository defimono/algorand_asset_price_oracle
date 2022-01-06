import json

from dotenv import load_dotenv

from modules.config.load_config import load_config
from modules.config.logger import logger

load_dotenv()


def main(event, context):
    config = load_config()

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


if __name__ == "__main__":
    logger.info(main(None, None))
