# MixMeasureBuddy Backend API

A lightweight Express.js service that stores recipes per MixMeasureBuddy device
and exposes an HTTP interface compatible with the firmware `recipe_updater.py`.

## Features

- Separate namespaces per `systemId`
- REST endpoints to list, fetch, add, update, and delete recipes
- JSON files persisted on disk (default: `data/systems/<systemId>/*.recipe`)
- Responses tailored to the firmware update flow (`/:systemId`,
  `/:systemId/recipes`, `/:systemId/recipe/:recipeName`)

## Getting Started

```bash
cd src/webapp/backend
npm install
npm run start # listens on http://localhost:4000 by default
```

Environment variables:

- `PORT` (optional) – port to listen on (default `4000`)
- `RECIPE_STORAGE` (optional) – directory where recipes are stored

## API Overview

| Method | Endpoint                                  | Description                          |
|--------|-------------------------------------------|--------------------------------------|
| GET    | `/:systemId`                              | Health/status check for firmware     |
| GET    | `/:systemId/recipes`                      | List recipe filenames for a device   |
| GET    | `/:systemId/recipe/:recipeName`           | Fetch recipe payload (JSON)          |
| POST   | `/:systemId/recipes`                      | Create a recipe (`{ name?, recipe }`)|
| PUT    | `/:systemId/recipe/:recipeName`           | Replace an existing recipe           |
| DELETE | `/:systemId/recipe/:recipeName`           | Remove a recipe                      |

Recipes are stored exactly as provided (`.recipe` JSON). Names are sanitized
and suffixed with `.recipe` automatically if needed.

The firmware can point its `NETWORK_API_ENPOINT` setting to this service;
`recipe_updater.py` will append the MixMeasureBuddy system identifier and
consume the required routes.
