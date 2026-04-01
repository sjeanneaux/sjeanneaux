import React, { useState } from 'react';
import { Menu, X, ChevronDown } from 'lucide-react';

const navItems = [
  {
    label: 'Educational Paths',
    href: '/schulformen',
    children: [
      { label: 'Berufliches Gymnasium', href: '/schulformen#berufliches-gymnasium' },
      { label: 'Fachoberschule', href: '/schulformen#fachoberschule' },
      { label: 'Berufsfachschule', href: '/schulformen#berufsfachschule' },
      { label: 'Duale Ausbildung', href: '/schulformen#berufsschule' },
    ],
  },
  { label: 'Terraream', href: '/#ausbildungsberufe' },
  { label: 'Our Team', href: '/#ueber-uns' },
  { label: 'Social Life', href: '/#termine' },
  { label: 'Contact', href: '/#kontakt' },
];

export default function MobileNav() {
  const [open, setOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  return (
    <div className="md:hidden">
      <button
        onClick={() => setOpen(!open)}
        className="p-2 rounded-lg text-white hover:bg-white/10 transition-colors"
        aria-label="Navigation umschalten"
      >
        {open ? <X size={24} /> : <Menu size={24} />}
      </button>

      {open && (
        <div className="absolute top-full left-0 right-0 bg-wks-navy shadow-xl z-50 border-t border-white/10">
          <nav className="p-4 space-y-1">
            {navItems.map((item) => (
              <div key={item.label}>
                {item.children ? (
                  <div>
                    <button
                      className="flex items-center justify-between w-full px-4 py-3 text-left text-white/85 font-medium hover:bg-white/10 rounded-lg transition-colors"
                      onClick={() =>
                        setOpenDropdown(openDropdown === item.label ? null : item.label)
                      }
                    >
                      {item.label}
                      <ChevronDown
                        size={15}
                        className={`transition-transform text-white/60 ${openDropdown === item.label ? 'rotate-180' : ''}`}
                      />
                    </button>
                    {openDropdown === item.label && (
                      <div className="pl-4 border-l border-white/20 ml-5 mt-1 mb-2 space-y-1">
                        {item.children.map((child) => (
                          <a
                            key={child.label}
                            href={child.href}
                            className="block px-3 py-2 text-sm text-white/70 hover:text-white hover:bg-white/10 rounded-md transition-colors"
                            onClick={() => setOpen(false)}
                          >
                            {child.label}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <a
                    href={item.href}
                    className="block px-4 py-3 text-white/85 font-medium hover:bg-white/10 hover:text-white rounded-lg transition-colors"
                    onClick={() => setOpen(false)}
                  >
                    {item.label}
                  </a>
                )}
              </div>
            ))}
            <div className="pt-3 border-t border-white/10 mt-2">
              <a
                href="/bewerbung"
                className="block w-full text-center py-3 px-6 bg-wks-orange text-white font-semibold rounded-lg hover:bg-wks-orange-dark transition-colors"
                onClick={() => setOpen(false)}
              >
                Jetzt bewerben
              </a>
            </div>
          </nav>
        </div>
      )}
    </div>
  );
}
