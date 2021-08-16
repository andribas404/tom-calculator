import uvicorn


if __name__ == '__main__':
    uvicorn.run('tom_calculator.application:app', host='0.0.0.0', port=80)
