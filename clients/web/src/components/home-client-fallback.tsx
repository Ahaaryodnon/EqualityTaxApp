"use client"

import { useState } from "react"
import Head from "next/head"
import Link from "next/link"

import Layout from "@/components/layout"
import PersonCard from "@/components/person-card"
import SearchBar from "@/components/search-bar"
import { Button } from "@/components/ui/button"
import { mockPoliticians } from "./mock-data"

export default function HomeClientFallback() {
  const [searchQuery, setSearchQuery] = useState("")

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    // In a real app, this would trigger a search
  }

  return (
    <Layout>
      <Head>
        <title>Inequality App | Financial Transparency for Public Figures</title>
        <meta
          name="description"
          content="Revealing passive income and wealth tax metrics for politicians and billionaires"
        />
      </Head>

      <section className="relative bg-gradient-to-b from-primary to-primary-foreground py-20 md:py-28">
        <div className="container px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="mb-6 text-4xl font-bold text-white md:text-5xl lg:text-6xl">
              Financial Transparency for Public Figures
            </h1>
            <p className="mb-8 text-lg text-white/90 md:text-xl">
              Discover how much passive income UK politicians and billionaires earn each year and what a 1% wealth tax
              above £2 million would cost them.
            </p>

            <SearchBar onSearch={handleSearch} className="mx-auto" />
          </div>
        </div>
        <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,transparent,rgba(255,255,255,0.5),transparent)]" />
      </section>

      <section className="py-16 bg-muted/30">
        <div className="container px-4">
          <h2 className="mb-12 text-center text-3xl font-bold md:text-4xl">Top MPs by Passive Income</h2>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {mockPoliticians.map((person) => (
              <PersonCard key={person.id} person={person} />
            ))}
          </div>

          <div className="mt-12 text-center">
            <Button asChild size="lg">
              <Link href="/politicians">View All Politicians</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="py-16 bg-background">
        <div className="container px-4">
          <div className="mx-auto max-w-3xl">
            <h2 className="mb-8 text-center text-3xl font-bold md:text-4xl">Why Financial Transparency Matters</h2>

            <div className="prose prose-gray mx-auto dark:prose-invert lg:prose-lg">
              <p>
                Financial transparency in politics is essential for democracy. When politicians have significant
                financial interests, the public deserves to know about potential conflicts of interest.
              </p>

              <p>The Inequality App collects data from official sources including:</p>

              <ul>
                <li>UK Parliament's Register of Members' Financial Interests</li>
                <li>Companies House filings</li>
                <li>Land Registry records</li>
                <li>Forbes billionaire valuations</li>
              </ul>

              <p>
                We normalize this data and calculate metrics like yearly passive income and potential wealth tax
                contributions to provide a clear picture of financial inequality.
              </p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}
