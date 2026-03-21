import React from 'react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

const faqs = [
  {
    id: 'q1',
    question: 'Welche Schulformen bietet die Wilhelm-Knapp-Schule an?',
    answer:
      'Wir bieten folgende Schulformen an: Berufliches Gymnasium (Abitur), Fachoberschule (Fachhochschulreife), Berufsfachschule (Mittlerer Abschluss), Berufsschule im dualen System, Fachschule für Technik sowie Bildungsgänge zur Berufsvorbereitung.',
  },
  {
    id: 'q2',
    question: 'Wie kann ich mich an der WKS bewerben?',
    answer:
      'Die Bewerbung erfolgt über unser Online-Bewerbungsformular. Wählen Sie die gewünschte Schulform, füllen Sie das Formular aus und reichen Sie die erforderlichen Unterlagen ein. Die Anmeldung für das Berufliche Gymnasium und die Fachoberschule erfolgt in der Regel bis zum 30. April des Vorjahres.',
  },
  {
    id: 'q3',
    question: 'Welche Voraussetzungen brauche ich für das Berufliche Gymnasium?',
    answer:
      'Für die Aufnahme in das Berufliche Gymnasium benötigen Sie einen qualifizierenden Mittleren Abschluss (Realschulabschluss) oder die Versetzung in die Einführungsphase der gymnasialen Oberstufe. Der Notendurchschnitt in Deutsch, Mathematik und Englisch sollte mindestens 3,0 betragen, wobei keines dieser Fächer schlechter als Note 4 sein darf.',
  },
  {
    id: 'q4',
    question: 'Gibt es eine Mensa oder Cafeteria?',
    answer:
      'Ja, die WKS verfügt über eine Mensa, die von der Abteilung Ernährung und Hauswirtschaft betrieben wird. Hier erhalten Sie täglich frisch zubereitete Mahlzeiten zu günstigen Preisen. Zusätzlich gibt es einen Kiosk mit Snacks und Getränken.',
  },
  {
    id: 'q5',
    question: 'Wie erreiche ich die WKS mit öffentlichen Verkehrsmitteln?',
    answer:
      'Die WKS ist gut mit öffentlichen Verkehrsmitteln erreichbar. Vom Bahnhof Weilburg ist die Schule in ca. 10 Minuten zu Fuß erreichbar. Zahlreiche Buslinien des RMV fahren direkt zur Haltestelle nahe der Schule. Es stehen auch Parkplätze für Fahrräder und PKW zur Verfügung.',
  },
  {
    id: 'q6',
    question: 'Bietet die WKS Praktikumsplätze an?',
    answer:
      'In der Fachoberschule (Form A) ist ein einjähriges gelenktes Praktikum im ersten Ausbildungsjahr vorgesehen. Wir unterstützen unsere Schülerinnen und Schüler bei der Suche nach geeigneten Praktikumsplätzen in Betrieben der Region.',
  },
  {
    id: 'q7',
    question: 'Was ist eine Selbstständige Berufliche Schule (SBS)?',
    answer:
      'Als Selbstständige Berufliche Schule (SBS) verfügt die WKS über erweiterte Entscheidungsbefugnisse in den Bereichen Unterrichtsorganisation, Personalmanagement und Budgetverwaltung. Dies ermöglicht uns, schnell und flexibel auf die Bedürfnisse unserer Schülerinnen und Schüler sowie die Anforderungen des regionalen Arbeitsmarktes zu reagieren.',
  },
];

export default function FaqAccordion() {
  return (
    <Accordion type="single" collapsible className="w-full max-w-3xl mx-auto">
      {faqs.map((faq) => (
        <AccordionItem key={faq.id} value={faq.id}>
          <AccordionTrigger>{faq.question}</AccordionTrigger>
          <AccordionContent>{faq.answer}</AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
