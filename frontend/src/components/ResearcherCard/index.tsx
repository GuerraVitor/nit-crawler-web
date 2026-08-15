import React from "react";
import {
  CardContainer,
  CardHeader,
  CardTitle,
  CardSubtitle,
  InterestsRow,
  InterestPill,
  CardFooter,
  FieldLabel,
  LattesLink,
} from "./style";

export interface Researcher {
  id: number;
  name: string;
  lattes_id: string;
  lattes_url: string;
  institution?: string;
  interests: string[];
  matched_interests?: string[];
}

interface ResearcherCardProps {
  researcher: Researcher;
}

const ResearcherCard: React.FC<ResearcherCardProps> = ({ researcher }) => {
  const matched = new Set(researcher.matched_interests || []);

  return (
    <CardContainer>
      <CardHeader>
        <CardTitle>{researcher.name}</CardTitle>
        {researcher.institution && (
          <CardSubtitle>{researcher.institution}</CardSubtitle>
        )}
      </CardHeader>

      <InterestsRow>
        {researcher.interests.map((interest) => (
          <InterestPill key={interest} $matched={matched.has(interest)}>
            {interest}
          </InterestPill>
        ))}
      </InterestsRow>

      <CardFooter>
        <div>
          <FieldLabel>ID Lattes:</FieldLabel>
          <span>{researcher.lattes_id}</span>
        </div>
        <LattesLink
          href={researcher.lattes_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Ver currículo Lattes
        </LattesLink>
      </CardFooter>
    </CardContainer>
  );
};

export default ResearcherCard;
