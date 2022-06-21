import traceback
import uvicorn
import yaml
from typing import Optional
import logging
from starlette.requests import Request

from fastapi import FastAPI, HTTPException

from passworder import Passworder
from random_password import get_random_salt
from pydantic import BaseModel


class EncryptRequest(BaseModel):
    salt: Optional[str] = None
    cleartext: str
    algorithm: Optional[str] = Passworder.DEFAULT_ALGO
    random_salt: Optional[bool] = True


with open("settings.yaml") as settings_file:
    settings = yaml.safe_load(settings_file)
    logging_file_dir = settings["logging_directory"] + "hier-log-ik.log"
main_parameters = {}
if not settings["openapi_console"]:
    main_parameters["docs_url"] = None

app = FastAPI(**main_parameters)
passworder = Passworder()

logger = logging.getLogger(__name__)

logging.basicConfig(filename=logging_file_dir,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S $p')


@app.get("/encrypt/generators")
async def generators_list():
    return [list(Passworder.ALGO_MAP.keys())]


@app.get("/encrypt/version")
async def show_version():
    try:
        with open("version.txt", "r") as version_file:
            version = version_file.read()
            version = version.strip()
        return {"version": version}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail="Version file missing or not readeable")

@app.post("/encrypt/")
async def encrypt(encrypt_request: EncryptRequest, request: Request):
    logging.info(f"200 {request.client.host} {encrypt_request.algorithm}")
    result = {}
    try:
        # Request validation steps..
        if not encrypt_request.cleartext:
            raise HTTPException(status_code=400, detail="Missing cleartext entry to encrypt")
        if not encrypt_request.random_salt and not encrypt_request.salt:
            raise HTTPException(status_code=400, detail="Either random salt or a set salt should be given")

        parameters = encrypt_request.dict()

        # It could be a random salt was requested. In this case, generate one
        # and include it in the function call
        if parameters.get("random_salt"):
            parameters["salt"] = get_random_salt()
        del parameters["random_salt"]

        shadow_string = passworder.get_linux_password(**parameters)

        result = {
            "shadow_string": shadow_string,
            "salt": parameters["salt"],
        }
    except HTTPException as e:
        # Raising the HTTP exception here, otherwise it will be picked up by
        # the generic exception handler
        raise e
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        return result


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=settings["reload"], host=settings["listen_address"],
                port=settings["listen_port"])
