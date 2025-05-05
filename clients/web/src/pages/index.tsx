import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useQuery } from '@apollo/client';
import { gql } from '@apollo/client';
import Layout from '@/components/Layout';
import PersonCard from '@/components/PersonCard';
import SearchBar from '@/components/SearchBar';

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
`;

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const { loading, error, data } = useQuery(GET_TOP_POLITICIANS, {
    variables: { limit: 12 },
  });

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    // In a real app, this would trigger a new query with the search parameter
  };

  return (
    <Layout>
      <Head>
        <title>Inequality App | Financial Transparency for Public Figures</title>
        <meta
          name="description"
          content="Revealing passive income and wealth tax metrics for politicians and billionaires"
        />
      </Head>

      <section className="bg-gradient-to-b from-indigo-900 to-indigo-800 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-6">
              Financial Transparency for Public Figures
            </h1>
            <p className="text-xl mb-8">
              Discover how much passive income UK politicians and billionaires earn 
              each year and what a 1% wealth tax above £2 million would cost them.
            </p>
            
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </section>

      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Top MPs by Passive Income
          </h2>

          {loading ? (
            <div className="text-center">Loading politicians data...</div>
          ) : error ? (
            <div className="text-center text-red-600">
              Error loading data. Please try again later.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data?.persons.map((person: any) => (
                <PersonCard key={person.id} person={person} />
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link 
              href="/politicians"
              className="inline-block bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              View All Politicians
            </Link>
          </div>
        </div>
      </section>

      <section className="py-12 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-8">
              Why Financial Transparency Matters
            </h2>
            
            <div className="prose lg:prose-lg mx-auto">
              <p>
                Financial transparency in politics is essential for democracy. When politicians 
                have significant financial interests, the public deserves to know about potential 
                conflicts of interest.
              </p>
              
              <p>
                The Inequality App collects data from official sources including:
              </p>
              
              <ul>
                <li>UK Parliament's Register of Members' Financial Interests</li>
                <li>Companies House filings</li>
                <li>Land Registry records</li>
                <li>Forbes billionaire valuations</li>
              </ul>
              
              <p>
                We normalize this data and calculate metrics like yearly passive income and 
                potential wealth tax contributions to provide a clear picture of financial 
                inequality.
              </p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
} 