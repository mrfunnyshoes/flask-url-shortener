# URL Shortener Microservice (freeCodeCamp project)

## Example request

- Using `curl`

```console
curl http://localhost:9876/shorten/new -d "{\"url\":\"https://www.google.com\"}" -H  "Content-Type: application/json"
```

- Or import this collection and test it with Postman: `https://www.getpostman.com/collections/a646b773a5ac0c24a0b7`

## Example response

- If passed a valid URL (format and DNS lookup):

```json
{
  "original_url": "https://www.google.com",
  "short_url": 2
}
```

Then, visiting `http://localhost:9876/shorten/2` should redirect you to `https://www.google.com`.

- If passed an invalid URL (non-existent site or not a valid URL):

```json
{
  "error": "invalid URL"
}
```
