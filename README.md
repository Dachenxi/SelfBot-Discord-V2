
```
SelfBot-Discord-V2
├─ backend
│  ├─ generated
│  │  └─ prisma
│  │     ├─ browser.ts
│  │     ├─ client.ts
│  │     ├─ commonInputTypes.ts
│  │     ├─ enums.ts
│  │     ├─ internal
│  │     │  ├─ class.ts
│  │     │  ├─ prismaNamespace.ts
│  │     │  └─ prismaNamespaceBrowser.ts
│  │     ├─ models
│  │     │  └─ Sniff.ts
│  │     ├─ models.ts
│  │     ├─ runtime
│  │     ├─ wasm-edge-light-loader.mjs
│  │     └─ wasm-worker-loader.mjs
│  ├─ package.json
│  ├─ pnpm-lock.yaml
│  ├─ prisma
│  │  └─ migrations
│  │     ├─ 20260605091725_init_sniffer
│  │     │  └─ migration.sql
│  │     └─ migration_lock.toml
│  ├─ prisma.config.ts
│  ├─ src
│  │  ├─ Dockerfile
│  │  ├─ api
│  │  │  ├─ controller
│  │  │  │  └─ clientController.ts
│  │  │  ├─ routes
│  │  │  │  ├─ authRoutes.ts
│  │  │  │  ├─ clientRoutes.ts
│  │  │  │  └─ snifferRoutes.ts
│  │  │  └─ server.ts
│  │  ├─ bot
│  │  │  ├─ client.ts
│  │  │  └─ events
│  │  │     └─ messageCreate.ts
│  │  ├─ index.ts
│  │  └─ lib
│  │     ├─ cache.ts
│  │     └─ prisma.ts
│  └─ tsconfig.json
├─ docker-compose.yaml
├─ frontend
│  ├─ .npmrc
│  ├─ .prettierignore
│  ├─ .prettierrc
│  ├─ .svelte-kit
│  │  ├─ ambient.d.ts
│  │  ├─ env.d.ts
│  │  ├─ generated
│  │  │  ├─ client
│  │  │  │  ├─ app.js
│  │  │  │  ├─ matchers.js
│  │  │  │  └─ nodes
│  │  │  │     ├─ 0.js
│  │  │  │     ├─ 1.js
│  │  │  │     ├─ 2.js
│  │  │  │     ├─ 3.js
│  │  │  │     ├─ 4.js
│  │  │  │     ├─ 5.js
│  │  │  │     ├─ 6.js
│  │  │  │     └─ 7.js
│  │  │  ├─ root.js
│  │  │  ├─ root.svelte
│  │  │  └─ server
│  │  │     └─ internal.js
│  │  ├─ non-ambient.d.ts
│  │  ├─ tsconfig.json
│  │  └─ types
│  │     ├─ route_meta_data.json
│  │     └─ src
│  │        └─ routes
│  │           ├─ $types.d.ts
│  │           ├─ (dashboard)
│  │           │  ├─ $types.d.ts
│  │           │  ├─ profile
│  │           │  │  └─ $types.d.ts
│  │           │  ├─ setting
│  │           │  │  └─ $types.d.ts
│  │           │  └─ sniffer
│  │           │     ├─ $types.d.ts
│  │           │     └─ proxy+page.server.ts
│  │           ├─ login
│  │           │  ├─ $types.d.ts
│  │           │  └─ proxy+page.server.ts
│  │           ├─ profile
│  │           ├─ setting
│  │           └─ sniffer
│  ├─ README.md
│  ├─ eslint.config.js
│  ├─ package.json
│  ├─ pnpm-lock.yaml
│  ├─ src
│  │  ├─ app.d.ts
│  │  ├─ app.html
│  │  ├─ lib
│  │  │  ├─ api.ts
│  │  │  ├─ assets
│  │  │  │  └─ favicon.svg
│  │  │  ├─ components
│  │  │  │  ├─ Button.svelte
│  │  │  │  ├─ Pill.svelte
│  │  │  │  └─ ToastContainer.svelte
│  │  │  ├─ index.ts
│  │  │  └─ state
│  │  │     └─ Toast.svelte.ts
│  │  └─ routes
│  │     ├─ (dashboard)
│  │     │  ├─ +layout.server.ts
│  │     │  ├─ +layout.svelte
│  │     │  ├─ +page.svelte
│  │     │  ├─ profile
│  │     │  │  └─ +page.svelte
│  │     │  ├─ setting
│  │     │  │  └─ +page.svelte
│  │     │  └─ sniffer
│  │     │     ├─ +page.server.ts
│  │     │     └─ +page.svelte
│  │     ├─ layout.css
│  │     └─ login
│  │        ├─ +page.server.ts
│  │        └─ +page.svelte
│  ├─ static
│  │  └─ robots.txt
│  ├─ svelte.config.js
│  ├─ tsconfig.json
│  └─ vite.config.ts
└─ shared
   └─ types.ts

```