import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Send, CheckCircle } from 'lucide-react';

const schulformen = [
  'Berufliches Gymnasium',
  'Fachoberschule (Form A – mit Praktikum)',
  'Fachoberschule (Form B – mit Berufsabschluss)',
  'Berufsfachschule',
  'Berufsschule (Duales System)',
  'Fachschule für Technik',
  'Bildungsgänge zur Berufsvorbereitung',
];

export default function BewerbungForm() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
    }, 1200);
  };

  if (submitted) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center space-y-4">
        <CheckCircle className="w-20 h-20 text-green-500" />
        <h3 className="text-2xl font-bold text-wks-dark">Bewerbung eingereicht!</h3>
        <p className="text-muted-foreground max-w-md">
          Ihre Bewerbung wurde erfolgreich eingereicht. Sie erhalten in Kürze eine
          Bestätigungs-E-Mail. Wir freuen uns auf Sie!
        </p>
        <Button variant="outline" onClick={() => setSubmitted(false)}>
          Weitere Bewerbung einreichen
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Persönliche Daten */}
      <div>
        <h3 className="text-lg font-semibold text-wks-dark mb-4 pb-2 border-b">
          Persönliche Daten
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="vorname">
              Vorname <span className="text-destructive">*</span>
            </Label>
            <Input id="vorname" placeholder="Max" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="nachname">
              Nachname <span className="text-destructive">*</span>
            </Label>
            <Input id="nachname" placeholder="Mustermann" required />
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
          <div className="space-y-2">
            <Label htmlFor="geburtsdatum">
              Geburtsdatum <span className="text-destructive">*</span>
            </Label>
            <Input id="geburtsdatum" type="date" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="telefon">Telefon</Label>
            <Input id="telefon" type="tel" placeholder="06471 / 123456" />
          </div>
        </div>
        <div className="mt-4 space-y-2">
          <Label htmlFor="email">
            E-Mail <span className="text-destructive">*</span>
          </Label>
          <Input
            id="email"
            type="email"
            placeholder="max.mustermann@beispiel.de"
            required
          />
        </div>
      </div>

      {/* Adresse */}
      <div>
        <h3 className="text-lg font-semibold text-wks-dark mb-4 pb-2 border-b">
          Adresse
        </h3>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="strasse">
              Straße und Hausnummer <span className="text-destructive">*</span>
            </Label>
            <Input id="strasse" placeholder="Musterstraße 1" required />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="plz">
                PLZ <span className="text-destructive">*</span>
              </Label>
              <Input id="plz" placeholder="35781" required />
            </div>
            <div className="sm:col-span-2 space-y-2">
              <Label htmlFor="ort">
                Ort <span className="text-destructive">*</span>
              </Label>
              <Input id="ort" placeholder="Weilburg" required />
            </div>
          </div>
        </div>
      </div>

      {/* Schulform */}
      <div>
        <h3 className="text-lg font-semibold text-wks-dark mb-4 pb-2 border-b">
          Gewünschte Schulform
        </h3>
        <div className="space-y-2">
          <Label htmlFor="schulform">
            Schulform <span className="text-destructive">*</span>
          </Label>
          <select
            id="schulform"
            required
            className="flex h-11 w-full rounded-md border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors"
          >
            <option value="">Bitte wählen...</option>
            {schulformen.map((sf) => (
              <option key={sf} value={sf}>
                {sf}
              </option>
            ))}
          </select>
        </div>
        <div className="mt-4 space-y-2">
          <Label htmlFor="schulabschluss">
            Höchster Schulabschluss <span className="text-destructive">*</span>
          </Label>
          <select
            id="schulabschluss"
            required
            className="flex h-11 w-full rounded-md border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors"
          >
            <option value="">Bitte wählen...</option>
            <option>Hauptschulabschluss</option>
            <option>Mittlerer Abschluss / Realschulabschluss</option>
            <option>Fachhochschulreife</option>
            <option>Allgemeine Hochschulreife (Abitur)</option>
            <option>Noch kein Abschluss</option>
          </select>
        </div>
      </div>

      {/* Anmerkungen */}
      <div className="space-y-2">
        <Label htmlFor="anmerkungen">Anmerkungen / Fragen</Label>
        <Textarea
          id="anmerkungen"
          placeholder="Haben Sie besondere Anmerkungen oder Fragen?"
          rows={4}
        />
      </div>

      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          id="datenschutz"
          required
          className="mt-1 w-4 h-4 accent-primary"
        />
        <label htmlFor="datenschutz" className="text-sm text-muted-foreground">
          Ich habe die{' '}
          <a href="/datenschutz" className="text-primary underline hover:no-underline">
            Datenschutzerklärung
          </a>{' '}
          gelesen und bin mit der Verarbeitung meiner Daten einverstanden.{' '}
          <span className="text-destructive">*</span>
        </label>
      </div>

      <Button
        type="submit"
        variant="gold"
        size="xl"
        className="w-full"
        disabled={loading}
      >
        {loading ? (
          'Bewerbung wird eingereicht...'
        ) : (
          <>
            <Send size={18} />
            Bewerbung jetzt einreichen
          </>
        )}
      </Button>
    </form>
  );
}
