"use client"

import * as React from "react"
import { Search } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface SearchBarProps {
  onSearch: (query: string) => void
  className?: string
  placeholder?: string
}

export default function SearchBar({
  onSearch,
  className,
  placeholder = "Search for a politician or billionaire...",
}: SearchBarProps) {
  const [query, setQuery] = React.useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className={cn("relative w-full max-w-lg", className)}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          placeholder={placeholder}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-10 pr-12 py-6 rounded-full border-2 focus-visible:ring-primary"
        />
        <Button type="submit" size="sm" className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full">
          Search
        </Button>
      </div>
    </form>
  )
}
