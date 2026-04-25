# LAVERVOTREVEHICULE.FR

Site web de **AvaLior** (nom commercial : _lavervotrevehicule_) — service mobile de lavage écologique sans eau pour camping-cars, voitures et motos sur la Côte d'Azur.

## Stack

- **Next.js 16** (App Router, TypeScript, `src/` directory)
- **Tailwind CSS v4** + **shadcn/ui** (base `base-nova`, couleur neutre)
- **ESLint** (flat config) + **Prettier** + **prettier-plugin-tailwindcss**
- **Husky** + **lint-staged** (pre-commit hooks)

## Palette de la marque

Définie dans `src/app/globals.css` :

| Token           | Couleur                 | Tailwind                         |
| --------------- | ----------------------- | -------------------------------- |
| `--brand-green` | Vert écologique         | `bg-brand-green` / `bg-primary`  |
| `--brand-azur`  | Bleu Azur (Côte d'Azur) | `bg-brand-azur` / `bg-secondary` |
| `--brand-sun`   | Orange / Jaune soleil   | `bg-brand-sun` / `bg-accent`     |

## Commandes

```bash
npm run dev           # Démarrer le serveur de dev (http://localhost:3000)
npm run build         # Build de production
npm run start         # Lancer le build de production
npm run lint          # ESLint
npm run lint:fix      # ESLint avec auto-fix
npm run format        # Prettier (écriture)
npm run format:check  # Prettier (vérification)
npm run typecheck     # TypeScript --noEmit
```

## Structure du projet

Voir [`src/README.md`](./src/README.md) pour le détail de l'organisation.

## Variables d'environnement

Copier `.env.example` en `.env.local` et remplir les valeurs.

## Prochaines étapes

La phase 1 (setup) est terminée. Voir `../תכנית-פיתוח-האתר.md` pour la roadmap complète.

**Phase 2** : composants partagés (Header, Footer, Hero, PricingCard, WaterCounter).
