import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface Person {
  id: string;
  fullName: string;
  title?: string;
  constituency?: string;
  party?: string;
  yearlyPassiveIncome: number;
  wealthTaxContribution: number;
  photoUrl?: string;
}

interface PersonCardProps {
  person: Person;
}

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

const PersonCard: React.FC<PersonCardProps> = ({ person }) => {
  const {
    id,
    fullName,
    title,
    constituency,
    party,
    yearlyPassiveIncome,
    wealthTaxContribution,
    photoUrl,
  } = person;

  return (
    <Link href={`/person/${id}`} className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <div className="h-48 bg-gray-200 relative">
          {photoUrl ? (
            <Image
              src={photoUrl}
              alt={fullName}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="h-full flex items-center justify-center bg-indigo-100">
              <span className="text-4xl text-indigo-300">
                {fullName.charAt(0)}
              </span>
            </div>
          )}
        </div>

        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900">
            {title ? `${title} ` : ''}
            {fullName}
          </h3>

          {(constituency || party) && (
            <div className="text-sm text-gray-600 mt-1">
              {constituency && <span>{constituency}</span>}
              {constituency && party && <span> • </span>}
              {party && <span>{party}</span>}
            </div>
          )}

          <div className="mt-4 space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Yearly Passive Income:</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(yearlyPassiveIncome)}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-sm text-gray-500">Wealth Tax (1%):</span>
              <span className="text-sm font-medium text-gray-900">
                {formatCurrency(wealthTaxContribution)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default PersonCard; 