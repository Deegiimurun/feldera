# DBSP Web UI

This is the web UI for the DBSP project.

## Setup

```bash
sudo apt-get update
sudo apt-get install git sudo curl
curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
sudo npm install --global yarn
sudo npm install --global openapi-typescript-codegen

git clone https://github.com/feldera/dbsp.git
cd dbsp/web-console
```

If you don't run ubuntu: [other binary distributions for node.js](https://github.com/nodesource/distributions)

## Development

Install dependencies (needs to be done whenever package.json depencies change):

```bash
yarn install
```

Start the development server:

```bash
yarn dev
```

Build & export static website:

```bash
yarn build
yarn export
```

Format the code & linting:

```bash
yarn format
yarn lint
```

If `yarn audit` fails for a transitive dependency you can try to update it:

```bash
yarn up --recursive loader-utils
```

For direct dependencies, you can adjust the version in `package.json`
and run `yarn install`.

## OpenAPI bindings

The bindings for OpenAPI (under src/lib/services/manager) are generated using
[openapi typescript codegen](https://www.npmjs.com/package/openapi-typescript-codegen).

If you change the API, execute the following steps to update the bindings:

```bash
yarn generate-openapi
```

Note sometimes strange caching errors may warrant deleting `node_modules` after
regenerating the API bindings.

## File Organization

-  `@core/`: Settings, style and MUI overrides.
-  `lib/`: Imported modules
-  `lib/components/`: Reusable React components.
-  `lib/compositions/`: Modules that encapsulate app state management
-  `lib/functions/`: Pure functions, or functions that perform side effects through dependency injection
-  `lib/functions/common`: Utility functions that are not specific to this project
-  `lib/services/`: Functions that describe side effects (persistent storage, networking etc.)
-  `lib/types/`: Types used throughout the app, OpenAPI generated types.
-  `pages/`: Webapp pages used by file-based routing