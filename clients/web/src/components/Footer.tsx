import Link from "next/link"
import { Separator } from "@/components/ui/separator"

const footerLinks = [
  {
    title: "Quick Links",
    links: [
      { name: "Politicians", href: "/politicians" },
      { name: "Billionaires", href: "/billionaires" },
      { name: "About", href: "/about" },
      { name: "Methodology", href: "/methodology" },
    ],
  },
  {
    title: "Legal",
    links: [
      { name: "Privacy Policy", href: "/privacy" },
      { name: "Terms of Service", href: "/terms" },
      { name: "Contact Us", href: "/contact" },
    ],
  },
]

export default function Footer() {
  return (
    <footer className="border-t bg-muted/40">
      <div className="container px-4 py-12 md:py-16">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div>
            <Link href="/" className="text-xl font-bold text-primary">
              Inequality App
            </Link>
            <p className="mt-4 text-sm text-muted-foreground">
              Revealing passive income and wealth tax metrics for politicians and billionaires.
            </p>
          </div>

          {footerLinks.map((section) => (
            <div key={section.title}>
              <h3 className="text-base font-medium">{section.title}</h3>
              <ul className="mt-4 space-y-3">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-primary transition-colors"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Separator className="my-8" />

        <div className="text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} Inequality App Ltd. MIT License.</p>
          <p className="mt-2">Data sourced from public records and official disclosures.</p>
        </div>
      </div>
    </footer>
  )
}
