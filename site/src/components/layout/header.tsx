import Link from "next/link";
import { Button } from "@/components/ui/button";
import { SITE_CONFIG } from "@/lib/constants";

const NAV_LINKS = [
  { href: "/vehicule-de-loisir", label: "Véhicule de loisir" },
  { href: "/voiture", label: "Voiture" },
  { href: "/moto", label: "Moto" },
  { href: "/blog", label: "Blog" },
];

export function Header() {
  return (
    <header className="border-border/60 bg-background/80 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 border-b backdrop-blur">
      <div className="container mx-auto flex h-16 items-center justify-between px-6">
        {/* Brand / Logo */}
        <Link href="/" className="flex items-center gap-2">
          <span
            aria-hidden
            className="bg-brand-green ring-brand-green/20 inline-block h-3 w-3 rounded-full ring-4"
          />
          <span className="text-lg font-bold tracking-tight">
            <span className="text-brand-green">LAVER</span>
            <span className="text-brand-azur">VOTRE</span>
            <span className="text-brand-sun">VEHICULE</span>
          </span>
          <span className="text-muted-foreground hidden text-xs font-medium sm:inline">
            .fr · par {SITE_CONFIG.legalName}
          </span>
        </Link>

        {/* Navigation */}
        <nav className="hidden items-center gap-6 md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-foreground/80 hover:text-brand-green text-sm font-medium transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* CTA */}
        <Button
          asChild
          className="bg-brand-green text-brand-green-foreground hover:bg-brand-green/90"
        >
          <Link href="#reserver">Réserver</Link>
        </Button>
      </div>
    </header>
  );
}
