import Link from "next/link"
import Image from "next/image"

import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface Person {
  id: string
  fullName: string
  title?: string
  constituency?: string
  party?: string
  yearlyPassiveIncome: number
  wealthTaxContribution: number
  photoUrl?: string
}

interface PersonCardProps {
  person: Person
  className?: string
}

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

export default function PersonCard({ person, className }: PersonCardProps) {
  const { id, fullName, title, constituency, party, yearlyPassiveIncome, wealthTaxContribution, photoUrl } = person

  return (
    <Link href={`/person/${id}`} className={cn("block", className)}>
      <Card className="h-full overflow-hidden transition-all hover:shadow-lg hover:border-primary/50">
        <div className="aspect-[4/3] relative bg-muted">
          {photoUrl ? (
            <Image
              src={photoUrl || "/placeholder.svg"}
              alt={fullName}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="h-full flex items-center justify-center bg-primary/10">
              <Avatar className="h-24 w-24">
                <AvatarFallback className="text-4xl bg-primary/20 text-primary">{fullName.charAt(0)}</AvatarFallback>
              </Avatar>
            </div>
          )}
        </div>

        <CardHeader className="pb-2">
          <div className="flex flex-col gap-1">
            <h3 className="text-lg font-semibold line-clamp-1">
              {title ? `${title} ` : ""}
              {fullName}
            </h3>

            {(constituency || party) && (
              <div className="flex flex-wrap gap-2">
                {party && (
                  <Badge variant="outline" className="text-xs font-normal">
                    {party}
                  </Badge>
                )}
                {constituency && (
                  <Badge variant="secondary" className="text-xs font-normal">
                    {constituency}
                  </Badge>
                )}
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent className="pb-2">
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Yearly Passive Income:</span>
              <span className="text-sm font-medium">{formatCurrency(yearlyPassiveIncome)}</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Wealth Tax (1%):</span>
              <span className="text-sm font-medium">{formatCurrency(wealthTaxContribution)}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
