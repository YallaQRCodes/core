# Core Library
## docs
[https://yqrc-api-core.gaytomycode.com](https://yqrc-api-core.gaytomycode.com)

## Install
### Commandline
```bash
$ pip install git+ssh://git@github.com/yallaqrcodes/api-core
```
### requirements.txt
```txt
yqrc-core @ git+ssh://git@github.com/yallqrcodes/api-core
```

## Usage

```python3
import yqrc_core
```

## Scructure
YQRC Backend is a micro-service architecture containing:
* identity: Managing JWT tokens and sessions.
* qrcode: Generating QRCodes and tracking their visits.
* queue: A queue of people ex: waitinglist, reservations.
* restaurant: Restaurant information and configuration.
* seating: Restaurant table management.
* terms: Restaurant terms and conditions.
* shrink: Shortns and tracks urls.

## Modules
* config: Has the settings.
* crud_base: The base crud class.
* deps: Router dependances.
* exceptions: Exceptions that result in http response.
* helpers: Utility functions.
* models_base: The base sqlachemy model class.
* schemas_base: Pydantic base that supports property.
