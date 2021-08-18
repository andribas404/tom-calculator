import logging

import uvicorn

from tom_calculator.application import create_app

logger = logging.getLogger(__name__)

app = create_app()


if __name__ == '__main__':
    uvicorn.run('tom_calculator.main:app', host='0.0.0.0', port=8000)
