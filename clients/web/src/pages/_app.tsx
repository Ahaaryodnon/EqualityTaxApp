import type { AppProps } from 'next/app';
import { ApolloProvider } from '@apollo/client';
import client from '../lib/apolloClient';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ApolloProvider client={client}>
      <Component {...pageProps} />
    </ApolloProvider>
  );
} 