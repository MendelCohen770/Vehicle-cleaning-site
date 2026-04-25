import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SITE_CONFIG } from "@/lib/constants";

export default function Home() {
  return (
    <>
       <main className="flex-1">
      {/* Hero — Brand colors demo */}
      <section className="from-brand-green via-brand-green to-brand-azur relative overflow-hidden bg-gradient-to-br text-white">
        <div className="container mx-auto px-6 py-24 sm:py-32">
          <p className="text-brand-sun mb-4 text-sm font-semibold tracking-widest uppercase">
            {SITE_CONFIG.legalName} — Côte d&apos;Azur
          </p>
          <h1 className="mb-6 max-w-3xl text-4xl leading-tight font-bold sm:text-6xl">
            {SITE_CONFIG.name}
          </h1>
          <p className="mb-8 max-w-2xl text-lg text-white/90 sm:text-xl">
            {SITE_CONFIG.description}
          </p>
          <div className="flex flex-wrap gap-4">
            <Button
              size="lg"
              className="bg-brand-sun text-brand-sun-foreground hover:bg-brand-sun/90"
            >
              Réserver une prestation
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-white/40 bg-white/10 text-white hover:bg-white/20"
            >
              En savoir plus
            </Button>
                      </div>
        </div>
      </section>
                  {/* Palette preview */}
      <section className="container mx-auto px-6 py-16">
        <h2 className="mb-2 text-2xl font-bold">Palette de la marque</h2>
        <p className="text-muted-foreground mb-8">
          Aperçu des couleurs définies dans{" "}
          <code className="bg-muted rounded px-1.5 py-0.5 text-sm">src/app/globals.css</code>.
        </p>
                   <div className="grid gap-4 sm:grid-cols-3">
          <Card className="overflow-hidden">
            <div className="bg-brand-green h-24" />
            <CardHeader>
              <CardTitle>Vert écologique</CardTitle>
              <CardDescription>bg-brand-green · bg-primary</CardDescription>
            </CardHeader>
          </Card>
                      <Card className="overflow-hidden">
            <div className="bg-brand-azur h-24" />
            <CardHeader>
              <CardTitle>Bleu Azur</CardTitle>
              <CardDescription>bg-brand-azur · bg-secondary</CardDescription>
            </CardHeader>
          </Card>
            <Card className="overflow-hidden">
            <div className="bg-brand-sun h-24" />
            <CardHeader>
              <CardTitle>Orange / Jaune</CardTitle>
              <CardDescription>bg-brand-sun · bg-accent</CardDescription>
            </CardHeader>
          </Card>
        </div>
        <Card className="mt-10">
          <CardContent>
            <ul className="text-muted-foreground list-inside list-disc space-y-1 text-sm">
              <li>Next.js 16 · TypeScript · App Router · src/</li>
              <li>Tailwind CSS v4 + shadcn/ui (base-nova, neutral)</li>
              <li>Palette de marque configurée (vert, azur, soleil)</li>
              <li>Structure : app / components / features / hooks / lib / types</li>
              <li>ESLint + Prettier + Husky + lint-staged</li>
            </ul>
          </CardContent>
        </Card>
      </section>
    </main>
    </>
  );
}
