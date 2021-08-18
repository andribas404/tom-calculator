import logging

import uvicorn

from tom_calculator.util import set_debug

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    set_debug()
    uvicorn.run('tom_calculator.application:app', host='0.0.0.0', port=8000)
