import type { AppProps } from "next/app"
import { ThemeProvider } from "@/components/theme-provider"
import { ApolloWrapper } from "../lib/apollo-provider"
import "@/app/globals.css"

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ApolloWrapper>
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
        <Component {...pageProps} />
      </ThemeProvider>
    </ApolloWrapper>
  )
}
