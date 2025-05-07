import { useState } from "react"
import Head from "next/head"
import Link from "next/link"
import { useQuery } from "@apollo/client"
import { gql } from "@apollo/client"
import Layout from "@/components/Layout"
import PersonCard from "@/components/PersonCard"
import SearchBar from "@/components/SearchBar"
import { ArrowRight, BarChart2, Shield, Database } from "lucide-react"

// GraphQL query to fetch top politicians with highest passive income
const GET_TOP_POLITICIANS = gql`
  query GetTopPoliticians($limit: Int!) {
    persons(type: POLITICIAN, limit: $limit) {
      id
      fullName
      title
      constituency
      party
      yearlyPassiveIncome
      wealthTaxContribution
      photoUrl
    }
  }
`

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("")
  const { loading, error, data } = useQuery(GET_TOP_POLITICIANS, {
    variables: { limit: 12 },
  })

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    // In a real app, this would trigger a new query with the search parameter
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

      <section className="relative bg-gradient-to-br from-indigo-950 via-indigo-900 to-purple-900 text-white py-28 overflow-hidden">
        <div className="absolute inset-0 bg-[url('/placeholder.svg?height=100&width=100')] bg-repeat opacity-5"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 tracking-tight">
              Financial Transparency for Public Figures
            </h1>
            <p className="text-xl md:text-2xl mb-10 text-indigo-100 leading-relaxed">
              Discover how much passive income UK politicians and billionaires earn each year and what a 1% wealth tax
              above £2 million would cost them.
            </p>

            <div className="transition-all duration-300 transform hover:scale-[1.02]">
              <SearchBar onSearch={handleSearch} />
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-gray-50 to-transparent"></div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">Top MPs by Passive Income</h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Explore the financial interests of the UK's most influential politicians and their potential conflicts of
            interest.
          </p>

          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent"></div>
              <p className="mt-4 text-gray-600">Loading politicians data...</p>
            </div>
          ) : error ? (
            <div className="text-center py-20 text-red-600">
              <p className="font-medium">Error loading data. Please try again later.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {data?.persons.map((person: any) => (
                <div key={person.id} className="transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
                  <PersonCard person={person} />
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-16">
            <Link
              href="/politicians"
              className="group inline-flex items-center gap-2 bg-indigo-600 text-white py-3 px-8 rounded-full hover:bg-indigo-700 transition-all duration-300 shadow-md hover:shadow-xl"
            >
              View All Politicians
              <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-8">Why Financial Transparency Matters</h2>

            <div className="grid md:grid-cols-3 gap-8 mb-12">
              <div className="bg-gray-50 p-6 rounded-xl">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                  <Shield className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Democratic Integrity</h3>
                <p className="text-gray-600">
                  Financial transparency ensures politicians serve the public interest, not their own financial gain.
                </p>
              </div>

              <div className="bg-gray-50 p-6 rounded-xl">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                  <BarChart2 className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Inequality Insights</h3>
                <p className="text-gray-600">
                  Understanding wealth distribution helps inform policy discussions about taxation and inequality.
                </p>
              </div>

              <div className="bg-gray-50 p-6 rounded-xl">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                  <Database className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Data-Driven Policy</h3>
                <p className="text-gray-600">
                  Accurate financial data enables better policy decisions and more informed public debate.
                </p>
              </div>
            </div>

            <div className="prose lg:prose-lg mx-auto bg-gray-50 p-8 rounded-xl border border-gray-100">
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
