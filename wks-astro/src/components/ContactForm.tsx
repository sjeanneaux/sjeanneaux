import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Send, CheckCircle } from 'lucide-react';

export default function ContactForm() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
    }, 1000);
  };

  if (submitted) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center space-y-4">
        <CheckCircle className="w-16 h-16 text-green-500" />
        <h3 className="text-xl font-semibold text-wks-dark">Nachricht gesendet!</h3>
        <p className="text-muted-foreground">
          Vielen Dank für Ihre Nachricht. Wir melden uns schnellstmöglich bei Ihnen.
        </p>
        <Button variant="outline" onClick={() => setSubmitted(false)}>
          Neue Nachricht
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
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

      <div className="space-y-2">
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

      <div className="space-y-2">
        <Label htmlFor="betreff">Betreff</Label>
        <select
          id="betreff"
          className="flex h-11 w-full rounded-md border border-input bg-background px-4 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors"
        >
          <option value="">Bitte wählen...</option>
          <option value="allgemein">Allgemeine Anfrage</option>
          <option value="schulform">Frage zu Schulformen</option>
          <option value="bewerbung">Frage zur Bewerbung</option>
          <option value="ausbildung">Frage zur Ausbildung</option>
          <option value="sonstiges">Sonstiges</option>
        </select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="nachricht">
          Nachricht <span className="text-destructive">*</span>
        </Label>
        <Textarea
          id="nachricht"
          placeholder="Ihre Nachricht an uns..."
          rows={5}
          required
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
        variant="default"
        size="lg"
        className="w-full bg-wks-primary hover:bg-wks-dark"
        disabled={loading}
      >
        {loading ? (
          'Wird gesendet...'
        ) : (
          <>
            <Send size={16} />
            Nachricht senden
          </>
        )}
      </Button>
    </form>
  );
}
