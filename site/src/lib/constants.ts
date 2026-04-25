/**
 * Constantes globales du projet.
 */

export const SITE_CONFIG = {
  name: "LAVERVOTREVEHICULE",
  legalName: "AvaLior",
  domain: "lavervotrevehicule.fr",
  description:
    "Lavage mobile écologique sans eau pour camping-cars, voitures et motos sur la Côte d'Azur.",
  defaultLocale: "fr" as const,
  supportedLocales: ["fr", "en"] as const,
} as const;

export const BRAND_COLORS = {
  green: "oklch(0.55 0.14 155)",
  azur: "oklch(0.65 0.16 240)",
  sun: "oklch(0.82 0.18 80)",
} as const;

export const NICE_COORDINATES = {
  lat: 43.7102,
  lng: 7.262,
} as const;

export const SERVICE_RADIUS_KM = 10;

export const WATER_SAVED_PER_WASH_LITERS = 300;

export const DEPOSIT_PERCENTAGE = 0.15;
