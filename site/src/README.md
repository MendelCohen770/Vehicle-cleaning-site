# Project Structure — LAVERVOTREVEHICULE.FR

```
src/
├── app/                      # Next.js App Router (pages, layouts, API routes)
│   ├── layout.tsx            # Root layout (metadata, fonts, providers)
│   ├── page.tsx              # Homepage
│   ├── globals.css           # Global styles + brand color tokens
│   └── (routes)/             # Page routes to be added
│
├── components/
│   ├── ui/                   # shadcn/ui primitives (button, card, input...)
│   ├── layout/               # Header, Footer, Navigation
│   ├── sections/             # Hero, PricingTable, WaterCounter, Testimonials
│   └── forms/                # BookingForm, ContactForm (par catégorie)
│
├── features/                 # Feature-specific modules (booking, blog, admin)
│
├── hooks/                    # Custom React hooks (useBooking, useGeolocation)
│
├── lib/
│   ├── utils.ts              # cn() et helpers (shadcn)
│   ├── constants.ts          # Constantes globales (prix, coords, config)
│   └── validations/          # Schémas Zod (formulaires, API)
│
└── types/
    └── index.ts              # Types partagés (Booking, Customer, etc.)
```

## Aliases d'import

```ts
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SITE_CONFIG } from "@/lib/constants";
import type { Booking } from "@/types";
```

## Palette de couleurs (brand)

Les couleurs sont définies dans `src/app/globals.css` via CSS variables :

- `bg-primary` / `text-primary-foreground` → **Vert écologique**
- `bg-secondary` / `text-secondary-foreground` → **Bleu Azur** (Côte d'Azur)
- `bg-accent` / `text-accent-foreground` → **Orange/Jaune** soleil
- `bg-brand-green`, `bg-brand-azur`, `bg-brand-sun` → tokens dédiés
