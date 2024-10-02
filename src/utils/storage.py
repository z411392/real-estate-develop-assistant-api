import hashlib
from magic import from_buffer
from mimetypes import guess_extension
from firebase_admin import storage
from src.utils.threads import ThreadPoolExecutor
from datetime import datetime
from src.utils.development import onDevelopment


def mimeFor(buffer: bytes):
    mime = from_buffer(buffer, mime=True)
    return mime


def extensionFor(mime: str):
    extension = guess_extension(mime).lstrip(".")
    return extension


def _prefix():
    if onDevelopment():
        return "development"
    return "production"


def filePathFor(buffer: bytes, bufferSize=4096):
    hash = hashlib.md5()
    for index in range(0, len(buffer), bufferSize):
        hash.update(buffer[index: index + bufferSize])
    md5 = hash.hexdigest()
    mime = mimeFor(buffer)
    extension = extensionFor(mime)
    filePath = f"{extension}/{md5}"
    return filePath


def _existObject(filePath: str):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    return file.exists()


async def existObject(filePath: str):
    async with ThreadPoolExecutor() as execute:
        return await execute(_existObject, filePath)


def _putObject(buffer: bytes, metadata: dict = None):
    bucket = storage.bucket()
    filePath = filePathFor(buffer)
    mime = mimeFor(buffer)
    file = bucket.blob(f"{_prefix()}/{filePath}")
    file.upload_from_string(buffer, content_type=mime)
    if metadata:
        file.metadata = metadata
        file.patch()
    return filePath


async def putObject(buffer: bytes, metadata: dict = None):
    async with ThreadPoolExecutor() as execute:
        return await execute(_putObject, buffer, metadata)


def _getObjectURL(filePath: str, expiry: int = 3600):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    expiration = int(datetime.now().timestamp()) + expiry
    url = file.generate_signed_url(expiration=expiration, method="GET")
    return url


async def getObjectURL(filePath: str, expiry: int = 3600):
    async with ThreadPoolExecutor() as execute:
        return await execute(_getObjectURL, filePath, expiry)


def _deleteObject(filePath: str):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    file.delete()


async def deleteObjectURL(filePath: str):
    async with ThreadPoolExecutor() as execute:
        return await execute(_deleteObject, filePath)


def _getObjectMetaData(filePath: str):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    file.reload()
    return file.metadata


async def getObjectMetaData(filePath: str):
    async with ThreadPoolExecutor() as execute:
        return await execute(_getObjectMetaData, filePath)


def _uploadFromString(filePath: str, text: str, metadata: dict = None):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    file.upload_from_string(text)
    if metadata:
        file.metadata = metadata
        file.patch()
    return filePath


async def uploadFromString(filePath: str, text: str, metadata: dict = None):
    async with ThreadPoolExecutor() as execute:
        return await execute(_uploadFromString, filePath, text, metadata)


def _downloadAsString(filePath: str):
    bucket = storage.bucket()
    file = bucket.blob(f"{_prefix()}/{filePath}")
    return file.download_as_string()


async def downloadAsString(filePath: str):
    async with ThreadPoolExecutor() as execute:
        return await execute(_downloadAsString, filePath)
